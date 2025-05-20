from database.connection import get_connection

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