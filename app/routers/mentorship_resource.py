from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.resource import Resource
from models.mentorship import Mentorship
from schemas.resource import ResourceResponse

router = APIRouter(prefix="/mentorship", tags=["Mentorship Resources"])

@router.post("/{mentorship_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def recommend_resource_to_mentorship(mentorship_id: int, resource_id: int, db: Session = Depends(get_db)):
    mentorship = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not mentorship:
        raise HTTPException(status_code=404, detail="Mentorship not found")

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource not in mentorship.resources:
        mentorship.resources.append(resource)
        db.commit()

@router.get("/{mentorship_id}/resources", response_model=List[ResourceResponse])
def list_resources_for_mentorship(mentorship_id: int, db: Session = Depends(get_db)):
    mentorship = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not mentorship:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    return mentorship.resources

@router.delete("/{mentorship_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_resource_from_mentorship(mentorship_id: int, resource_id: int, db: Session = Depends(get_db)):
    mentorship = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not mentorship:
        raise HTTPException(status_code=404, detail="Mentorship not found")

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource in mentorship.resources:
        mentorship.resources.remove(resource)
        db.commit()