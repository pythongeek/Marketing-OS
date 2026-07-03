(function () {
  "use strict";

  // ═══════════════════════════════════════════════════════════
  // AgenticMarketingPro — Form API Connector
  // All skill forms include this script to:
  // 1. Fetch clients from API and show a dropdown
  // 2. POST form data to /api/webhook to create a job
  // 3. Show real-time status messages
  // ═══════════════════════════════════════════════════════════

  const API_BASE = "";
  let clients = [];

  // ── Fetch clients from API ──────────────────────────────
  async function loadClients() {
    try {
      const res = await fetch(API_BASE + "/api/clients");
      const data = await res.json();
      clients = data.clients || [];
      injectClientSelector();
    } catch (e) {
      console.error("Failed to load clients:", e);
    }
  }

  // ── Inject client dropdown into every form ──────────────
  function injectClientSelector() {
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
      // Skip client onboarding form (creates new clients, doesn't select one)
      const skillSlug = form.dataset.skillSlug || "";
      if (skillSlug === "client-onboarding") return;
      if (form.querySelector("[name=client_slug]")) return; // already injected

      const wrapper = document.createElement("div");
      wrapper.className = "form-section";
      wrapper.innerHTML = `
        <div class="section-header">
          <div class="section-title">👤 Client</div>
          <div class="section-desc">Select the client for this job</div>
        </div>
        <div class="form-group">
          <label class="required">Select Client</label>
          <select name="client_slug" class="form-input" required>
            <option value="">-- Choose a client --</option>
            ${clients.map((c) => `<option value="${c.slug}">${c.name} (${c.slug})</option>`).join("")}
          </select>
          <div class="field-help">This job will be tagged to this client</div>
        </div>
      `;
      form.insertBefore(wrapper, form.firstChild);
    });
  }

  // ── Override form submit to create job via API ──────────
  function attachFormSubmit() {
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
      if (form.dataset.apiHooked) return;
      // Skip client onboarding form — it has its own /api/clients handler
      if (form.dataset.skillSlug === "client-onboarding") return;
      form.dataset.apiHooked = "true";

      form.addEventListener("submit", async function (e) {
        // Let the existing handler run first (for JSON export)
        // Then we create the job
        setTimeout(async () => {
          const clientSlug = form.querySelector("[name=client_slug]")?.value;
          if (!clientSlug) {
            showStatus(form, "❌ Please select a client first", "error");
            return;
          }

          const skillSlug = form.dataset.skillSlug || "general";
          const payload = collectFormData(form);

          try {
            const res = await fetch(API_BASE + "/api/webhook", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                type: "agent_run",
                client_slug: clientSlug,
                skill_slug: skillSlug,
                payload: payload,
              }),
            });
            const result = await res.json();
            if (res.ok) {
              showStatus(form, `✅ Job #${result.job_id} created! Check the Jobs page for progress.`, "success");
            } else {
              showStatus(form, `❌ Failed to create job: ${result.error || "Unknown error"}`, "error");
            }
          } catch (err) {
            showStatus(form, `❌ Network error: ${err.message}`, "error");
          }
        }, 100);
      });
    });
  }

  // ── Collect all form data into a clean object ───────────
  function collectFormData(form) {
    const data = {};
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      if (input.name && !input.name.startsWith("_")) {
        if (input.type === "checkbox") {
          data[input.name] = input.checked;
        } else if (input.type === "number") {
          data[input.name] = Number(input.value);
        } else {
          data[input.name] = input.value;
        }
      }
    });
    return data;
  }

  // ── Show status message below form ──────────────────────
  function showStatus(form, message, type) {
    let status = form.parentElement.querySelector(".form-api-status");
    if (!status) {
      status = document.createElement("div");
      status.className = "form-api-status";
      form.parentElement.appendChild(status);
    }
    status.textContent = message;
    status.className = "form-api-status " + type;
    status.style.cssText = `
      margin-top: 16px;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 500;
    `;
    if (type === "success") {
      status.style.background = "rgba(80, 200, 120, 0.15)";
      status.style.color = "#50C878";
      status.style.border = "1px solid rgba(80, 200, 120, 0.3)";
    } else {
      status.style.background = "rgba(231, 76, 60, 0.15)";
      status.style.color = "#E74C3C";
      status.style.border = "1px solid rgba(231, 76, 60, 0.3)";
    }
  }

  // ── Initialize ──────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", function () {
    loadClients();
    attachFormSubmit();
  });
})();
