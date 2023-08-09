from datetime import datetime
from typing import Literal

from beanie import Document, Indexed
from pydantic import Field


class User(Document):
    email: Indexed(str, unique=True)
    hashed_password: str = Field(min_length=8, max_length=128)
    role: Literal["developer", "manager"] = Field(default="developer", max_length=20)
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
