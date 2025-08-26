CREATE TABLE IF NOT EXISTS band (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    formed_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS instrument (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS musician (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INTEGER NOT NULL,
    band_id INTEGER REFERENCES band(id) ON DELETE SET NULL,
    instrument_id INTEGER REFERENCES instrument(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO instrument (name, type, created_at) VALUES
    ('Guitar', 'String', '2023-01-01 10:00:00'),
    ('Drums', 'Percussion', '2023-01-02 11:00:00'),
    ('Bass', 'String', '2023-01-03 12:00:00'),
    ('Keyboard', 'Keyboard', '2023-01-04 13:00:00'),
    ('Violin', 'String', '2023-01-05 14:00:00'),
    ('Trumpet', 'Brass', '2023-01-06 15:00:00'),
    ('Saxophone', 'Woodwind', '2023-01-07 16:00:00'),
    ('Flute', 'Woodwind', '2023-01-08 17:00:00'),
    ('Cello', 'String', '2023-01-09 18:00:00'),
    ('Harp', 'String', '2023-01-10 19:00:00');

INSERT INTO band (name, genre, formed_year, created_at) VALUES
    ('The Rockers', 'Rock', 2000, '2023-01-01 10:00:00'),
    ('Jazz Masters', 'Jazz', 1995, '2023-01-02 11:00:00'),
    ('Pop Stars', 'Pop', 2010, '2023-01-03 12:00:00'),
    ('Classic Ensemble', 'Classical', 1980, '2023-01-04 13:00:00'),
    ('Metal Heads', 'Metal', 2005, '2023-01-05 14:00:00'),
    ('Blues Crew', 'Blues', 1998, '2023-01-06 15:00:00'),
    ('Country Roads', 'Country', 2003, '2023-01-07 16:00:00'),
    ('Indie Vibes', 'Indie', 2012, '2023-01-08 17:00:00'),
    ('Reggae Roots', 'Reggae', 1992, '2023-01-09 18:00:00'),
    ('Electro Beats', 'Electronic', 2015, '2023-01-10 19:00:00');

INSERT INTO musician (name, birth_year, band_id, instrument_id, created_at) VALUES
    ('Alice Johnson', 1985, 1, 1, '2023-01-01 10:00:00');