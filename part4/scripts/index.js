import { API_BASE } from "./config.js";

const placesContainer = document.getElementById("places-list");

async function fetchPlaces() {
  try {
    const response = await fetch(`${API_BASE}/places`);

    if (!response.ok) {
      throw new Error("Failed to fetch places");
    }

    const places = await response.json();
    renderPlaces(places);

  } catch (error) {
    console.error(error);
    placesContainer.innerHTML = '<p>Failed to load places. Please try again later.</p>';
  }
}

function renderPlaces(places) {
  placesContainer.innerHTML = "";

  if (!places || places.length === 0) {
    placesContainer.innerHTML = '<p>No places available yet.</p>';
    return;
  }

  places.forEach(place => {
    const card = document.createElement("article");
    card.classList.add("place-card");

    card.innerHTML = `
      <h2 class="place-title">${place.title || 'Untitled'}</h2>
      <p class="place-price">$${place.price || 0} / night</p>
      <a class="details-button" href="place.html?id=${place.id}">
        View Details
      </a>
    `;

    placesContainer.appendChild(card);
  });
}

fetchPlaces();