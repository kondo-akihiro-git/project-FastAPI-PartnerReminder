import jwt
from datetime import datetime, timedelta
from database.connection import get_connection
import bcrypt

# def get_meetings():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT m.id, m.title, m.location, m.date, mp.image_path AS meeting_photo
#         FROM meetings m
#         LEFT JOIN meetingphotos mp ON m.id = mp.meeting_id
#     """)
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows

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

def get_meeting_details(meeting_id):
    conn = get_connection()
    cur = conn.cursor()

    # メインのデート情報、外見画像パス、デート写真パスを一度に取得
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
        WHERE m.id = %s
    """, (meeting_id,))
    
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

    cur.execute("""
        UPDATE myappearances
        SET image_path = %s
        WHERE meeting_id = %s
    """, (data["my_appearance_image_path"], meeting_id))

    cur.execute("""
        UPDATE meetingphotos
        SET image_path = %s
        WHERE meeting_id = %s
    """, (data["meeting_photo"], meeting_id))

    conn.commit()
    cur.close()
    conn.close()
    return True

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


def delete_meetings_by_ids(ids: list[int], user_id: int) -> int:
    if not ids:
        return 0

    conn = get_connection()
    cur = conn.cursor()
    try:
        # user_id所有のmeeting_idのみ削除
        cur.execute("""
            DELETE FROM meetings m
            USING user_meetings um
            WHERE m.id = um.meeting_id
            AND um.user_id = %s
            AND m.id = ANY(%s)
        """, (user_id, ids))
        deleted_count = cur.rowcount
        conn.commit()
        return deleted_count
    except Exception as e:
        print("DB Delete Error:", e)
        conn.rollback()
        return 0
    finally:
        cur.close()
        conn.close()

def get_all_good_points():
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
        LEFT JOIN meetingphotos mp ON m.id = mp.meeting_id
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
            "image": row[5],
        })

    return {"goodpoints": result}

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

def create_user(name, phone, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute(
            "INSERT INTO Users (name, phone, email, password_hash) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, phone, email, hashed_pw)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        print("ユーザー作成エラー:", e)
        return None
    finally:
        cur.close()
        conn.close()

def authenticate_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, password_hash FROM Users WHERE email=%s", (email,))
        result = cur.fetchone()
        if result and bcrypt.checkpw(password.encode(), result[1].encode()):
            return result[0]
        return None
    finally:
        cur.close()
        conn.close()

def user_exists(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def update_user_info(user_id: int, name: str,phone: str, hashed_password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    # ユーザー存在チェック
    cur.execute("SELECT id FROM Users WHERE id = %s", (user_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return False

    try:
        cur.execute("""
            UPDATE Users
            SET name = %s, password_hash = %s, phone = %s
            WHERE id = %s
        """, (name, hashed_password, phone, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ユーザー更新エラー: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "name": user[1],
            "phone": user[2],
            "email": user[3]
        }
    return None



def get_next_event_day():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT date FROM NextEventDay ORDER BY date ASC LIMIT 1;")
            row = cur.fetchone()
            return {"date": row[0]} if row else None
    finally:
        conn.close()

def update_next_event_day(new_date: str):
    conn = get_connection()
    cur = conn.cursor()

    # NextEventDay テーブルにレコードが存在するか確認
    cur.execute("SELECT id FROM NextEventDay LIMIT 1")
    row = cur.fetchone()

    if row:
        # 存在すれば更新
        cur.execute("UPDATE NextEventDay SET date = %s WHERE id = %s", (new_date, row[0]))
    else:
        # 存在しなければ挿入
        cur.execute("INSERT INTO NextEventDay (date) VALUES (%s)", (new_date,))
    
    conn.commit()
    cur.close()
    conn.close()
    return True



# JWTのシークレットとアルゴリズム（環境変数にした方が良い）
JWT_SECRET = "your_secret_key"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1時間

def create_jwt_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
