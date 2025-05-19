from database.connection import get_connection
import bcrypt

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
