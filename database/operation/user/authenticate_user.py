from database.connection import get_connection
import bcrypt

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