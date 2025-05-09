# api/main.py
from fastapi import FastAPI, HTTPException
from api.models.meeting import Meeting
from database.operation import get_meetings,get_meeting_details
from database.operation import update_meeting_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

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
