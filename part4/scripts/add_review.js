// File: part4/scripts/add_review.js

import { API_BASE } from "./config.js";
import { getToken, requireAuth, logout } from "./auth.js";

/**
 * Get place ID from URL query parameters
 */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("place_id");
}

/**
 * Display message to user
 */
function displayMessage(message, isError = false) {
  const el = document.getElementById("review-message");
  if (!el) return;

  el.textContent = message;
  el.style.color = isError ? "#dc2626" : "#16a34a";
  el.style.display = "block";
}

/**
 * Clear the review form
 */
function clearForm() {
  const form = document.getElementById("review-form");
  if (form) form.reset();
}

/**
 * Submit review to API
 */
async function submitReview(token, placeId, reviewText, rating) {
  const res = await fetch(`${API_BASE}/reviews/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      place_id: placeId,
      text: reviewText,
      rating: parseInt(rating, 10),
    }),
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    throw new Error(
      (data && (data.error || data.message)) ||
        `Failed to submit review (HTTP ${res.status})`
    );
  }

  return data;
}

/**
 * Handle form submit
 */
async function handleReviewSubmit(event) {
  event.preventDefault();

  const token = getToken();
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    displayMessage("Error: No place specified", true);
    setTimeout(() => (window.location.href = "index.html"), 1500);
    return;
  }

  const comment = document.getElementById("comment")?.value.trim();
  const rating = document.getElementById("rating")?.value;

  if (!comment) {
    displayMessage("Please enter a review comment", true);
    return;
  }

  const ratingNum = parseInt(rating, 10);
  if (!rating || ratingNum < 1 || ratingNum > 5) {
    displayMessage("Please select a rating between 1 and 5", true);
    return;
  }

  const submitBtn = event.target.querySelector('button[type="submit"]');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";
  }

  try {
    await submitReview(token, placeId, comment, ratingNum);
    displayMessage("Review submitted successfully!");
    clearForm();

    setTimeout(() => {
      window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;
    }, 1200);
  } catch (err) {
    displayMessage(`Error: ${err.message}`, true);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Review";
    }
  }
}

/**
 * Initialize page
 */
function initAddReviewPage() {
  // Require login
  requireAuth("index.html");

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    displayMessage("Error: No place specified", true);
    setTimeout(() => (window.location.href = "index.html"), 1500);
    return;
  }

  const form = document.getElementById("review-form");
  if (form) form.addEventListener("submit", handleReviewSubmit);

  // Header logout button
  const loginBtn = document.getElementById("header-login");
  if (loginBtn && getToken()) {
    loginBtn.textContent = "Logout";
    loginBtn.href = "#";
    loginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      logout("index.html");
    });
  }
}

document.addEventListener("DOMContentLoaded", initAddReviewPage);
