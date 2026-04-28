from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.goal import Goal
from app.models.resource import Resource
from app.schemas.resource import ResourceResponse

router = APIRouter(prefix="/goals", tags=["Goal Resources"])

@router.post("/{goal_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def attach_resource_to_goal(goal_id: int, resource_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource not in goal.resources:
        goal.resources.append(resource)
        db.commit()


@router.get("/{goal_id}/resources", response_model=List[ResourceResponse])
def list_resources_for_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal.resources


@router.delete("/{goal_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_resource_from_goal(goal_id: int, resource_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource in goal.resources:
        goal.resources.remove(resource)
        db.commit()