import logging
from database.connection import get_connection
import bcrypt


logging.basicConfig(level=logging.INFO)


# def authenticate_user(email, password):
#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT id, password_hash FROM Users WHERE email=%s", (email,))
#         result = cur.fetchone()
#         if result and bcrypt.checkpw(password.encode(), result[1].encode()):
#             return result[0]
#         return None
#     finally:
#         cur.close()
#         conn.close()


def authenticate_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        logging.info(f"ユーザー認証開始: email={email}")
        cur.execute("SELECT id, password_hash FROM Users WHERE email=%s", (email,))
        result = cur.fetchone()

        if result:
            user_id, password_hash = result
            logging.info(f"ユーザー見つかりました: user_id={user_id}")
            if bcrypt.checkpw(password.encode(), password_hash.encode()):
                logging.info("パスワード一致")
                return user_id
            else:
                logging.warning("パスワード不一致")
        else:
            logging.warning("ユーザーが見つかりません")
        return None
    finally:
        cur.close()
        conn.close()