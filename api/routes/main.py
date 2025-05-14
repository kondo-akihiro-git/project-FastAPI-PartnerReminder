# api/main.py
from typing import List
from uuid import uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from api.models.meeting import Meeting
from database.operation import get_meetings,get_meeting_details
from database.operation import update_meeting_data
from database.operation import create_meeting_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import shutil
import os
from database.operation import delete_meetings_by_ids
from database.operation import get_all_good_points

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React のアドレス
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