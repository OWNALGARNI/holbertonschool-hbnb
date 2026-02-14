import { API_BASE } from "./config.js";
import { getToken } from "./auth.js";

const placeNameEl = document.getElementById("place-name");
const hostEl = document.getElementById("place-host");
const priceEl = document.getElementById("place-price");
const descEl = document.getElementById("place-description");
const amenitiesEl = document.getElementById("place-amenities");
const reviewsEl = document.getElementById("reviews-list");
const addReviewLink = document.getElementById("add-review-link");

function getPlaceId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function setAddReviewLink(placeId) {
  const token = getToken();
  if (!token) {
    // غير مسجّل: اخف الزر
    addReviewLink.style.display = "none";
    return;
  }
  addReviewLink.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
}

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  const data = await res.json().catch(() => null);
  return { res, data };
}

function renderAmenities(amenities) {
  amenitiesEl.innerHTML = "";
  if (!amenities || amenities.length === 0) {
    amenitiesEl.innerHTML = "<li>—</li>";
    return;
  }
  amenities.forEach((a) => {
    const li = document.createElement("li");
    li.textContent = a.name || a;
    amenitiesEl.appendChild(li);
  });
}

function renderReviews(reviews) {
  reviewsEl.innerHTML = "";

  if (!reviews || reviews.length === 0) {
    reviewsEl.innerHTML = `
      <p class="form-message" style="color:#6b7280;">No reviews yet.</p>
    `;
    return;
  }

  reviews.forEach((r) => {
    const card = document.createElement("article");
    card.classList.add("review-card");

    const username = 
      (r.user && `${r.user.first_name || ""} ${r.user.last_name || ""}`.trim()) ||
      (r.user && r.user.email) ||
      "Anonymous";

    const rating = r.rating ?? "—";
    const comment = r.text ?? r.comment ?? "—";

    card.innerHTML = `
      <p class="review-comment">${comment}</p>
      <p class="review-meta">by <span>${username}</span> — ⭐ <span>${rating}</span></p>
    `;

    reviewsEl.appendChild(card);
  });
}

async function loadPlace() {
  const placeId = getPlaceId();
  if (!placeId) {
    placeNameEl.textContent = "Place not found (missing id)";
    addReviewLink.style.display = "none";
    return;
  }

  setAddReviewLink(placeId);

  // جلب تفاصيل المكان
  const { res: placeRes, data: place } = await fetchJSON(
    `${API_BASE}/places/${encodeURIComponent(placeId)}`,
    {
      headers: getToken() ? { Authorization: `Bearer ${getToken()}` } : {},
    }
  );

  if (!placeRes.ok || !place) {
    placeNameEl.textContent = "Failed to load place details.";
    addReviewLink.style.display = "none";
    return;
  }

  placeNameEl.textContent = place.title ?? "Unnamed place";
  priceEl.textContent = `$${place.price ?? "—"} / night`;
  descEl.textContent = place.description ?? "—";

  // host
  const ownerFirstName = place.first_name || (place.owner && place.owner.first_name) || "";
  const ownerLastName = place.last_name || (place.owner && place.owner.last_name) || "";
  const host = ownerFirstName && ownerLastName 
    ? `${ownerFirstName} ${ownerLastName}` 
    : (place.owner && place.owner.email) || "—";
  hostEl.textContent = host;

  // amenities
  renderAmenities(place.amenities);

  // reviews: أحيانًا ترجع داخل place، وأحيانًا endpoint مستقل
  let reviews = place.reviews;

  if (!reviews) {
    const { res: revRes, data: revData } = await fetchJSON(
      `${API_BASE}/places/${encodeURIComponent(placeId)}/reviews`,
      {
        headers: getToken() ? { Authorization: `Bearer ${getToken()}` } : {},
      }
    );

    if (revRes.ok && Array.isArray(revData)) {
      reviews = revData;
    } else {
      reviews = [];
    }
  }

  renderReviews(reviews);
}

loadPlace();