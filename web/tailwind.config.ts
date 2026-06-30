import { type Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f0f1a",
        card: "#1a1a2e",
        border: "#2a2a40",
        text: "#e0e0e0",
        muted: "#888",
        accent: "#4A90D9",
        "accent-hover": "#357ABD",
        danger: "#E74C3C",
        success: "#50C878",
        warning: "#F39C12",
      },
    },
  },
  plugins: [],
};

export default config;
