from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.models.mentee import UserRole


class MenteeCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class MenteeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    skills: Optional[List[str]] = None 


class MenteeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    department: Optional[str] = None
    skills: List[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}
