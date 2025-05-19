from database.connection import get_connection


def get_next_event_day(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT date FROM NextEventDay WHERE user_id = %s ORDER BY date ASC LIMIT 1;", (user_id,))
            row = cur.fetchone()
            return {"date": row[0]} if row else None
    finally:
        conn.close()
