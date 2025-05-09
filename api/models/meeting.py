from pydantic import BaseModel
from typing import List

class Meeting(BaseModel):
    title: str
    events: List[str]
    partner_looks: List[str]
    talked_topics: List[str]
    good_points: List[str]
    next_preparation: List[str]
    self_look_image: str 