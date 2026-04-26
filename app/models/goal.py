from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class GoalStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    mentorship_id = Column(Integer, ForeignKey("mentorship.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(GoalStatus), default=GoalStatus.not_started)

    # Relationships
    mentorship = relationship("Mentorship", back_populates="goals")
    progress_logs = relationship("ProgressLog", back_populates="goal", cascade="all, delete-orphan")


class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
    progress_percent = Column(Integer, default=0)
    update_text = Column(Text, nullable=True)

    # Relationships
    goal = relationship("Goal", back_populates="progress_logs")
