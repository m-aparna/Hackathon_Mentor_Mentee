from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from models.mentor import UserRole


class MentorCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class MentorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    skills: Optional[List[str]] = None


class MentorResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    department: Optional[str] = None
    skills: List[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}
