import os
import pandas as pd
import psycopg2
import numpy as np
from dotenv import load_dotenv
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.extras import RealDictCursor

CSV_SEPARATOR = ','

# [ filename ]
SCHEMA_FILES = [
    "drop_db",
    "lines",
    "stations",
    "station_lines",
    "locations",
    "amenities",
    "tags",
    "amenity_tags",
    "location_amenities",
]

# [ filename, [ column_names ] ]
CSV_FILES = [
    ("lines", ["name", "length"]),
    ("stations", ["name", "area"]),
    ("locations", ["id", "name", "address", "station", "minutes_to_walk"]),
    ("station_lines", ["station", "line", "position"]),
    ("amenities", ["id", "name"]),
    ("tags", ["type"]),
    ("location_amenities", ["amenity_id", "location_id"]),
    ("amenity_tags", ["amenity_id", "tag"]),
]

SETUP_SCRIPTS = [
    "set_identities"
]


ABSOLUTE_PATH = os.path.dirname(__file__)
SCHEMA_DIRECTORY = "schema"
DATA_DIRECTORY = "data"


_connection = None


def _get_connection():
    if _connection is not None:
        return _connection
    else:
        load_dotenv()

        conn = psycopg2.connect(
            host="localhost",
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )

        return conn


def cursor():
    return _get_connection().cursor(cursor_factory=RealDictCursor)


def commit():
    _get_connection().commit()


def reset() -> None:
    _register_adapters()

    with cursor() as cur:
        for name in SCHEMA_FILES:
            with open(_get_schema_file_string(name + ".sql")) as file:
                cur.execute(file.read())

        for csv in CSV_FILES:
            data = list(
                map(lambda x: tuple(x),
                    pd.read_csv(_get_data_file_string(csv[0] + ".csv"), sep=CSV_SEPARATOR)[csv[1]].to_records(index=False))
            )
            args_str = ','.join(cur.mogrify(_get_csv_symbols(len(csv[1])), d).decode('utf-8') for d in data)
            cur.execute("INSERT INTO " + csv[0] + " (" + (','.join(map(str, csv[1]))) + ") VALUES " + args_str)

        for name in SETUP_SCRIPTS:
            with open(_get_schema_file_string(name + ".sql")) as file:
                cur.execute(file.read())

    commit()


def get_secret_key() -> str:
    return os.getenv('SECRET_KEY')


def _get_schema_file_string(file_name: str) -> str:
    target = SCHEMA_DIRECTORY + "/" + file_name
    return os.path.join(ABSOLUTE_PATH, target)


def _get_data_file_string(file_name: str) -> str:
    target = DATA_DIRECTORY + "/" + file_name
    return os.path.join(ABSOLUTE_PATH, target)


def _get_csv_symbols(n: int) -> str:
    res = "("
    for _ in range(n):
        res += "%s, "
    return (res[:-2]) + ")"


def _adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def _adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


def _register_adapters() -> None:
    register_adapter(np.float64, _adapt_numpy_float64)
    register_adapter(np.int64, _adapt_numpy_int64)