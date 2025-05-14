-- デート情報のメインテーブル（Meeting = デート名：場所＋日付）
DROP TABLE IF EXISTS Meetings CASCADE;
CREATE TABLE Meetings (
    id SERIAL PRIMARY KEY,
    title TEXT, -- 任意：デートに名前を付けたい場合（例：「水族館デート」）
    location TEXT NOT NULL, -- 場所（必須）
    date DATE NOT NULL,     -- 日付（必須）
    my_appearance_image_path TEXT -- 自分の外見（画像パス、NULL可）
);

-- イベント名（複数可）：例「水族館」「ランチ」など
DROP TABLE IF EXISTS EventNames;
CREATE TABLE EventNames (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    event_name TEXT
);

-- 相手の外見（複数可）：例「ショートヘア」「白ワンピース」など
DROP TABLE IF EXISTS PartnerAppearances;
CREATE TABLE PartnerAppearances (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    appearance TEXT
);

-- 話したこと（複数可）：例「旅行の話」「趣味の話」など
DROP TABLE IF EXISTS TalkedTopics;
CREATE TABLE TalkedTopics (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    topic TEXT
);

-- 相手の良いところ（複数可）：例「笑顔が素敵」「話が丁寧」など
DROP TABLE IF EXISTS PartnerGoodPoints;
CREATE TABLE PartnerGoodPoints (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    good_point TEXT
);

-- 次回に向けてのToDo（複数可）：例「次の場所を探す」「映画のチケット取る」など
DROP TABLE IF EXISTS TodoForNext;
CREATE TABLE TodoForNext (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    todo TEXT
);
