from database.connection import get_connection

def get_meeting_details(meeting_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            m.id, m.title, m.location, m.date, 
            ma.image_path AS my_appearance_image_path, 
            mp.image_path AS meeting_photo,
            en.event_name, pa.appearance, tt.topic, gp.good_point, tn.todo
        FROM meetings m
        LEFT JOIN myappearances ma ON ma.meeting_id = m.id
        LEFT JOIN meetingphotos mp ON mp.meeting_id = m.id
        LEFT JOIN eventnames en ON en.meeting_id = m.id
        LEFT JOIN partnerappearances pa ON pa.meeting_id = m.id
        LEFT JOIN talkedtopics tt ON tt.meeting_id = m.id
        LEFT JOIN partnergoodpoints gp ON gp.meeting_id = m.id
        LEFT JOIN todofornext tn ON tn.meeting_id = m.id
        INNER JOIN user_meetings um ON m.id = um.meeting_id
        WHERE m.id = %s AND um.user_id = %s
    """, (meeting_id, user_id))
    
    meeting = cur.fetchone()

    if not meeting:
        cur.close()
        conn.close()
        return None

    cur.close()
    conn.close()

    return {
        "id": meeting[0],
        "title": meeting[1],
        "location": meeting[2],
        "date": meeting[3],
        "my_appearance_image_path": meeting[4],
        "meeting_photo": meeting[5],
        "event_names": meeting[6],
        "partner_appearances": meeting[7],
        "talked_topics": meeting[8],
        "partner_good_points": meeting[9],
        "todo_for_next": meeting[10]
    }