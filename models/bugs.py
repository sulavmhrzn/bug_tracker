from datetime import datetime
from typing import Literal, Optional

from beanie import Document, PydanticObjectId
from beanie.operators import In
from pydantic import Field


class Bug(Document):
    title: str
    description: str
    severity: Literal["low", "medium", "high"]
    status: Literal["open", "closed", "underdevelopment"]
    project_id: PydanticObjectId
    assigned_to: list[PydanticObjectId]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: PydanticObjectId

    @classmethod
    async def is_assigned_to(
        cls, *, bug_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> bool:
        result = await Bug.find_one(In(Bug.assigned_to, [user_id]), Bug.id == bug_id)
        return result or False
