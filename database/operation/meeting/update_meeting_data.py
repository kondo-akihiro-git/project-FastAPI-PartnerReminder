from database.connection import get_connection

def update_meeting_data(meeting_id: int, data: dict, user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # 所有権チェック
    cur.execute("""
        SELECT m.id
        FROM meetings m
        INNER JOIN user_meetings um ON m.id = um.meeting_id
        WHERE m.id = %s AND um.user_id = %s
    """, (meeting_id, user_id))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return False

    # 更新処理はこれまで通り
    cur.execute("""
        UPDATE meetings SET title = %s, location = %s, date = %s WHERE id = %s
    """, (data["title"], data["location"], data["date"], meeting_id))

    cur.execute("""
        UPDATE eventnames SET event_name = %s WHERE meeting_id = %s
    """, (data["event_names"], meeting_id))

    cur.execute("""
        UPDATE partnerappearances SET appearance = %s WHERE meeting_id = %s
    """, (data["partner_appearances"], meeting_id))

    cur.execute("""
        UPDATE talkedtopics SET topic = %s WHERE meeting_id = %s
    """, (data["talked_topics"], meeting_id))

    cur.execute("""
        UPDATE partnergoodpoints SET good_point = %s WHERE meeting_id = %s
    """, (data["partner_good_points"], meeting_id))

    cur.execute("""
        UPDATE todofornext SET todo = %s WHERE meeting_id = %s
    """, (data["todo_for_next"], meeting_id))

    cur.execute("""
        UPDATE myappearances SET image_path = %s WHERE meeting_id = %s
    """, (data["my_appearance_image_path"], meeting_id))

    cur.execute("""
        UPDATE meetingphotos SET image_path = %s WHERE meeting_id = %s
    """, (data["meeting_photo"], meeting_id))

    conn.commit()
    cur.close()
    conn.close()
    return True

