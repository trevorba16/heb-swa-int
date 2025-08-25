-- SQL to initialize the database for the DSR project
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add more tables as needed
