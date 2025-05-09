from database.connection import get_connection

def get_meetings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM meetings")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_meeting_details(meeting_id):
    conn = get_connection()
    cur = conn.cursor()

    # メインのデート情報
    cur.execute("SELECT id, title, location, date, my_appearance_image_path FROM meetings WHERE id = %s", (meeting_id,))
    meeting = cur.fetchone()

    if not meeting:
        cur.close()
        conn.close()
        return None  # 該当デートが存在しない場合

    # サブ情報をまとめて取得
    def fetch_list(query):
        cur.execute(query, (meeting_id,))
        return [row[0] for row in cur.fetchall()]

    event_names = fetch_list("SELECT event_name FROM eventnames WHERE meeting_id = %s")
    appearances = fetch_list("SELECT appearance FROM partnerappearances WHERE meeting_id = %s")
    topics = fetch_list("SELECT topic FROM talkedtopics WHERE meeting_id = %s")
    good_points = fetch_list("SELECT good_point FROM partnergoodpoints WHERE meeting_id = %s")
    todos = fetch_list("SELECT todo FROM todofornext WHERE meeting_id = %s")

    cur.close()
    conn.close()

    return {
        "id": meeting[0],
        "title": meeting[1],
        "location": meeting[2],
        "date": meeting[3],
        "my_appearance_image_path": meeting[4],
        "event_names": event_names,
        "partner_appearances": appearances,
        "talked_topics": topics,
        "partner_good_points": good_points,
        "todo_for_next": todos
    }