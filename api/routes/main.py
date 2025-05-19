# api/main.py
from typing import List
from uuid import uuid4
import bcrypt
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    Body,
    Path,
    Response,
    Cookie,
    Depends,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import smtplib
from email.mime.text import MIMEText
import random
from database.operation.meeting.create_meeting_data import create_meeting_data
from database.operation.meeting.delete_meetings_by_ids import delete_meetings_by_ids
from database.operation.meeting.get_all_good_points import get_all_good_points
from database.operation.meeting.get_meeting_details import get_meeting_details
from database.operation.meeting.get_meetings import get_meetings
from database.operation.meeting.update_meeting_data import update_meeting_data
from database.operation.user.authenticate_user import authenticate_user
from database.operation.user.create_jwt_token import create_jwt_token
from database.operation.user.create_user import create_user
from database.operation.user.decode_jwt_token import decode_jwt_token
from database.operation.user.get_next_event_day import get_next_event_day
from database.operation.user.get_user_by_id import get_user_by_id
from database.operation.user.update_next_event_day import update_next_event_day
from database.operation.user.update_user_info import update_user_info
from database.operation.user.user_exists import user_exists


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ユーザー認証用デコレータ例（トークンからuser_id抽出）
def get_current_user_id(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_jwt_token(access_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["user_id"]


@app.get("/meetings")
def read_meetings(user_id: int = Depends(get_current_user_id)):
    rows = get_meetings(user_id)
    return {"meetings": rows}


from fastapi import Body


@app.post("/meetings")
def create_meeting(
    new_meeting: dict = Body(...), user_id: int = Depends(get_current_user_id)
):
    meeting_id = create_meeting_data(new_meeting, user_id)
    if meeting_id is None:
        raise HTTPException(status_code=500, detail="Meeting作成失敗")
    return {"message": "登録に成功しました", "meeting_id": meeting_id}


@app.get("/meetings/{meeting_id}")
def read_meeting_details(meeting_id: int, user_id: int = Depends(get_current_user_id)):
    meeting = get_meeting_details(meeting_id, user_id)
    if meeting is None:
        raise HTTPException(
            status_code=404, detail="詳細データが見つかりませんでした。"
        )
    return {"meeting": meeting}


@app.put("/meetings/{meeting_id}")
def update_meeting(
    meeting_id: int,
    updated_data: dict = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    success = update_meeting_data(meeting_id, updated_data, user_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="更新するデートが見つからないか、権限がありません。"
        )
    return {"message": "更新に成功しました"}


app.mount("/files", StaticFiles(directory="files"), name="files")
UPLOAD_DIR = "files/uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": f"{UPLOAD_DIR}/{unique_filename}"}


class DeleteRequest(BaseModel):
    ids: List[int]


@app.post("/meetings/delete")
def delete_meetings(
    request: DeleteRequest, user_id: int = Depends(get_current_user_id)
):
    deleted_count = delete_meetings_by_ids(request.ids, user_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="削除対象のデートが見つからないか、権限がありません。",
        )
    return {"message": f"{deleted_count} 件のデート情報を削除しました。"}


@app.get("/goodpoints")
def read_good_points(user_id: int = Depends(get_current_user_id)):
    rows = get_all_good_points(user_id)
    return {"goodpoints": rows}


class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    code: str


class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: str


# メモリ上に一時保存（本番ならRedisなど）
email_verification_codes = {}


@app.post("/send_verification_code")
def send_verification_code(req: EmailRequest):
    code = str(random.randint(100000, 999999))
    email_verification_codes[req.email] = code

    msg = MIMEText(f"あなたの認証コードは {code} です。")
    msg["Subject"] = "【認証コード】ユーザー登録確認"
    msg["From"] = "noreply@example.com"
    msg["To"] = req.email

    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail="メール送信に失敗しました")

    return {"message": "認証コードを送信しました"}


@app.post("/register")
def register_user(data: RegisterRequest):
    if email_verification_codes.get(data.email) != data.code:
        raise HTTPException(status_code=400, detail="認証コードが無効です")
    try:
        user_id = create_user(data.name, data.phone, data.email, data.password)
        return {"message": "登録成功", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail="登録に失敗しました")


@app.post("/login")
def login(req: LoginRequest, response: Response):
    user_id = authenticate_user(req.email, req.password)
    if user_id is None:
        raise HTTPException(
            status_code=401, detail="メールアドレスかパスワードが違います。"
        )

    token = create_jwt_token(user_id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        path="/",
        secure=False,
    )
    return {"message": "ログイン成功", "user_id": user_id, "response": response}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "ログアウトしました"}


def get_current_user(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="未認証です")
    payload = decode_jwt_token(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="トークンが無効か期限切れです")
    user = get_user_by_id(payload["user_id"])
    if user is None:
        raise HTTPException(status_code=401, detail="ユーザーが存在しません")
    return user


@app.get("/me")
def read_current_user(user=Depends(get_current_user)):
    return {"user": user}


class UserUpdateRequest(BaseModel):
    name: str
    phone: str
    password: str


@app.put("/users/{user_id}")
def update_user(user_id: int = Path(...), data: UserUpdateRequest = Body(...)):
    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    success = update_user_info(user_id, data.name, data.phone, hashed_pw)
    if not success:
        raise HTTPException(
            status_code=404, detail="更新対象のユーザーが存在しません。"
        )
    return {"message": "ユーザー情報を更新しました"}


@app.get("/next")
def read_next_event_day(user_id: int = Depends(get_current_user_id)):
    next_day = get_next_event_day(user_id)
    if next_day is None:
        raise HTTPException(status_code=404, detail="次の予定が見つかりませんでした。")
    return next_day


class NextEventUpdateRequest(BaseModel):
    date: str  # 形式: YYYY-MM-DD


@app.put("/next")
def update_next_event(
    req: NextEventUpdateRequest, user_id: int = Depends(get_current_user_id)
):
    try:
        success = update_next_event_day(req.date, user_id)
        if not success:
            raise HTTPException(
                status_code=500, detail="次回イベント日の更新に失敗しました。"
            )
        return {"message": "次回イベント日を更新しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
