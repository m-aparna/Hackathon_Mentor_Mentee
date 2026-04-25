from pydantic import BaseModel, HttpUrl
from typing import Optional


class ResourceCreate(BaseModel):
    title: str
    link: HttpUrl
    description: Optional[str] = None


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[HttpUrl] = None
    description: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    link: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
