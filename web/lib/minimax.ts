/**
 * Minimax M3 Service
 * ==================
 * Primary AI provider for the AgenticMarketingPro system.
 * OpenAI-compatible API with MiniMax-M3 model (1M context, reasoning support).
 *
 * Base URL: https://api.minimax.io/v1
 * Model: MiniMax-M3
 * Docs: https://minimax-ai.chat/docs/api/
 */

export interface MinimaxMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  name?: string;
  tool_calls?: MinimaxToolCall[];
}

export interface MinimaxToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: string;
  };
}

export interface MinimaxTool {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: {
      type: "object";
      properties: Record<string, any>;
      required?: string[];
    };
  };
}

export interface MinimaxCompletionOptions {
  model?: string;
  messages: MinimaxMessage[];
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  stream?: boolean;
  tools?: MinimaxTool[];
  tool_choice?: "auto" | "none" | { type: "function"; function: { name: string } };
  reasoning_split?: boolean;
  thinking?: boolean;
  stream_options?: {
    include_usage?: boolean;
  };
}

export interface MinimaxUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface MinimaxCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    index: number;
    message: {
      role: string;
      content: string | null;
      reasoning_details?: string;
      tool_calls?: MinimaxToolCall[];
    };
    finish_reason: string | null;
  }[];
  usage: MinimaxUsage;
}

export interface MinimaxStreamChunk {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    index: number;
    delta: {
      role?: string;
      content?: string | null;
      reasoning_details?: string;
      tool_calls?: MinimaxToolCall[];
    };
    finish_reason: string | null;
  }[];
  usage?: MinimaxUsage;
}

// ── Default configuration ──
const DEFAULT_BASE_URL = "https://api.minimax.io/v1";
const DEFAULT_MODEL = "MiniMax-M3";
const DEFAULT_TEMPERATURE = 0.7;
const DEFAULT_MAX_TOKENS = 4096;

// ── Cost tracking (per 1K tokens, approximate) ──
const COST_PER_1K_INPUT = 0.0015;   // $0.0015 per 1K input tokens
const COST_PER_1K_OUTPUT = 0.006;   // $0.006 per 1K output tokens

/**
 * Build the authorization header for Minimax API
 */
function buildAuthHeader(apiKey: string): string {
  return `Bearer ${apiKey}`;
}

/**
 * Call Minimax M3 chat completions API
 */
export async function callMinimaxM3(
  apiKey: string,
  options: MinimaxCompletionOptions,
  baseUrl: string = DEFAULT_BASE_URL
): Promise<MinimaxCompletionResponse> {
  const url = `${baseUrl}/chat/completions`;

  const body = {
    model: options.model || DEFAULT_MODEL,
    messages: options.messages,
    temperature: options.temperature ?? DEFAULT_TEMPERATURE,
    max_tokens: options.max_tokens ?? DEFAULT_MAX_TOKENS,
    top_p: options.top_p ?? 1.0,
    stream: false,
    ...(options.tools ? { tools: options.tools } : {}),
    ...(options.tool_choice ? { tool_choice: options.tool_choice } : {}),
    ...(options.reasoning_split !== undefined ? { reasoning_split: options.reasoning_split } : { reasoning_split: true }),
    ...(options.thinking !== undefined ? { thinking: options.thinking } : {}),
  };

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": buildAuthHeader(apiKey),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Minimax API error ${res.status}: ${errText}`);
  }

  return res.json();
}

/**
 * Stream Minimax M3 chat completions
 */
export async function* streamMinimaxM3(
  apiKey: string,
  options: MinimaxCompletionOptions,
  baseUrl: string = DEFAULT_BASE_URL
): AsyncGenerator<MinimaxStreamChunk, void, unknown> {
  const url = `${baseUrl}/chat/completions`;

  const body = {
    model: options.model || DEFAULT_MODEL,
    messages: options.messages,
    temperature: options.temperature ?? DEFAULT_TEMPERATURE,
    max_tokens: options.max_tokens ?? DEFAULT_MAX_TOKENS,
    top_p: options.top_p ?? 1.0,
    stream: true,
    ...(options.tools ? { tools: options.tools } : {}),
    ...(options.tool_choice ? { tool_choice: options.tool_choice } : {}),
    ...(options.reasoning_split !== undefined ? { reasoning_split: options.reasoning_split } : { reasoning_split: true }),
    ...(options.thinking !== undefined ? { thinking: options.thinking } : {}),
    stream_options: { include_usage: true },
  };

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": buildAuthHeader(apiKey),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Minimax API error ${res.status}: ${errText}`);
  }

  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed === "data: [DONE]") continue;
      if (trimmed.startsWith("data: ")) {
        try {
          const chunk: MinimaxStreamChunk = JSON.parse(trimmed.slice(6));
          yield chunk;
        } catch (_e) {
          // Skip malformed chunks
        }
      }
    }
  }
}

/**
 * Simple non-streaming call with system + user prompt
 */
export async function callMinimaxM3Simple(
  apiKey: string,
  systemPrompt: string,
  userPrompt: string,
  options: Partial<MinimaxCompletionOptions> = {},
  baseUrl: string = DEFAULT_BASE_URL
): Promise<{ content: string; tokensIn: number; tokensOut: number; reasoning?: string }> {
  const messages: MinimaxMessage[] = [
    { role: "system", content: systemPrompt },
    { role: "user", content: userPrompt },
  ];

  const res = await callMinimaxM3(apiKey, {
    messages,
    ...options,
  }, baseUrl);

  const choice = res.choices[0];
  const content = choice?.message?.content || "";
  const reasoning = choice?.message?.reasoning_details || "";
  const usage = res.usage || { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 };

  return {
    content,
    tokensIn: usage.prompt_tokens,
    tokensOut: usage.completion_tokens,
    reasoning: reasoning || undefined,
  };
}

/**
 * Calculate cost from token usage
 */
export function calculateMinimaxCost(tokensIn: number, tokensOut: number): number {
  const inputCost = (tokensIn / 1000) * COST_PER_1K_INPUT;
  const outputCost = (tokensOut / 1000) * COST_PER_1K_OUTPUT;
  return Number((inputCost + outputCost).toFixed(6));
}

/**
 * Build a system prompt optimized for Minimax M3
 * M3 works best with clear, structured prompts with explicit reasoning instructions
 */
export function buildMinimaxSystemPrompt(basePrompt: string): string {
  return `${basePrompt}

## Response Guidelines
- Think step-by-step before answering
- Be concise but thorough
- Use markdown formatting for readability
- When uncertain, state your reasoning clearly
- Always provide actionable, specific recommendations`;
}

/**
 * Strip thinking tags from Minimax M3 output (when reasoning_split is false)
 */
export function stripMinimaxThinking(content: string): string {
  return content.replace(/<thinking>[\s\S]*?<\/thinking>/g, "").trim();
}
