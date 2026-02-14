import { API_BASE } from "./config.js";
import { setCookie } from "./auth.js";

const form = document.getElementById("login-form");
const msg = document.getElementById("login-message");

function showMessage(text, isError = true) {
  msg.textContent = text;
  msg.style.color = isError ? "#b91c1c" : "#065f46";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showMessage("");

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    showMessage("Please enter email and password.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      showMessage(data.message || "Login failed. Check your credentials.");
      return;
    }

    // توقع شائع: { "access_token": "..." } أو { "token": "..." }
    const token = data.access_token || data.token || data.jwt;

    if (!token) {
      showMessage("Login succeeded but token not found in response.");
      return;
    }

    setCookie("token", token, 1); 
    showMessage("Login successful! Redirecting...", false);

    window.location.href = "index.html";
  } catch (err) {
    showMessage("Network error. Check API server and CORS.");
  }
});