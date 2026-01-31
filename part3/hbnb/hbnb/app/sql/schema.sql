
DROP DATABASE IF EXISTS hbnb_dev_db;

-- Create database
CREATE DATABASE hbnb_dev_db;
USE hbnb_dev_db;

-- ======================
-- USERS
-- ======================
CREATE TABLE users (
    id VARCHAR(60) PRIMARY KEY,
    email VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- ======================
-- PLACES
-- ======================
CREATE TABLE places (
    id VARCHAR(60) PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description VARCHAR(1024),
    price INT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ======================
-- AMENITIES
-- ======================
CREATE TABLE amenities (
    id VARCHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- ======================
-- REVIEWS
-- ======================
CREATE TABLE reviews (
    id VARCHAR(60) PRIMARY KEY,
    text VARCHAR(1024) NOT NULL,
    rating INT NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ======================
-- PLACE_AMENITY (Many-to-Many)
-- ======================
CREATE TABLE place_amenity (
    place_id VARCHAR(60) NOT NULL,
    amenity_id VARCHAR(60) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
