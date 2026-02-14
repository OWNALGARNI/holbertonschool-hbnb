// File: part4/scripts/add_review.js

import { API_BASE } from "./config.js";
import { getToken, requireAuth } from "./auth.js";

/**
 * Get place ID from URL query parameters
 * @returns {string|null} The place ID or null if not found
 */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("place_id");
}

/**
 * Display message to user
 * @param {string} message
 * @param {boolean} isError
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
 * Submit a review to the API
 * @param {string} token
 * @param {string} placeId
 * @param {string} reviewText
 * @param {number|string} rating
 */
async function submitReview(token, placeId, reviewText, rating) {
  const payload = {
    place_id: placeId,
    text: reviewText,
    rating: parseInt(rating, 10),
  };

  const res = await fetch(`${API_BASE}/reviews/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  // حاول تقرأ JSON حتى لو فشل
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    const msg =
      (data && (data.error || data.message)) ||
      `Failed to submit review (HTTP ${res.status})`;
    throw new Error(msg);
  }

  return data;
}

/**
 * Handle review form submission
 * @param {Event} event
 */
async function handleReviewSubmit(event) {
  event.preventDefault();

  const token = getToken();
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    displayMessage("Error: No place ID provided", true);
    setTimeout(() => (window.location.href = "index.html"), 1500);
    return;
  }

  const commentEl = document.getElementById("comment");
  const ratingEl = document.getElementById("rating");

  const reviewText = commentEl ? commentEl.value.trim() : "";
  const rating = ratingEl ? ratingEl.value : "";

  if (!reviewText) {
    displayMessage("Please enter a review comment", true);
    return;
  }

  const ratingNum = parseInt(rating, 10);
  if (!rating || Number.isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
    displayMessage("Please select a rating between 1 and 5", true);
    return;
  }

  const submitButton = event.target.querySelector('button[type="submit"]');
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";
  }

  try {
    await submitReview(token, placeId, reviewText, ratingNum);
    displayMessage("Review submitted successfully!", false);
    clearForm();

    setTimeout(() => {
      window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;
    }, 1200);
  } catch (err) {
    displayMessage(`Error: ${err.message}`, true);
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "Submit Review";
    }
  }
}

/**
 * Initialize add review page
 */
function initAddReviewPage() {
  // Redirect to index.html if not authenticated
  requireAuth("index.html");

  const token = getToken();
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    displayMessage("Error: No place specified", true);
    setTimeout(() => (window.location.href = "index.html"), 1500);
    return;
  }

  const form = document.getElementById("review-form");
  if (form) form.addEventListener("submit", handleReviewSubmit);

  // Optional: update header login button to logout
  if (token) {
    const loginButton = document.getElementById("header-login");
    if (loginButton) {
      loginButton.textContent = "Logout";
      loginButton.href = "#";
      loginButton.addEventListener("click", (e) => {
        e.preventDefault();
        document.cookie =
          "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.href = "index.html";
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", initAddReviewPage);
