# db/queries.py
from database.connection import get_connection

def get_meetings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM meetings")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
