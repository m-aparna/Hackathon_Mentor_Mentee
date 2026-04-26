from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base



mentorship_resources = Table(
    "mentorship_resources",
    Base.metadata,
    Column("mentorship_id", Integer, ForeignKey("mentorship.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True),
)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    link = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    # Which mentorships recommended this resource
    mentorships = relationship("Mentorship",secondary=mentorship_resources,back_populates="resources")