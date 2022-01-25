from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseLog(BaseModel):
    id: int
    object_id: int
    object_name: str
    object_type: str
    action: str
    time: datetime = datetime.now()
    created_alarm: bool
    actor_id: int
    message: str


class CreateLog(BaseModel):
    object_name: str
    action: str
