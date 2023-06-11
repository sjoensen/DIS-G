def get_line_locations_with_tags(line: str, origin: str, distance: int, tags: [str]):
    sql =\
    f"""
    SELECT station
    FROM locations L
    NATURAL JOIN (
        SELECT amenity_id, location_id AS id
        FROM location_amenities
    ) AS LA
    NATURAL JOIN (
        SELECT amenity_id, tag
        FROM amenity_tags
        WHERE tag IN ({_format_list(tags)})
    ) AS AT
    NATURAL JOIN (
        SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS priority
        FROM station_lines SLOrig, station_lines SL
        WHERE SL.line = '{line}'
        AND SLOrig.line = '{line}'
        AND SLOrig.station = '{origin}'
    ) AS S
    WHERE priority <= '{distance}'
    ORDER BY priority, minutes_to_walk;
    """

    print(sql)
    with cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()