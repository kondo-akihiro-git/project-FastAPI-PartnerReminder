from database.connection import get_connection


def create_meeting_data(data: dict, user_id: int):
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

        # user_meetings に紐付け追加
        cur.execute("""
            INSERT INTO user_meetings (user_id, meeting_id) VALUES (%s, %s)
        """, (user_id, meeting_id))

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

        cur.execute("""
            INSERT INTO myappearances (meeting_id, image_path)
            VALUES (%s, %s)
        """, (meeting_id, data.get("my_appearance_image_path", "")))

        cur.execute("""
            INSERT INTO meetingphotos (meeting_id, image_path)
            VALUES (%s, %s)
        """, (meeting_id, data.get("meeting_photo", "")))

        conn.commit()
        return meeting_id

    except Exception as e:
        print("DB Insert Error:", e)
        conn.rollback()
        return None

    finally:
        cur.close()
        conn.close()