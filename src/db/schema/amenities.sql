CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    address VARCHAR,
    name VARCHAR,
    minutes_to_reach INT,
    station VARCHAR,
    CONSTRAINT fk_station FOREIGN KEY(station) REFERENCES stations(name)
);