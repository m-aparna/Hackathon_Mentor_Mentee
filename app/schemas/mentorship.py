from pydantic import BaseModel
from typing import Optional
import datetime
from app.models.mentorship import MentorshipStatus


class MentorshipCreate(BaseModel):
    mentor_id: int
    mentee_id: int
    start_date: Optional[datetime.date] = None
    status: MentorshipStatus = MentorshipStatus.active


class MentorshipUpdate(BaseModel):
    status: Optional[MentorshipStatus] = None


class MentorshipResponse(BaseModel):
    id: int
    mentor_id: int
    mentee_id: int
    start_date: Optional[datetime.date] = None
    status: MentorshipStatus

    model_config = {"from_attributes": True}