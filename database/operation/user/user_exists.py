from database.connection import get_connection

def user_exists(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None