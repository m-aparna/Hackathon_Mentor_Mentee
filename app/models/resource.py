from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


mentorship_resources = Table(
    "mentorship_resources",
    Base.metadata,
    Column("mentorship_id", Integer, ForeignKey("mentorship.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True),
)

goal_resources = Table(
    "goal_resources",
    Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True),
)


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    link = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    mentorships = relationship("Mentorship", secondary=mentorship_resources, back_populates="resources")
    goals = relationship("Goal", secondary=goal_resources, back_populates="resources")