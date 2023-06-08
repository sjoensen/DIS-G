CREATE TABLE amenity_tags (
    amenity_id INT,
    tag VARCHAR,
    CONSTRAINT pk_amenity_tag PRIMARY KEY (amenity_id, tag),
    CONSTRAINT fk_amenity FOREIGN KEY (amenity_id) REFERENCES amenities(id),
    CONSTRAINT fk_tag FOREIGN KEY (tag) REFERENCES tags(type)
)
