CREATE TABLE amenities_locations (
    amenity INT,
    location INT,
    PRIMARY KEY (amenity, location),
    FOREIGN KEY (amenity) REFERENCES (amenities.id),
    FOREIGN KEY (location) REFERENCES (locations.id),
);