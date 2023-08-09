from datetime import datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Project(Document):
    name: Indexed(str)
    description: str
    created_by: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
