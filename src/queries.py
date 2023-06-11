import psycopg2
from src.db.util import cursor, commit, rollback
from src.models import Tag, Station, Line, Location, Amenity


def _format_list(lst: [str]):
    lst = ",".join(lst)
    lst = lst.replace(",", "','")
    lst = "'" + lst + "'"
    return lst


def filtered_search(
        line: str,
        origin: str,
        destination: str,
        tags: [str],
        min_minutes_to_walk,
        max_minutes_to_walk,
        min_line_proximity,
        max_line_proximity,
        sorting
):
    sql_origin_search = \
        f"""
            FROM station_lines SLOrig, station_lines SL
                WHERE SL.line = '{line}'
                AND SLOrig.station = '{origin}'
                AND SL.station = '{origin}'
            """

    sql_whole_line_search = \
        f"""
        FROM station_lines SLOrig, station_lines SL
            WHERE SL.line = '{line}'
            AND SLOrig.line = '{line}'
            AND SLOrig.station = '{origin}'
        """

    sql_origin_to_destination_search = \
        f"""
        FROM station_lines SLOrig, station_lines SLDest, station_lines SL
            WHERE SL.line = '{line}'
            AND SLOrig.line = '{line}'
            AND SLDest.line = '{line}'
            AND SLOrig.station = '{origin}'
            AND SLDest.station = '{destination}'
            AND (
                SL.position BETWEEN SLOrig.position AND SLDest.position
                OR SL.position BETWEEN SLDest.position AND SLOrig.position
            )
        """

    sql_search_method = sql_whole_line_search if destination == "destination_all" else sql_origin_to_destination_search
    sql_search_method = sql_origin_search if destination == "destination_none" else sql_search_method

    sql = \
        f"""
        SELECT station, minutes_to_walk, name, address, tag
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
            SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS proximity
            {sql_search_method}
        ) AS S
        WHERE L.minutes_to_walk BETWEEN {min_minutes_to_walk} AND {max_minutes_to_walk} 
        AND S.proximity BETWEEN {min_line_proximity} AND {max_line_proximity} 
        ORDER BY {sorting};
        """

    print(sql)
    with cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


# Didn't manage to make them work in time :(

# def get_stations_with_all_tags(
#         line: str, origin: str, destination: str, tags: [str],
#         min_minutes_to_walk, max_minutes_to_walk,
#         min_line_proximity, max_line_proximity,
#         sorting ):
#     numstr = "AT"+str(len(tags)-1)
#     join_string = "SELECT slstation AS station, " + numstr + ".name, " + numstr + ".tag, "
#     join_string += numstr + ".minutes_to_walk, " + numstr + ".address "
#     join_string += "FROM (SELECT station, minutes_to_walk, name, tag, address FROM locations L "
#     join_string += "NATURAL JOIN (SELECT amenity_id, location_id AS id FROM location_amenities) AS LA "
#     join_string += "NATURAL JOIN (SELECT amenity_id, tag FROM amenity_tags WHERE tag='" + tags[0] + "') AS ATA ) "
#     join_string += "AS AT0 "
#
#     for i in range(1, len(tags)):
#         join_string += " INNER JOIN"
#         join_string += "(SELECT station, minutes_to_walk, name, tag, address FROM locations L "
#         join_string += "NATURAL JOIN (SELECT amenity_id, location_id AS id FROM location_amenities) AS LA "
#         join_string += "NATURAL JOIN (SELECT amenity_id, tag FROM amenity_tags WHERE tag='" + tags[i] + "') AS ATA ) "
#         join_string += "AS AT" + str(i)
#         join_string += " ON AT" + str(i-1) + ".station=AT" + str(i) + ".station "
#
#     rsql = \
#         f"""
#         {join_string}
#         INNER JOIN (
#         SELECT SL.station AS slstation, SL.position, ABS(SL.position - SLOrig.position) AS proximity
#         FROM station_lines SLOrig, station_lines SLDest, station_lines SL
#         WHERE SL.line = '{line}'
#         AND SLOrig.line = '{line}'
#         AND SLDest.line = '{line}'
#         AND SLOrig.station = '{origin}'
#         AND SLDest.station = '{destination}'
#         AND (
#             SL.position BETWEEN SLOrig.position AND SLDest.position
#             OR SL.position BETWEEN SLDest.position AND SLOrig.position
#         )) AS S
#         ON {numstr}.station=S.slstation
#         WHERE(
#         {numstr}.minutes_to_walk BETWEEN {min_minutes_to_walk} AND {max_minutes_to_walk}
#         AND proximity BETWEEN {min_line_proximity} AND {max_line_proximity}
#         )
#         ORDER BY {sorting}
#         """
#     print(rsql)
#     with cursor() as cur:
#         cur.execute(rsql)
#         return(cur.fetchall())



# def find_highest_tag_incidence(
#         line: str, origin: str, destination: str, tags: [str],
#         min_minutes_to_walk, max_minutes_to_walk):
#
#     bsql=\
#     f"""
#     SELECT station, (COUNT(*)) as tag
#     FROM locations L
#     NATURAL JOIN (
#         SELECT amenity_id, location_id AS id
#         FROM location_amenities
#     ) AS LA
#     NATURAL JOIN (
#         SELECT amenity_id, tag
#         FROM amenity_tags
#         WHERE tag = '{tags[0]}'
#     ) AS AT
#     NATURAL JOIN (
#         SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS proximity
#         FROM station_lines SLOrig, station_lines SLDest, station_lines SL
#         WHERE SL.line = '{line}'
#         AND SLOrig.line = '{line}'
#         AND SLDest.line = '{line}'
#         AND SLOrig.station = '{origin}'
#         AND SLDest.station = '{destination}'
#         AND (
#             SL.position BETWEEN SLOrig.position AND SLDest.position
#             OR SL.position BETWEEN SLDest.position AND SLOrig.position
#         )
#     ) AS S
#     WHERE L.minutes_to_walk < {max_minutes_to_walk}
#     AND L.minutes_to_walk > {min_minutes_to_walk}
#     GROUP BY (station, proximity)
#     ORDER BY count(*) DESC, proximity ASC
#     LIMIT 1
#     """
#     print(bsql)
#     with cursor() as cur:
#         cur.execute(bsql)
#         return(cur.fetchall())


def insert_tag(value):
    sql = f"INSERT INTO tags (type) VALUES ('{value}')"
    try:
        with cursor() as cur:
            cur.execute(sql)
        commit()
    except psycopg2.Error as e:
        print(e)
        rollback()


def update_tag(new_type, old_type):
    sql = f"UPDATE tags SET type = '{new_type}' WHERE type = '{old_type}'"
    print(sql)
    try:
        with cursor() as cur:
            cur.execute(sql)
        commit()
    except psycopg2.Error as e:
        print(e)
        rollback()


def delete(table: str, pkey, values):
    sql = f"DELETE FROM {table} WHERE {pkey} IN ({_format_list(values)})"
    try:
        with cursor() as cur:
            cur.execute(sql)
        commit()
    except psycopg2.Error as e:
        rollback()


def get_lines():
    return _query_list(Line, "lines")


def get_stations():
    return _query_list(Station, "stations")


def get_locations():
    return _query_list(Location, "locations")


def get_tags():
    return _query_list(Tag, "tags")


def get_amenities():
    return _query_list(Amenity, "amenities")


def _query_list(constructor, table_name: str):
    with cursor() as cur:
        cur.execute("SELECT * from " + table_name)
        result = [constructor(res) for res in cur.fetchall()] if cur.rowcount > 0 else []
        return result
