SELECT setval(pg_get_serial_sequence('amenities', 'id'), coalesce(MAX(id), 1))
from amenities;
SELECT setval(pg_get_serial_sequence('locations', 'id'), coalesce(MAX(id), 1))
from locations;