# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database.operation import get_meetings

app = FastAPI()

class Meeting(BaseModel):
    title: str
    events: List[str]
    partner_looks: List[str]
    talked_topics: List[str]
    good_points: List[str]
    next_preparation: List[str]
    self_look_image: str  # Base64文字列などを想定

@app.get("/meetings")
def read_meetings():
    rows = get_meetings()
    return {"meetings": rows}
