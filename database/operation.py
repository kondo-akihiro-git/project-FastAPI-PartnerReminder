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

    # メインのデート情報と外見画像パスを取得
    cur.execute("""
        SELECT m.id, m.title, m.location, m.date, ma.image_path 
        FROM meetings m
        LEFT JOIN myappearances ma ON ma.meeting_id = m.id
        WHERE m.id = %s
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

    # 画像パスの更新（もし提供されていれば）
    if "my_appearance_image_path" in data:
        # MyAppearancesテーブルに画像パスを更新（または新規挿入）
        cur.execute("""
            INSERT INTO myappearances (meeting_id, image_path)
            VALUES (%s, %s)
            ON CONFLICT (meeting_id) 
            DO UPDATE SET image_path = EXCLUDED.image_path
        """, (meeting_id, data["my_appearance_image_path"]))

    conn.commit()
    cur.close()
    conn.close()
    return True

def create_meeting_data(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # メインテーブルに挿入
        cur.execute("""
            INSERT INTO meetings (title, location, date)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (data["title"], data["location"], data["date"]))
        meeting_id = cur.fetchone()[0]

        # サブ情報の挿入（各テーブルに対応）
        cur.execute("""
            INSERT INTO eventnames (meeting_id, event_name)
            VALUES (%s, %s)
        """, (meeting_id, data.get("event_names", "")))

        cur.execute("""
            INSERT INTO partnerappearances (meeting_id, appearance)
            VALUES (%s, %s)
        """, (meeting_id, data.get("partner_appearances", "")))

        cur.execute("""
            INSERT INTO talkedtopics (meeting_id, topic)
            VALUES (%s, %s)
        """, (meeting_id, data.get("talked_topics", "")))

        cur.execute("""
            INSERT INTO partnergoodpoints (meeting_id, good_point)
            VALUES (%s, %s)
        """, (meeting_id, data.get("partner_good_points", "")))

        cur.execute("""
            INSERT INTO todofornext (meeting_id, todo)
            VALUES (%s, %s)
        """, (meeting_id, data.get("todo_for_next", "")))

        # 画像パス（任意）
        if "my_appearance_image_path" in data:
            cur.execute("""
                INSERT INTO myappearances (meeting_id, image_path)
                VALUES (%s, %s)
            """, (meeting_id, data["my_appearance_image_path"]))

        conn.commit()
        return meeting_id

    except Exception as e:
        print("DB Insert Error:", e)
        conn.rollback()
        return None

    finally:
        cur.close()
        conn.close()

def delete_meetings_by_ids(ids: list[int]) -> int:
    if not ids:
        return 0

    conn = get_connection()
    cur = conn.cursor()
    try:
        # SQL IN 句で一括削除
        query = "DELETE FROM meetings WHERE id = ANY(%s);"
        cur.execute(query, (ids,))
        deleted_count = cur.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"削除中にエラーが発生しました: {e}")
        deleted_count = 0
    finally:
        cur.close()
        conn.close()

    return deleted_count


def get_all_good_points():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT gp.id, gp.meeting_id, gp.good_point, m.location, m.date
        FROM partnergoodpoints gp
        JOIN meetings m ON gp.meeting_id = m.id
        ORDER BY gp.id ASC
    """)

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
        })

    return {"goodpoints": result}
