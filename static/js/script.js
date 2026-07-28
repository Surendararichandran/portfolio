// script.js
// Submits the contact form to the Flask backend (POST /api/contact)
// and shows the response inline, styled like the rest of the page.

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  const statusEl = document.getElementById("contact-status");
  const submitBtn = document.getElementById("contact-submit");

  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      message: document.getElementById("message").value.trim(),
    };

    statusEl.textContent = "";
    statusEl.className = "";
    submitBtn.disabled = true;
    submitBtn.textContent = "sending...";

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        statusEl.textContent = `// ${data.status} — ${data.detail}`;
        statusEl.className = "ok";
        form.reset();
      } else {
        statusEl.textContent = `// 400 Bad Request — ${data.detail}`;
        statusEl.className = "err";
      }
    } catch (err) {
      statusEl.textContent = "// network error — could not reach the server";
      statusEl.className = "err";
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "send message";
    }
  });
});
