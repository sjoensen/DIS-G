from src.db import util


def test():
    get_tags()


def get_stations():
    conn = util.connect()
    curr = conn.cursor()
    # curr.execute("SELECT * from stations")
    curr.execute("SELECT * from stations WHERE NOT name = 'Vigerslev Allé'")
    result = curr.fetchall()
    print(result)
    conn.close()


def get_tags():
    conn = util.connect()
    curr = conn.cursor()
    # curr.execute("SELECT * from stations")
    curr.execute("SELECT * from tags")
    result = curr.fetchall()
    print(result)
    conn.close()

