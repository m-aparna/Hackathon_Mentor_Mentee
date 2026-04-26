from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mentor import Mentor
from app.schemas.mentor import MentorCreate, MentorUpdate, MentorResponse

router = APIRouter(prefix="/mentors", tags=["mentors"])


@router.post("/", response_model=MentorResponse, status_code=status.HTTP_201_CREATED)
def create_mentor(payload: MentorCreate, db: Session = Depends(get_db)):
    existing = db.query(Mentor).filter(Mentor.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    mentor = Mentor(**payload.model_dump(exclude={"skills"}))
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor


@router.get("/", response_model=List[MentorResponse])
def list_mentors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Mentor).offset(skip).limit(limit).all()


@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="mentor not found")
    return mentor


@router.patch("/{mentor_id}", response_model=MentorResponse)
def update_mentor(mentor_id: int, payload: MentorUpdate, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="mentor not found")
    for field, value in payload.model_dump(exclude_none=True, exclude={"skills"}).items():
        setattr(mentor, field, value)
    db.commit()
    db.refresh(mentor)
    return mentor


@router.delete("/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="mentor not found")
    db.delete(mentor)
    db.commit()
