-- Ensure you're connected to the default database (postgres) or another existing database
-- \connect postgres;

-- Create the database if it doesn't already exist (Manual step or handled programmatically)
CREATE DATABASE hbnb_dev;

-- Connect to the newly created database
\c hbnb_dev;

-- Create the necessary tables

CREATE TABLE IF NOT EXISTS country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS city (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (country_code) REFERENCES country (code)
);

CREATE TABLE IF NOT EXISTS amenity (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS place (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    address VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    host_id VARCHAR(36) NOT NULL,
    city_id VARCHAR(36) NOT NULL,
    price_per_night INTEGER NOT NULL,
    number_of_rooms INTEGER NOT NULL,
    number_of_bathrooms INTEGER NOT NULL,
    max_guests INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES "user"(id),
    FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE IF NOT EXISTS review (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    comment VARCHAR(255) NOT NULL,
    rating FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
