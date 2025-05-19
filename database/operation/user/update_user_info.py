
from database.connection import get_connection

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
