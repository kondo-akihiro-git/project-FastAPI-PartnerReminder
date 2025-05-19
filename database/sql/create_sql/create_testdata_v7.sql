-- ▼ 依存テーブルを先に削除
DROP TABLE IF EXISTS user_meetings;
DROP TABLE IF EXISTS NextEventDay;
DROP TABLE IF EXISTS TodoForNext;
DROP TABLE IF EXISTS PartnerGoodPoints;
DROP TABLE IF EXISTS TalkedTopics;
DROP TABLE IF EXISTS PartnerAppearances;
DROP TABLE IF EXISTS EventNames;
DROP TABLE IF EXISTS MeetingPhotos;
DROP TABLE IF EXISTS MyAppearances;

-- ▼ Meetings → Users を最後に削除
DROP TABLE IF EXISTS Meetings;
DROP TABLE IF EXISTS Users;


CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);


-- デート情報のメインテーブル（Meeting = デート名：場所＋日付）
CREATE TABLE Meetings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL, -- 任意：デートに名前を付けたい場合
    location TEXT NOT NULL,
    date DATE NOT NULL
);

-- 自分の外見（画像パス）
CREATE TABLE MyAppearances (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER UNIQUE REFERENCES Meetings(id) ON DELETE CASCADE,
    image_path TEXT NOT NULL
);

-- デート写真（画像パス）
CREATE TABLE MeetingPhotos (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER UNIQUE REFERENCES Meetings(id) ON DELETE CASCADE,
    image_path TEXT NOT NULL
);

-- 以下、他のテーブルは変更なし
CREATE TABLE EventNames (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    event_name TEXT NOT NULL
);

CREATE TABLE PartnerAppearances (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    appearance TEXT NOT NULL
);

CREATE TABLE TalkedTopics (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    topic TEXT NOT NULL
);

CREATE TABLE PartnerGoodPoints (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    good_point TEXT NOT NULL
);

CREATE TABLE TodoForNext (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES Meetings(id) ON DELETE CASCADE,
    todo TEXT NOT NULL
);


CREATE TABLE user_meetings (
    user_id INT NOT NULL,
    meeting_id INT NOT NULL,
    PRIMARY KEY (user_id, meeting_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);


CREATE TABLE NextEventDay (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    date DATE NOT NULL
);



