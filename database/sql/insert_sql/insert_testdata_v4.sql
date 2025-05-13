-- 既存データ削除
DELETE FROM TodoForNext;
DELETE FROM PartnerGoodPoints;
DELETE FROM TalkedTopics;
DELETE FROM PartnerAppearances;
DELETE FROM EventNames;
DELETE FROM MyAppearances;
DELETE FROM Meetings;

-- Meetings テーブル
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

-- MyAppearances テーブル
INSERT INTO MyAppearances (meeting_id, image_path) VALUES
(1, 'self1.jpg'),
(3, 'self2.jpg'),
(4, 'self3.jpg'),
(5, 'self3.jpg'),
(7, 'self4.jpg'),
(9, 'self5.jpg'),
(11, 'self6.jpg'),
(12, 'self7.jpg');

-- EventNames
INSERT INTO EventNames (meeting_id, event_name) VALUES
(1, E'水族館\nランチ'),
(2, 'カフェ'),
(3, E'映画鑑賞\nイタリアンディナー'),
(5, E'ドライブ\nランチ'),
(6, E'ピクニック\n公園散歩'),
(8, '博物館巡り'),
(9, E'夜景鑑賞\nディナー'),
(10, E'美術館鑑賞\n読書の話'),
(11, '川沿いの散歩'),
(12, E'イルミネーション\n写真撮影');

-- PartnerAppearances
INSERT INTO PartnerAppearances (meeting_id, appearance) VALUES
(1, E'ロングヘア\n白いワンピース'),
(3, E'眼鏡\nカジュアルな服装'),
(5, E'カジュアルな服装\n明るい笑顔'),
(6, E'明るい笑顔\nカジュアルな服装'),
(9, E'ドレッシーな服\n笑顔が素敵'),
(10, E'シンプルな服装\n落ち着いた雰囲気'),
(11, E'ポニーテール\nワンピース'),
(12, E'ニット帽\nロングコート');

-- TalkedTopics
INSERT INTO TalkedTopics (meeting_id, topic) VALUES
(1, E'海の生き物の話\n旅行の計画'),
(2, E'最近読んだ本\n好きな作家'),
(3, E'映画の感想\nおすすめの映画'),
(5, E'家族の話\n将来の計画'),
(6, E'趣味のカメラ\nおすすめの撮影地'),
(10, E'アートの話\n美術館の展示'),
(12, E'夜景スポットの話\n写真撮影のコツ');

-- PartnerGoodPoints
INSERT INTO PartnerGoodPoints (meeting_id, good_point) VALUES
(1, E'優しい話し方\n気配りが素晴らしい'),
(2, E'笑顔が素敵\n話が面白い'),
(3, E'映画のセンスが良い\n気配りが上手'),
(5, E'ドライブ中の会話が楽しい\nリラックスできる雰囲気'),
(9, E'気配り上手\n笑顔が素敵'),
(11, E'話しやすい\n自然体でいられる');

-- TodoForNext
INSERT INTO TodoForNext (meeting_id, todo) VALUES
(1, E'次は動物園に行く予定\nランチの場所を決める'),
(3, E'映画館を予約する\nディナーの予約'),
(5, E'温泉地の候補を探す\n次回のデート場所を決める'),
(6, E'お弁当を作る\nピクニックの準備'),
(10, E'美術館のチケットを取る\nカフェでゆっくり過ごす'),
(12, E'次は夜景ドライブを計画\nカメラを新調する');
