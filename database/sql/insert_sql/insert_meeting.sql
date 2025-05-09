-- Meetings テーブル：10件分
INSERT INTO Meetings (title, location, date, my_appearance_image_path) VALUES
('水族館デート', '品川水族館', '2024-04-15', 'images/self1.jpg'),
('カフェでまったり', '代官山カフェ', '2024-04-22', NULL),
('映画とディナー', '渋谷', '2024-04-29', 'images/self2.jpg'),
(NULL, '新宿御苑', '2024-05-01', NULL),
('ドライブデート', '箱根', '2024-05-04', 'images/self3.jpg'),
('ランチと公園', '代々木公園', '2024-05-07', NULL),
(NULL, '浅草寺', '2024-05-09', 'images/self4.jpg'),
('博物館めぐり', '上野', '2024-05-12', NULL),
('夜景とディナー', 'お台場', '2024-05-15', 'images/self5.jpg'),
('美術館と読書の話', '六本木', '2024-05-18', NULL);

-- EventNames：いくつかのMeetingsに対して
INSERT INTO EventNames (meeting_id, event_name) VALUES
(1, '水族館'),
(1, 'ランチ'),
(2, 'カフェ'),
(3, '映画鑑賞'),
(3, 'イタリアンディナー'),
(5, 'ドライブ'),
(6, 'ピクニック'),
(8, '博物館巡り'),
(9, '夜景鑑賞'),
(10, '美術館鑑賞');

-- PartnerAppearances
INSERT INTO PartnerAppearances (meeting_id, appearance) VALUES
(1, 'ロングヘア'),
(1, '白いワンピース'),
(3, '眼鏡'),
(5, 'カジュアルな服装'),
(6, '明るい笑顔'),
(9, 'ドレッシーな服'),
(10, 'シンプルな服装');

-- TalkedTopics
INSERT INTO TalkedTopics (meeting_id, topic) VALUES
(1, '海の生き物の話'),
(2, '最近読んだ本'),
(3, '映画の感想'),
(5, '家族の話'),
(6, '趣味のカメラ'),
(10, 'アートの話');

-- PartnerGoodPoints
INSERT INTO PartnerGoodPoints (meeting_id, good_point) VALUES
(1, '優しい話し方'),
(2, '笑顔が素敵'),
(3, '映画のセンスが良い'),
(5, 'ドライブ中の会話が楽しい'),
(9, '気配り上手');

-- TodoForNext
INSERT INTO TodoForNext (meeting_id, todo) VALUES
(1, '次は動物園に行く予定'),
(3, '映画館を予約する'),
(5, '温泉地の候補を探す'),
(6, 'お弁当を作る'),
(10, '美術館のチケットを取る');
