from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mentorship import Mentorship
from app.models.mentee import Mentee, UserRole
from app.models.mentor import Mentor
from app.schemas.mentorship import MentorshipCreate, MentorshipUpdate, MentorshipResponse

router = APIRouter(prefix="/mentorships", tags=["Mentorships"])


@router.post("/", response_model=MentorshipResponse, status_code=status.HTTP_201_CREATED)
def create_mentorship(payload: MentorshipCreate, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == payload.mentor_id).first()
    if not mentor or mentor.role != UserRole.mentor:
        raise HTTPException(status_code=400, detail="Mentor not found or user is not a mentor")

    mentee = db.query(Mentee).filter(Mentee.id == payload.mentee_id).first()
    if not mentee or mentee.role != UserRole.mentee:
        raise HTTPException(status_code=400, detail="Mentee not found or user is not a mentee")

    if mentor.department != mentee.department:
        raise HTTPException(status_code=400, detail="Mentor and mentee must belong to the same department")

    mentor_skills = set(mentor.skills or [])
    mentee_skills = set(mentee.skills or [])
    shared_skills = sorted(mentor_skills.intersection(mentee_skills))
    if not shared_skills:
        raise HTTPException(status_code=400, detail="Mentor and mentee must share at least one skill")

    existing = db.query(Mentorship).filter(
        Mentorship.mentor_id == payload.mentor_id,
        Mentorship.mentee_id == payload.mentee_id,
        Mentorship.status == "active",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Active mentorship already exists between these users")

    payload_data = payload.model_dump()
    payload_data["department"] = mentor.department
    payload_data["skills"] = shared_skills

    m = Mentorship(**payload_data)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/", response_model=List[MentorshipResponse])
def list_mentorships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Mentorship).offset(skip).limit(limit).all()


@router.get("/{mentorship_id}", response_model=MentorshipResponse)
def get_mentorship(mentorship_id: int, db: Session = Depends(get_db)):
    m = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    return m


@router.patch("/{mentorship_id}", response_model=MentorshipResponse)
def update_mentorship(mentorship_id: int, payload: MentorshipUpdate, db: Session = Depends(get_db)):
    m = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(m, field, value)
    db.commit()
    db.refresh(m)
    return m


@router.delete("/{mentorship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentorship(mentorship_id: int, db: Session = Depends(get_db)):
    m = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    db.delete(m)
    db.commit()