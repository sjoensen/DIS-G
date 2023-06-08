CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    address VARCHAR,
    station VARCHAR,
    minutes_to_walk INT,
    FOREIGN KEY (station) REFERENCES stations(name)
);