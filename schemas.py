from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    # common fields for all events
    event_type: str
    event_data: str | None = None
    reason: str | None = None


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True
