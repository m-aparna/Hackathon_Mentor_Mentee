from sqlalchemy import Column, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from database import Base
from models.resource import mentorship_resources
import enum
import datetime


class MentorshipStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    completed = "completed"


class Mentorship(Base):
    __tablename__ = "mentorship"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentor.id", ondelete="CASCADE"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("mentee.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, default=datetime.date.today)
    status = Column(Enum(MentorshipStatus), default=MentorshipStatus.active)

    # Relationships
    mentor = relationship("Mentor", foreign_keys=[mentor_id], back_populates="mentorship_as_mentor")
    mentee = relationship("Mentee", foreign_keys=[mentee_id], back_populates="mentorship_as_mentee")
    goals = relationship("Goal", back_populates="mentorship", cascade="all, delete-orphan")
    resources = relationship("Resource",secondary=mentorship_resources,back_populates="mentorships")
