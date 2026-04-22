from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.mentorship import Mentorship
from models.goal import Goal, ProgressLog
from schemas.goal import (
    GoalCreate, GoalUpdate, GoalResponse,
    ProgressLogCreate, ProgressLogResponse,
)

router = APIRouter(tags=["Goals"])

goal_router = APIRouter(prefix="/goals")
progress_router = APIRouter(prefix="/progress-logs")


# ── Goals ──────────────────────────────────────────────────────────────────────

@goal_router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    mentorship = db.query(Mentorship).filter(
        Mentorship.id == payload.mentorship_id
    ).first()
    if not mentorship:
        raise HTTPException(status_code=400, detail="Mentorship not found")

    goal = Goal(**payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@goal_router.get("/", response_model=List[GoalResponse])
def list_goals(mentorship_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Goal)
    if mentorship_id:
        q = q.filter(Goal.mentorship_id == mentorship_id)
    return q.all()


@goal_router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@goal_router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, payload: GoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


@goal_router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()


# ── Progress Logs ──────────────────────────────────────────────────────────────

@progress_router.post("/", response_model=ProgressLogResponse, status_code=status.HTTP_201_CREATED)
def create_progress_log(payload: ProgressLogCreate, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == payload.goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if not 0 <= payload.progress_percent <= 100:
        raise HTTPException(status_code=400, detail="progress_percent must be between 0 and 100")
    log = ProgressLog(**payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


# @progress_router.get("/goal/{goal_id}", response_model=List[ProgressLogResponse])
# def get_logs_for_goal(goal_id: int, db: Session = Depends(get_db)):
#     return db.query(ProgressLog).filter(ProgressLog.goal_id == goal_id).all()


@progress_router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ProgressLog).filter(ProgressLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Progress log not found")
    db.delete(log)
    db.commit()


router.include_router(goal_router)
router.include_router(progress_router)
