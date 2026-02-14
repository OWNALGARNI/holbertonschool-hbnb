import { API_BASE } from "./config.js";
import { getToken, getCookie, logout } from "./auth.js";

const placesContainer = document.getElementById("places-list");
const priceFilter = document.getElementById("price-filter");
const loginButton = document.getElementById("header-login");

let allPlaces = [];

/**
 * Check user authentication and update login button
 */
function checkAuthentication() {
  const token = getToken();
  
  if (token) {
    // User is authenticated - change button to Logout
    loginButton.textContent = "Logout";
    loginButton.href = "#";
    loginButton.addEventListener("click", (e) => {
      e.preventDefault();
      logout("index.html");
    });
  } else {
    // User is not authenticated - show Login
    loginButton.textContent = "Login";
    loginButton.href = "login.html";
  }
}

/**
 * Fetch places from API with authentication token if available
 */
async function fetchPlaces() {
  try {
    const token = getToken();
    const headers = {
      "Content-Type": "application/json"
    };
    
    // Include token in Authorization header if available
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}/places`, { headers });

    const data = await res.json().catch(() => []);
    if (!res.ok) {
      console.error("Failed to fetch places:", data);
      return;
    }

    allPlaces = Array.isArray(data) ? data : [];
    renderPlaces(allPlaces);
  } catch (err) {
    console.error("Network error fetching places:", err);
  }
}

/**
 * Render places list
 */
function renderPlaces(places) {
  placesContainer.innerHTML = "";

  places.forEach((place) => {
    const card = document.createElement("article");
    card.classList.add("place-card");
    card.dataset.price = place.price || 0;

    const price = place.price ?? "—";
    const title = place.title ?? "Unnamed place";

    card.innerHTML = `
      <h2 class="place-title">${title}</h2>
      <p class="place-price">$${price} / night</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;

    placesContainer.appendChild(card);
  });

  if (places.length === 0) {
    placesContainer.innerHTML = `<p class="form-message" style="color:#6b7280;">No places found.</p>`;
  }
}

/**
 * Filter places by price without reloading the page
 */
function filterPlacesByPrice() {
  const selectedPrice = priceFilter.value;
  const placeCards = document.querySelectorAll(".place-card");

  placeCards.forEach((card) => {
    const cardPrice = parseFloat(card.dataset.price) || 0;

    if (selectedPrice === "all") {
      card.style.display = "";
    } else {
      const maxPrice = parseFloat(selectedPrice);
      if (cardPrice <= maxPrice) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    }
  });
}

// Event listener for price filter
priceFilter.addEventListener("change", filterPlacesByPrice);

// Initialize page
checkAuthentication();
fetchPlaces();