

-- デート情報のメインテーブル（Meeting = デート名：場所＋日付）
DROP TABLE IF EXISTS Meetings CASCADE;
CREATE TABLE Meetings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL, -- 任意：デートに名前を付けたい場合
    location TEXT NOT NULL,
    date DATE NOT NULL
);

-- 自分の外見（画像パス）
DROP TABLE IF EXISTS MyAppearances;
CREATE TABLE MyAppearances (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER UNIQUE REFERENCES Meetings(id) ON DELETE CASCADE,
    image_path TEXT
);

-- 以下、他のテーブルは変更なし
DROP TABLE IF EXISTS EventNames;
CREATE TABLE EventNames (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    event_name TEXT
);

DROP TABLE IF EXISTS PartnerAppearances;
CREATE TABLE PartnerAppearances (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    appearance TEXT
);

DROP TABLE IF EXISTS TalkedTopics;
CREATE TABLE TalkedTopics (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    topic TEXT
);

DROP TABLE IF EXISTS PartnerGoodPoints;
CREATE TABLE PartnerGoodPoints (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    good_point TEXT
);

DROP TABLE IF EXISTS TodoForNext;
CREATE TABLE TodoForNext (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    todo TEXT
);
