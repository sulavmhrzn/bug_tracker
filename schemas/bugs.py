from datetime import datetime
from typing import Literal, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from .projects import ProjectOut
from .users import UserOut


class BugsBase(BaseModel):
    title: str
    description: str
    severity: Literal["low", "medium", "high"]
    status: Literal["open", "closed", "underdevelopment"]
    project_id: PydanticObjectId
    assigned_to: list[PydanticObjectId]


class BugCreate(BugsBase):
    pass


class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["open", "closed", "underdevelopment"]] = None


class BugInDBBase(BugsBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: PydanticObjectId


class BugInDBCreate(BugInDBBase):
    pass


class BugInDBOut(BugInDBBase):
    id: PydanticObjectId = Field(..., alias="_id")


class BugDetailOut(BaseModel):
    title: str
    description: str
    severity: Literal["low", "medium", "high"]
    status: Literal["open", "closed", "underdevelopment"]
    project: list[ProjectOut]
    assigned_to: list[UserOut]
