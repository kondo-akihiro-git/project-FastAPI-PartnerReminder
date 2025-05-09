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
    cur.execute("""
        SELECT id, title, location, date, my_appearance_image_path 
        FROM meetings 
        WHERE id = %s
    """, (meeting_id,))
    meeting = cur.fetchone()

    if not meeting:
        cur.close()
        conn.close()
        return None

    # 各サブ情報を1つずつ取得（リストではなく単一値）
    def fetch_single(query):
        cur.execute(query, (meeting_id,))
        row = cur.fetchone()
        return row[0] if row else ""

    event_name = fetch_single("SELECT event_name FROM eventnames WHERE meeting_id = %s")
    appearance = fetch_single("SELECT appearance FROM partnerappearances WHERE meeting_id = %s")
    topic = fetch_single("SELECT topic FROM talkedtopics WHERE meeting_id = %s")
    good_point = fetch_single("SELECT good_point FROM partnergoodpoints WHERE meeting_id = %s")
    todo = fetch_single("SELECT todo FROM todofornext WHERE meeting_id = %s")

    cur.close()
    conn.close()

    return {
        "id": meeting[0],
        "title": meeting[1],
        "location": meeting[2],
        "date": meeting[3],
        "my_appearance_image_path": meeting[4],
        "event_names": event_name,
        "partner_appearances": appearance,
        "talked_topics": topic,
        "partner_good_points": good_point,
        "todo_for_next": todo
    }

def update_meeting_data(meeting_id: int, data: dict):

    conn = get_connection()
    cur = conn.cursor()

    # まず対象のMeetingが存在するか確認
    cur.execute("SELECT id FROM meetings WHERE id = %s", (meeting_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return False

    # メインテーブルの更新
    cur.execute("""
        UPDATE meetings
        SET title = %s, location = %s, date = %s
        WHERE id = %s
    """, (data["title"], data["location"], data["date"], meeting_id))

    # ここでは配列関連の処理を削除し、文章を直接登録
    cur.execute("""
        UPDATE eventnames
        SET event_name = %s
        WHERE meeting_id = %s
    """, (data["event_names"], meeting_id))

    cur.execute("""
        UPDATE partnerappearances
        SET appearance = %s
        WHERE meeting_id = %s
    """, (data["partner_appearances"], meeting_id))

    cur.execute("""
        UPDATE talkedtopics
        SET topic = %s
        WHERE meeting_id = %s
    """, (data["talked_topics"], meeting_id))

    cur.execute("""
        UPDATE partnergoodpoints
        SET good_point = %s
        WHERE meeting_id = %s
    """, (data["partner_good_points"], meeting_id))

    cur.execute("""
        UPDATE todofornext
        SET todo = %s
        WHERE meeting_id = %s
    """, (data["todo_for_next"], meeting_id))

    conn.commit()
    cur.close()
    conn.close()
    return True
