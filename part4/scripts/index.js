import { API_BASE } from "./config.js";
import { getToken, requireAuth } from "./auth.js";

requireAuth("login.html");

const placesContainer = document.getElementById("places-list");

async function fetchPlaces() {
  try {
    const response = await fetch(`${API_BASE}/places`, {
      headers: {
        "Authorization": `Bearer ${getToken()}`
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch places");
    }

    const places = await response.json();
    renderPlaces(places);

  } catch (error) {
    console.error(error);
  }
}

function renderPlaces(places) {
  placesContainer.innerHTML = "";

  places.forEach(place => {
    const card = document.createElement("article");
    card.classList.add("place-card");

    card.innerHTML = `
      <h2 class="place-title">${place.name}</h2>
      <p class="place-price">$${place.price_per_night} / night</p>
      <a class="details-button" href="place.html?id=${place.id}">
        View Details
      </a>
    `;

    placesContainer.appendChild(card);
  });
}

fetchPlaces();