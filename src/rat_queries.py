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

def get_stations_with_all_tags(line: str, origin: str, destination: str, tags: [str]):
    numstr = str(len(tags)-1)
    join_string = "SELECT slstation AS station, AT" + numstr + ".name, AT" + numstr + ".tag, "
    join_string += "AT" + numstr + ".minutes_to_walk, AT" + numstr + ".address "
    join_string += "FROM (SELECT station, minutes_to_walk, name, tag, address FROM locations L "
    join_string += "NATURAL JOIN (SELECT amenity_id, location_id AS id FROM location_amenities) AS LA "
    join_string += "NATURAL JOIN (SELECT amenity_id, tag FROM amenity_tags WHERE tag='" + tags[0] + "') AS ATA ) "
    join_string += "AS AT0 "

    for i in range(1, len(tags)):
        join_string += " INNER JOIN"
        join_string += "(SELECT station, minutes_to_walk, name, tag, address FROM locations L "
        join_string += "NATURAL JOIN (SELECT amenity_id, location_id AS id FROM location_amenities) AS LA "
        join_string += "NATURAL JOIN (SELECT amenity_id, tag FROM amenity_tags WHERE tag='" + tags[i] + "') AS ATA ) "
        join_string += "AS AT" + str(i)
        join_string += " ON AT" + str(i-1) + ".station=AT" + str(i) + ".station "

    rsql = \
        f"""
        {join_string}
        INNER JOIN (
        SELECT SL.station AS slstation, SL.position, ABS(SL.position - SLOrig.position) AS priority
        FROM station_lines SLOrig, station_lines SLDest, station_lines SL
        WHERE SL.line = '{line}'
        AND SLOrig.line = '{line}'
        AND SLDest.line = '{line}'
        AND SLOrig.station = '{origin}'
        AND SLDest.station = '{destination}'
        AND (
            SL.position BETWEEN SLOrig.position AND SLDest.position
            OR SL.position BETWEEN SLDest.position AND SLOrig.position
        )) AS S
        ON AT{str(len(tags)-1)}.station=S.slstation
        ORDER BY priority, AT{str(len(tags)-1)}.minutes_to_walk;
        """

    print(rsql)
    with cursor() as cur:
        cur.execute(rsql)
        print(cur.fetchall())