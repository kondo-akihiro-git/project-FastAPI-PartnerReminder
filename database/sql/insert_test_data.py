import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

# backendから実行コマンド ： python database/sql/insert_test_data.py 

# .env読み込み
load_dotenv()

# DB接続
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

# パスワード「test」のハッシュ化
password = "test"
hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 全削除SQL
delete_sql = """
DELETE FROM Users;
DELETE FROM TodoForNext;
DELETE FROM PartnerGoodPoints;
DELETE FROM TalkedTopics;
DELETE FROM PartnerAppearances;
DELETE FROM EventNames;
DELETE FROM MyAppearances;
DELETE FROM MeetingPhotos;
DELETE FROM Meetings;
DELETE FROM NextEventDay;
"""

# 実行
cur.execute(delete_sql)

# Meetings 挿入
cur.execute("""
INSERT INTO Meetings (title, location, date) VALUES
('水族館デート', '品川水族館', '2024-04-15'),
('カフェでまったり', '代官山カフェ', '2024-04-22'),
('映画とディナー', '渋谷', '2024-04-29'),
('TEST', '新宿御苑', '2024-05-01'),
('ドライブデート', '箱根', '2024-05-04'),
('ランチと公園', '代々木公園', '2024-05-07'),
('TEST', '浅草寺', '2024-05-09'),
('博物館めぐり', '上野', '2024-05-12'),
('夜景とディナー', 'お台場', '2024-05-15'),
('美術館と読書の話', '六本木', '2024-05-18'),
('川沿い散歩', '中目黒', '2024-05-21'),
('夜のイルミネーション', '表参道', '2024-05-25');
""")

# 以下、各種 INSERT を順番にまとめて実行（順番注意）

# MyAppearances
cur.execute("""
INSERT INTO MyAppearances (meeting_id, image_path) VALUES
(1, ''),
(2, 'files/uploaded_images/hand-886420_1280.jpg'),
(3, 'files/uploaded_images/shoe-2313143_1280.jpg'),
(4, 'files/uploaded_images/zip-1268656_1280.jpg'),
(5, 'files/uploaded_images/oxford-shoes-6078993_1280.jpg'),
(6, 'files/uploaded_images/ties-56107_1280.jpg'),
(7, 'files/uploaded_images/shirts-591750_1280.jpg'),
(8, 'files/uploaded_images/clothes-1846128_1280.jpg'),
(9, 'files/uploaded_images/jeans-2551188_1280.jpg'),
(10, 'files/uploaded_images/neckties-210451_1280.jpg'),
(11, 'files/uploaded_images/necktie-1284463_1280.jpg'),
(12, 'files/uploaded_images/shirts-591756_1280.jpg');
""")

# MeetingPhotos
cur.execute("""
INSERT INTO MeetingPhotos (meeting_id, image_path) VALUES
(1, ''),
(2, 'files/uploaded_images/bridge-7779222_1280.jpg'),
(3, 'files/uploaded_images/gallery-3114279_1280.jpg'),
(4, 'files/uploaded_images/art-3802145_1280.jpg'),
(5, 'files/uploaded_images/forget-me-not-5143015_1280.jpg'),
(6, 'files/uploaded_images/herbstastern-5938056_1280.jpg'),
(7, 'files/uploaded_images/road-6881040_1280.jpg'),
(8, 'files/uploaded_images/student-1258137_1280.jpg'),
(9, 'files/uploaded_images/gallery-2901718_1280.jpg'),
(10, 'files/uploaded_images/city-7492749_1280.jpg'),
(11, 'files/uploaded_images/gallery-1570804_1280.jpg'),
(12, 'files/uploaded_images/summer-783347_1280.jpg');
""")

# EventNames
cur.execute("""
INSERT INTO EventNames (meeting_id, event_name) VALUES
(1, E'水族館\nランチ'),
(2, 'カフェ'),
(3, E'映画鑑賞\nイタリアンディナー'),
(4, ''),
(5, E'ドライブ\nランチ'),
(6, E'ピクニック\n公園散歩'),
(7, ''),
(8, '博物館巡り'),
(9, E'夜景鑑賞\nディナー'),
(10, E'美術館鑑賞\n読書の話'),
(11, '川沿いの散歩'),
(12, E'イルミネーション\n写真撮影');
""")

# PartnerAppearances
cur.execute("""
INSERT INTO PartnerAppearances (meeting_id, appearance) VALUES
(1, E'ロングヘア\n白いワンピース'),
(2, ''),
(3, E'眼鏡\nカジュアルな服装'),
(4, ''),
(5, E'カジュアルな服装\n明るい笑顔'),
(6, E'明るい笑顔\nカジュアルな服装'),
(7, ''),
(8, ''),
(9, E'ドレッシーな服\n笑顔が素敵'),
(10, E'シンプルな服装\n落ち着いた雰囲気'),
(11, E'ポニーテール\nワンピース'),
(12, E'ニット帽\nロングコート');
""")

# TalkedTopics
cur.execute("""
INSERT INTO TalkedTopics (meeting_id, topic) VALUES
(1, E'海の生き物の話\n旅行の計画'),
(2, E'最近読んだ本\n好きな作家'),
(3, E'映画の感想\nおすすめの映画'),
(4, ''),
(5, E'家族の話\n将来の計画'),
(6, E'趣味のカメラ\nおすすめの撮影地'),
(7, ''),
(8, ''),
(9, ''),
(10, E'アートの話\n美術館の展示'),
(11, ''),
(12, E'夜景スポットの話\n写真撮影のコツ');
""")

# PartnerGoodPoints
cur.execute("""
INSERT INTO PartnerGoodPoints (meeting_id, good_point) VALUES
(1, E'優しい話し方\n気配りが素晴らしい'),
(2, E'笑顔が素敵\n話が面白い'),
(3, E'映画のセンスが良い\n気配りが上手'),
(4, ''),
(5, E'ドライブ中の会話が楽しい\nリラックスできる雰囲気'),
(6, ''),
(7, ''),
(8, ''),
(9, E'気配り上手\n笑顔が素敵'),
(10, ''),
(11, E'話しやすい\n自然体でいられる'),
(12, '');
""")

# TodoForNext
cur.execute("""
INSERT INTO TodoForNext (meeting_id, todo) VALUES
(1, E'次は動物園に行く予定\nランチの場所を決める'),
(2, ''),
(3, E'映画館を予約する\nディナーの予約'),
(4, ''),
(5, E'温泉地の候補を探す\n次回のデート場所を決める'),
(6, E'お弁当を作る\nピクニックの準備'),
(7, ''),
(8, ''),
(9, ''),
(10, E'美術館のチケットを取る\nカフェでゆっくり過ごす'),
(11, ''),
(12, E'次は夜景ドライブを計画\nカメラを新調する');
""")

# Users
cur.execute("""
INSERT INTO Users (name, phone, email, password_hash) VALUES
('田中 太郎', '09011112222', 'a@a.com', %s),
('山田 花子', '08033334444', 'hanako@example.com', %s),
('佐藤 一郎', '07055556666', 'ichiro@example.com', %s);
""", (hashed_password, hashed_password, hashed_password))

# user_meetings 挿入（各ユーザーにMeetingを紐づける）
cur.execute("""
INSERT INTO user_meetings (user_id, meeting_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 11),
(2, 12);
""")

cur.execute("""
INSERT INTO NextEventDay (user_id, date) VALUES
(1, '2025-05-20'),
(2, '2025-06-01'),
(3, '2025-06-15');
""")


# コミット & 終了
conn.commit()
cur.close()
conn.close()

print("✅ テストデータ挿入が完了しました。")
