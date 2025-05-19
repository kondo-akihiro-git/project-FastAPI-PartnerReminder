from database.connection import get_connection

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
