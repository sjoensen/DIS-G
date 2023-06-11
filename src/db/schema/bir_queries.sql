INSERT:
- tag
INSERT INTO tags (type)
VALUES {fun(val)};

- stations
INSERT INTO stations (name, area)
VALUES {fun(val)};

- station_lines
INSERT INTO station_lines (station, line, position)
VALUES {fun(val)};

- locations
INSERT INTO locations (id, name, address, station, minutes_to_walk)
VALUES {fun(val)}

- location_amenities
INSERT INTO location_amenities (location_id, amenities_id)
VALUES {fun(val)}

- lines
INSERT INTO lines (name, length)
VALUES {fun(val)}

- amenity_tags
INSERT INTO amenities_tags (amenity_id, tag)
VALUES {fun(val)}

- amenity
INSERT INTO amenities (id, name)
VALUES {fun(val)}

UPDATE:
- tag
UPDATE tags
WHERE tag = {fun(val)};

- stations
UPDATE stations
WHERE {fun(val)};

- station_lines
UPDATE station_lines
WHERE {fun(val)};

- locations
UPDATE locations
WHERE {fun(val)};

- location_amenities
UPDATE location_amenities
WHERE {fun(val)};

- amenity_tags
UPDATE amenity_tags
WHERE {fun(val)};

- amenities
UPDATE amenities
WHERE {fun(val)};

- lines
UPDATE lines
WHERE {fun(val)};


DELETE:
- tag
DELETE FROM tags
WHERE (type = {fun(val)});

- stations
DELETE FROM stations
WHERE {fun(val)};

- station_lines
DELETE FROM station_lines
WHERE {fun(val)};

- locations
DELETE FROM locations
WHERE {fun(val)};

- location_amenities
DELETE FROM location_amenities
WHERE {fun(val)};

- lines
DELETE FROM lines
WHERE {fun(val)};

- amenity_tags
DELETE FROM amenity_tags
WHERE {fun(val)};

- amenities
DELETE FROM amenities
WHERE {fun(val)};


// Selects all toilets with less than 5 minutes walk
SELECT l.station, a.name, l.minutes_to_walk, l.address
FROM locations l JOIN location_amenities la on l.id = la.location_id
JOIN amenities a on la.amenity_id = a.id
WHERE a.name = 'Toilet'
AND l.minutes_to_walk < 5
ORDER BY minutes_to_walk ASC


// Select depending on position, in ascending order from position first, then minutes to walk
SELECT l.station, a.name, l.minutes_to_walk, l.address
FROM locations l JOIN location_amenities la on l.id = la.location_id
JOIN amenities a on la.amenity_id = a.id JOIN station_lines sl on l.station = sl.station
WHERE a.name = 'Toilet'
AND l.minutes_to_walk < 20
AND sl.station < 4
ORDER BY sl.position ASC, l.minutes_to_walk ASC


SELECT l.station, a.name, l.minutes_to_walk, l.address
FROM locations l JOIN location_amenities la on l.id = la.location_id
JOIN amenities a on la.amenity_id = a.id JOIN station_lines sl on l.station = sl.station
JOIN station_lines sl2 on l.station = sl2.station
WHERE a.name = 'Toilet'
AND l.minutes_to_walk < 20
AND sl.position < 4
ORDER BY sl.position ASC, l.minutes_to_walk ASC
--ELSE ORDER BY sl.position DES


    SELECT station, minutes_to_walk, name, address, tag
    FROM locations L
    NATURAL JOIN (
        SELECT amenity_id, location_id AS id
        FROM location_amenities
    ) AS LA
    NATURAL JOIN (
        SELECT amenity_id, tag
        FROM amenity_tags
        WHERE tag = 'Toilet'
        OR tag = 'Coffeeshop'
    ) AS AT
    NATURAL JOIN (
        SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS proximity
        FROM station_lines SLOrig, station_lines SLDest, station_lines SL
        WHERE SL.line = 'F'
        AND SLOrig.line = 'F'
        AND SLDest.line = 'F'
        AND SLOrig.station = 'Hellerup'
        AND SLDest.station = 'Nørrebro'
        AND (
            SL.position BETWEEN SLOrig.position AND SLDest.position
            OR SL.position BETWEEN SLDest.position AND SLOrig.position
        )
    ) AS S
    WHERE L.minutes_to_walk < 1000
    AND L.minutes_to_walk > 0
    ORDER BY proximity ASC, minutes_to_walk ASC;




SELECT station, (COUNT(*)) as count
FROM locations L
NATURAL JOIN (
    SELECT amenity_id, location_id AS id
    FROM location_amenities
) AS LA
NATURAL JOIN (
    SELECT amenity_id, tag
    FROM amenity_tags
    WHERE tag = 'Toilet'
    OR tag = 'Coffeeshop'
) AS AT
NATURAL JOIN (
    SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS proximity
    FROM station_lines SLOrig, station_lines SLDest, station_lines SL
    WHERE SL.line = 'F'
    AND SLOrig.line = 'F'
    AND SLDest.line = 'F'
    AND SLOrig.station = 'Hellerup'
    AND SLDest.station = 'Nørrebro'
    AND (
        SL.position BETWEEN SLOrig.position AND SLDest.position
        OR SL.position BETWEEN SLDest.position AND SLOrig.position
    )
) AS S
WHERE L.minutes_to_walk < 1000
AND L.minutes_to_walk > 0
GROUP BY (station, proximity)
ORDER BY count DESC, proximity ASC
LIMIT 1