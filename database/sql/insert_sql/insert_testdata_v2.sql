-- 既存データ削除（子テーブルから削除）
DELETE FROM TodoForNext;
DELETE FROM PartnerGoodPoints;
DELETE FROM TalkedTopics;
DELETE FROM PartnerAppearances;
DELETE FROM EventNames;
DELETE FROM Meetings;

-- Meetings テーブル
INSERT INTO Meetings (title, location, date, my_appearance_image_path) VALUES
('水族館デート', '品川水族館', '2024-04-15', '/uploaded_images/self1.jpg'),
('カフェでまったり', '代官山カフェ', '2024-04-22', NULL),
('映画とディナー', '渋谷', '2024-04-29', '/uploaded_images/self2.jpg'),
(NULL, '新宿御苑', '2024-05-01', '/uploaded_images/self3.jpg'),
('ドライブデート', '箱根', '2024-05-04', '/uploaded_images/self3.jpg'),
('ランチと公園', '代々木公園', '2024-05-07', NULL),
(NULL, '浅草寺', '2024-05-09', '/uploaded_images/self4.jpg'),
('博物館めぐり', '上野', '2024-05-12', NULL),
('夜景とディナー', 'お台場', '2024-05-15', '/uploaded_images/self5.jpg'),
('美術館と読書の話', '六本木', '2024-05-18', NULL);

-- EventNames（改行込み）
INSERT INTO EventNames (meeting_id, event_name) VALUES
(1, '水族館\nランチ'),
(2, 'カフェ'),
(3, '映画鑑賞\nイタリアンディナー'),
(5, 'ドライブ\nランチ'),
(6, 'ピクニック\n公園散歩'),
(8, '博物館巡り'),
(9, '夜景鑑賞\nディナー'),
(10, '美術館鑑賞\n読書の話');

-- PartnerAppearances（改行込み）
INSERT INTO PartnerAppearances (meeting_id, appearance) VALUES
(1, 'ロングヘア\n白いワンピース'),
(3, '眼鏡\nカジュアルな服装'),
(5, 'カジュアルな服装\n明るい笑顔'),
(6, '明るい笑顔\nカジュアルな服装'),
(9, 'ドレッシーな服\n笑顔が素敵'),
(10, 'シンプルな服装\n落ち着いた雰囲気');

-- TalkedTopics（改行込み）
INSERT INTO TalkedTopics (meeting_id, topic) VALUES
(1, '海の生き物の話\n旅行の計画'),
(2, '最近読んだ本\n好きな作家'),
(3, '映画の感想\nおすすめの映画'),
(5, '家族の話\n将来の計画'),
(6, '趣味のカメラ\nおすすめの撮影地'),
(10, 'アートの話\n美術館の展示');

-- PartnerGoodPoints（改行込み）
INSERT INTO PartnerGoodPoints (meeting_id, good_point) VALUES
(1, '優しい話し方\n気配りが素晴らしい'),
(2, '笑顔が素敵\n話が面白い'),
(3, '映画のセンスが良い\n気配りが上手'),
(5, 'ドライブ中の会話が楽しい\nリラックスできる雰囲気'),
(9, '気配り上手\n笑顔が素敵');

-- TodoForNext（改行込み）
INSERT INTO TodoForNext (meeting_id, todo) VALUES
(1, '次は動物園に行く予定\nランチの場所を決める'),
(3, '映画館を予約する\nディナーの予約'),
(5, '温泉地の候補を探す\n次回のデート場所を決める'),
(6, 'お弁当を作る\nピクニックの準備'),
(10, '美術館のチケットを取る\nカフェでゆっくり過ごす');
