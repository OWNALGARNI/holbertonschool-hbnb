// File: part4/scripts/auth.js

export function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();

  // Encode safely
  const encoded = encodeURIComponent(value);

  // Better defaults for browsers
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie =
    `${name}=${encoded}; expires=${expires}; path=/; SameSite=Lax${secure}`;
}

export function getCookie(name) {
  const found = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));

  if (!found) return null;

  // Keep everything after the first '=' (in case the value contains '=')
  const rawValue = found.substring(found.indexOf("=") + 1);
  return rawValue || null;
}

export function deleteCookie(name) {
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax${secure}`;
}

export function getToken() {
  const token = getCookie("token");
  if (!token) return null;

  // Decode safely (avoid crashes if token has bad encoding)
  try {
    return decodeURIComponent(token);
  } catch {
    return token;
  }
}

export function isAuthenticated() {
  return !!getToken();
}

export function requireAuth(redirect = "login.html") {
  if (!isAuthenticated()) {
    window.location.href = redirect;
    return false;
  }
  return true;
}

export function logout(redirect = "index.html") {
  deleteCookie("token");
  window.location.href = redirect;
}
