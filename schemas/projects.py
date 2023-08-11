from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    created_by: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectOut(ProjectBase):
    id: PydanticObjectId
    created_at: datetime


class ProjectInDBBase(ProjectBase):
    id: PydanticObjectId
    created_at: datetime
