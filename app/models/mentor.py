from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    mentor = "mentor"


class Mentor(Base):
    __tablename__ = "mentor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    role = Column(Enum(UserRole), nullable=False)
    department = Column(String(100), nullable=True)
    skills=Column(JSON, nullable=False, default= list)

    # # Relationships
    # skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    mentorship_as_mentor = relationship(
        "Mentorship", foreign_keys="Mentorship.mentor_id", back_populates="mentor"
    )
