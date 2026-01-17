import sqlite3

def fetch_record(table):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    return cur.fetchone()
