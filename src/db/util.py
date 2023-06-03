import os


def connect():
    import psycopg2
    from dotenv import load_dotenv

    load_dotenv()

    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )

    return conn


def reset(connection):
    absolute_path = os.path.dirname(__file__)
    directory = "schema"

    def get_file_string(file_name):
        target = directory + "/" + file_name
        return os.path.join(absolute_path, target)

    conn = connect()
    with conn.cursor() as cur:
        with open(get_file_string("reset.sql")) as file:
            cur.execute(file.read())
        with open(get_file_string("tests.sql")) as file:
            cur.execute(file.read())
    conn.commit()
    conn.close()


def get_secret_key():
    os.getenv('SECRET_KEY')
