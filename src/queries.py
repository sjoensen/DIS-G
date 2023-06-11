from src.db.util import cursor
from src.models import Tag, Station, Line, Location


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
    selected_sorting
):
    min_minutes_to_walk = 0 if min_minutes_to_walk is None else min_minutes_to_walk
    max_minutes_to_walk = 10000 if max_minutes_to_walk is None else max_minutes_to_walk
    min_line_proximity = 0 if min_line_proximity is None else min_line_proximity
    max_line_proximity = 10000 if max_line_proximity is None else max_line_proximity
    sorting = selected_sorting.replace("'", "")
    sorting = sorting.replace("(", "")
    sorting = sorting.replace(")", "")
    split = sorting.split(", ")
    second = "proximity" if split[0] != "proximity" else "minutes_to_walk"
    sorting = f"""{split[0]} {split[1]}, {second} ASC"""
    #TODO: Generalise minutes to walk < 20 to MAX walking time and Minutes_to_walk > 5 to MINIMUM walking time
    sql =\
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
    ) AS S
    WHERE L.minutes_to_walk BETWEEN {min_minutes_to_walk} AND {max_minutes_to_walk} 
    AND S.proximity BETWEEN {min_line_proximity} AND {max_line_proximity} 
    -- WHERE L.minutes_to_walk <= {max_minutes_to_walk}
    -- AND L.minutes_to_walk >= {min_minutes_to_walk}
    ORDER BY {sorting};
    """

    print(sql)
    with cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def test():
    get_tags()


def get_lines():
    return _query_list(Line, "lines")


def get_stations():
    return _query_list(Station, "stations")


def get_locations():
    return _query_list(Location, "locations")


def get_tags():
    return _query_list(Tag, "tags")


def _query_list(constructor, table_name: str):
    with cursor() as cur:
        cur.execute("SELECT * from " + table_name)
        result = [constructor(res) for res in cur.fetchall()] if cur.rowcount > 0 else []
        return result
