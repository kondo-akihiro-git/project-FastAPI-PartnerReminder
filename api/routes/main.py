# api/main.py
from typing import List
from uuid import uuid4
import bcrypt
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from api.models.meeting import Meeting
from database.operation import get_meetings,get_meeting_details, get_next_event_day
from database.operation import update_meeting_data
from database.operation import create_meeting_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import shutil
import os
from database.operation import delete_meetings_by_ids
from database.operation import get_all_good_points
from database.operation import create_user, authenticate_user
import smtplib
from email.mime.text import MIMEText
import random
from database.operation import user_exists 
from database.operation import update_user_info
from fastapi import Path
from database.operation import get_user_by_id
from fastapi import Response, Cookie, Depends
import jwt
from database.operation import create_jwt_token, decode_jwt_token


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # React のアドレス
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/meetings")
def read_meetings():
    rows = get_meetings()
    return {"meetings": rows}

@app.get("/meetings/{meeting_id}")
def read_meeting_details(meeting_id: int):
    meeting = get_meeting_details(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="詳細データが見つかりませんでした。")
    return {"meeting": meeting}

@app.put("/meetings/{meeting_id}")
def update_meeting(meeting_id: int, updated_data: dict = Body(...)):
    
    success = update_meeting_data(meeting_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="更新するデートが見つかりませんでした。")
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

@app.post("/meetings")
def create_meeting(new_data: dict = Body(...)):
    new_id = create_meeting_data(new_data)
    if new_id is None:
        raise HTTPException(status_code=400, detail="デート情報の登録に失敗しました。")
    return {"message": "登録に成功しました", "meeting_id": new_id}

class DeleteRequest(BaseModel):
    ids: List[int]

@app.post("/meetings/delete")
def delete_meetings(request: DeleteRequest):
    deleted_count = delete_meetings_by_ids(request.ids)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="削除対象のデートが見つかりませんでした。")
    return {"message": f"{deleted_count} 件のデート情報を削除しました。"}

@app.get("/goodpoints")
def read_good_points():
    rows = get_all_good_points()
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

    # Mailpit でメール送信
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

# ログイン処理（JWT発行・HTTP-only Cookieセット）
@app.post("/login")
def login(req: LoginRequest, response: Response):
    user_id = authenticate_user(req.email, req.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="メールアドレスかパスワードが違います。")

    token = create_jwt_token(user_id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        path="/",
        secure=False
    )
    return {"message": "ログイン成功", "user_id": user_id, "response":response}

# ログアウト処理（Cookie削除）
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "ログアウトしました"}


# 認証済みユーザー情報取得
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

@app.get("/verify-user/{user_id}")
def verify_user(user_id: int):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="ユーザーが存在しません")
    return {"message": "ユーザーは存在します"}


class UserUpdateRequest(BaseModel):
    name: str
    password: str

@app.put("/users/{user_id}")
def update_user(user_id: int = Path(...), data: UserUpdateRequest = Body(...)):
    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    success = update_user_info(user_id, data.name, hashed_pw)
    if not success:
        raise HTTPException(status_code=404, detail="更新対象のユーザーが存在しません。")
    return {"message": "ユーザー情報を更新しました"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    return {"user": user}

@app.get("/next")
def read_next_event_day():
    next_day = get_next_event_day()
    if next_day is None:
        raise HTTPException(status_code=404, detail="次の予定が見つかりませんでした。")
    return next_day