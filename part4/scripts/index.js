import { API_BASE } from "./config.js";
import { getToken, requireAuth } from "./auth.js";

requireAuth("login.html");

const placesContainer = document.getElementById("places-list");
const countrySelect = document.getElementById("country-filter");

let allPlaces = [];

async function fetchPlaces() {
  try {
    const res = await fetch(`${API_BASE}/places`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    });

    const data = await res.json().catch(() => []);
    if (!res.ok) {
      console.error("Failed to fetch places:", data);
      return;
    }

    allPlaces = Array.isArray(data) ? data : [];
    fillCountries(allPlaces);
    renderPlaces(allPlaces);
  } catch (err) {
    console.error("Network error fetching places:", err);
  }
}

function getCountryName(place) {
  // حاول تغطي أكثر من شكل يرجع من API
  return (
    place.country_name ||
    place.country ||
    (place.city && place.city.country_name) ||
    (place.city && place.city.country) ||
    "Unknown"
  );
}

function fillCountries(places) {
  const countries = new Set();
  places.forEach((p) => countries.add(getCountryName(p)));

  const sorted = Array.from(countries).sort((a, b) =>
    a.localeCompare(b, "en", { sensitivity: "base" })
  );

  // نظّف الخيارات القديمة (واترك All)
  countrySelect.innerHTML = `<option value="all">All</option>`;

  sorted.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    countrySelect.appendChild(opt);
  });
}

function renderPlaces(places) {
  placesContainer.innerHTML = "";

  places.forEach((place) => {
    const card = document.createElement("article");
    card.classList.add("place-card");

    const price = place.price_per_night ?? place.price ?? "—";

    card.innerHTML = `
      <h2 class="place-title">${place.name ?? "Unnamed place"}</h2>
      <p class="place-price">$${price} / night</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;

    placesContainer.appendChild(card);
  });

  // لو ما فيه نتائج بعد الفلترة
  if (places.length === 0) {
    placesContainer.innerHTML = `<p class="form-message" style="color:#6b7280;">No places found.</p>`;
  }
}

countrySelect.addEventListener("change", () => {
  const selected = countrySelect.value;

  if (selected === "all") {
    renderPlaces(allPlaces);
    return;
  }

  const filtered = allPlaces.filter((p) => getCountryName(p) === selected);
  renderPlaces(filtered);
});

fetchPlaces();