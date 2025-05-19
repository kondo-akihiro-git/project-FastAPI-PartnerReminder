
from database.connection import get_connection

def update_next_event_day(new_date: str, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM NextEventDay WHERE user_id = %s LIMIT 1", (user_id,))
    row = cur.fetchone()

    if row:
        cur.execute("UPDATE NextEventDay SET date = %s WHERE id = %s", (new_date, row[0]))
    else:
        cur.execute("INSERT INTO NextEventDay (user_id, date) VALUES (%s, %s)", (user_id, new_date))
    
    conn.commit()
    cur.close()
    conn.close()
    return True