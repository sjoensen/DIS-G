from src.db.util import cursor
from src.models import Tag, Station, Line, Location


def get_locations_with_tags(line: str, origin: str, destination: str, tags: [str]):
    sql =\
    f"""
    SELECT type FROM tags
    WHERE type IN {tuple(tags)}
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
