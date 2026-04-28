from pydantic import BaseModel
from typing import Optional
from app.models.goal import GoalStatus


class GoalCreate(BaseModel):
    mentorship_id: int
    title: str
    description: Optional[str] = None
    status: GoalStatus = GoalStatus.not_started


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[GoalStatus] = None


class GoalResponse(BaseModel):
    id: int
    mentorship_id: int
    title: str
    description: Optional[str] = None
    status: GoalStatus

    model_config = {"from_attributes": True}


class ProgressLogCreate(BaseModel):
    goal_id: int
    progress_percent: int
    update_text: Optional[str] = None


class ProgressLogUpdate(BaseModel):
    progress_percent: Optional[int] = None
    update_text: Optional[str] = None


class ProgressLogResponse(BaseModel):
    id: int
    goal_id: int
    progress_percent: int
    update_text: Optional[str] = None

    model_config = {"from_attributes": True}
