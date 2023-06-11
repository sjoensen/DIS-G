from src.db.util import cursor
from src.models import Tag, Station, Line, Location


def _format_list(lst: [str]):
    lst = ",".join(lst)
    lst = lst.replace(",", "','")
    lst = "'" + lst + "'"
    return lst


def get_locations_with_tags(line: str, origin: str, destination: str, tags: [str]):
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
        SELECT SL.station, SL.position, ABS(SL.position - SLOrig.position) AS priority
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
    ORDER BY priority, minutes_to_walk;
    """

    print(sql)
    with cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def test():
    #get_tags()
    get_stations_with_all_tags("F", "Hellerup", "Ny Ellebjerg", ["Toilet", "Groceries", "Pharmacy"])

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
