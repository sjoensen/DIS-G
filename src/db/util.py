import os
import pandas as pd
import psycopg2
import numpy as np
from dotenv import load_dotenv
from psycopg2.extensions import register_adapter, AsIs

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
    "amenity_locations"
]

# [ filename, [ column_names ] ]
CSV_FILES = [
    ("lines", ["name", "length"]),
    ("stations", ["name", "area"]),
    ("locations", ["id", "name", "address", "station", "minutes_to_walk"]),
    # ("station_lines", ["station", "line", "position"]),
    # ("station_lines", ["station", "line", "position"]),
    # ("tags", ["type"])
]

SETUP_SCRIPTS = [
    "set_identities"
]


ABSOLUTE_PATH = os.path.dirname(__file__)
SCHEMA_DIRECTORY = "schema"
DATA_DIRECTORY = "data"


def connect():
    load_dotenv()

    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )

    return conn


def reset() -> None:
    _register_adapters()

    conn = connect()

    with conn.cursor() as cur:
        for name in SCHEMA_FILES:
            with open(_get_schema_file_string(name + ".sql")) as file:
                cur.execute(file.read())

    with conn.cursor() as cur:
        for csv in CSV_FILES:
            data = list(
                map(lambda x: tuple(x),
                    pd.read_csv(_get_data_file_string(csv[0] + ".csv"), sep=CSV_SEPARATOR)[csv[1]].to_records(index=False))
            )
            args_str = ','.join(cur.mogrify(_get_csv_symbols(len(csv[1])), d).decode('utf-8') for d in data)
            cur.execute("INSERT INTO " + csv[0] + " (" + (','.join(map(str, csv[1]))) + ") VALUES " + args_str)

    with conn.cursor() as cur:
        for name in SETUP_SCRIPTS:
            with open(_get_schema_file_string(name + ".sql")) as file:
                cur.execute(file.read())

    conn.cursor().execute("INSERT INTO locations (address,station,name,minutes_to_walk) VALUES ('Philip Heymans Alle 17 2900 Hellerup','Hellerup','Waterfront Shopping Center',14)")
    conn.commit()
    conn.close()


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