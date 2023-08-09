from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    created_by: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectOut(ProjectBase):
    id: PydanticObjectId
    created_at: datetime


class ProjectInDBBase(ProjectBase):
    id: PydanticObjectId
    created_at: datetime
