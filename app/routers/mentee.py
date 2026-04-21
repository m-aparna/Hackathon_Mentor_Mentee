from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.mentee import Mentee
from schemas.mentee import MenteeCreate, MenteeUpdate, MenteeResponse

router = APIRouter(prefix="/mentees", tags=["mentees"])


@router.post("/", response_model=MenteeResponse, status_code=status.HTTP_201_CREATED)
def create_mentee(payload: MenteeCreate, db: Session = Depends(get_db)):
    existing = db.query(Mentee).filter(Mentee.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    mentee = Mentee(**payload.model_dump())
    db.add(mentee)
    db.commit()
    db.refresh(mentee)
    return mentee


@router.get("/", response_model=List[MenteeResponse])
def list_mentees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Mentee).offset(skip).limit(limit).all()


@router.get("/{mentee_id}", response_model=MenteeResponse)
def get_mentee(mentee_id: int, db: Session = Depends(get_db)):
    mentee = db.query(Mentee).filter(Mentee.id == mentee_id).first()
    if not mentee:
        raise HTTPException(status_code=404, detail="mentee not found")
    return mentee


@router.patch("/{mentee_id}", response_model=MenteeResponse)
def update_mentee(mentee_id: int, payload: MenteeUpdate, db: Session = Depends(get_db)):
    mentee = db.query(Mentee).filter(Mentee.id == mentee_id).first()
    if not mentee:
        raise HTTPException(status_code=404, detail="mentee not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(mentee, field, value)
    db.commit()
    db.refresh(mentee)
    return mentee


@router.delete("/{mentee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentee(mentee_id: int, db: Session = Depends(get_db)):
    mentee = db.query(Mentee).filter(Mentee.id == mentee_id).first()
    if not mentee:
        raise HTTPException(status_code=404, detail="mentee not found")
    db.delete(mentee)
    db.commit()
