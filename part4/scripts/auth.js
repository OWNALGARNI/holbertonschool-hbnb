export function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

export function getCookie(name) {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith(name + "="))
    ?.split("=")[1];
}

export function getToken() {
  const token = getCookie("token");
  return token ? decodeURIComponent(token) : null;
}

export function requireAuth(redirect = "login.html") {
  if (!getToken()) {
    window.location.href = redirect;
  }
}