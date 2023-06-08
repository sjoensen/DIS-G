CREATE TABLE amenity_tags (
    amenity_id INT,
    tag VARCHAR,
    PRIMARY KEY (amenity_id, tag),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id),
    FOREIGN KEY (tag) REFERENCES tags(type)
)
