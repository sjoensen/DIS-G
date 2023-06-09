CREATE TABLE location_amenities (
    location_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (amenity_id, location_id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);