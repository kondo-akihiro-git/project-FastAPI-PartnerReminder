# api/main.py
from fastapi import FastAPI, HTTPException
from api.models.meeting import Meeting
from database.operation import get_meetings,get_meeting_details
from fastapi.middleware.cors import CORSMiddleware

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