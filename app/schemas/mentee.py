from pydantic import BaseModel, EmailStr
from typing import Optional
from models.mentee import UserRole


class MenteeCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: Optional[str] = None


class MenteeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None


class MenteeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    department: Optional[str] = None

    model_config = {"from_attributes": True}
