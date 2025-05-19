import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

# 既存テーブル削除と再作成
with open(os.path.join(os.path.dirname(__file__), "create_testdata_v7.sql"), "r", encoding="utf-8") as f:

    sql = f.read()
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()
print("✅ テーブル作成完了")
