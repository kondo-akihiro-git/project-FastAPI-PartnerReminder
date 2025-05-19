from database.connection import get_connection

def get_all_good_points(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            gp.id,
            gp.meeting_id,
            gp.good_point,
            m.location,
            m.date,
            mp.image_path
        FROM partnergoodpoints gp
        JOIN meetings m ON gp.meeting_id = m.id
        INNER JOIN user_meetings um ON m.id = um.meeting_id
        LEFT JOIN meetingphotos mp ON m.id = mp.meeting_id
        WHERE um.user_id = %s
        ORDER BY gp.id ASC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "meeting_id": row[1],
            "good_point": row[2],
            "location": row[3],
            "date": row[4].isoformat(),
            "image": row[5],
        })

    return {"goodpoints": result}
