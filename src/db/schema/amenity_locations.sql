CREATE TABLE amenity_locations (
    amenity_id INT,
    location_id INT,
    PRIMARY KEY (amenity_id, location_id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);