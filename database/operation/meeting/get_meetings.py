from database.connection import get_connection

def get_meetings(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.id, m.title, m.location, m.date, mp.image_path AS meeting_photo
        FROM meetings m
        LEFT JOIN meetingphotos mp ON m.id = mp.meeting_id
        INNER JOIN user_meetings um ON m.id = um.meeting_id
        WHERE um.user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows