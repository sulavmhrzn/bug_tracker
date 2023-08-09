from datetime import datetime
from typing import Literal, Optional

from beanie import Document, Indexed
from pydantic import Field

from utils.password import verify_hash_password


class User(Document):
    email: Indexed(str, unique=True)
    hashed_password: str = Field(min_length=8, max_length=128)
    role: Literal["developer", "manager"] = Field(default="developer", max_length=20)
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def get_user_by_email(cls, *, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email)

    @classmethod
    async def authenticate(cls, *, email: str, password: str) -> Optional["User"]:
        user = await cls.get_user_by_email(email=email)
        if not user or not verify_hash_password(user.hashed_password, password):
            return None
        return user

    @classmethod
    async def has_role(cls, *, email: str, role: str) -> bool:
        user = await cls.get_user_by_email(email=email)
        if not user:
            return False
        return user.role == role
