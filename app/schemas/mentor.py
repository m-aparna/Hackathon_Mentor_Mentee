from pydantic import BaseModel, EmailStr
from typing import Optional
from models.mentor import UserRole


class MentorCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: Optional[str] = None


class MentorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None


class MentorResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    department: Optional[str] = None

    model_config = {"from_attributes": True}
