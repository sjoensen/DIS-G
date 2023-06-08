CREATE TABLE locations (
    address VARCHAR PRIMARY KEY,
    station VARCHAR,
    minutes_to_walk INT,
    FOREIGN KEY (station) REFERENCES stations(name)
);