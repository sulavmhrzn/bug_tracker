from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Extra, Field


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserCreate(UserBase):
    role: Literal["developer", "manager"] = Field(default="developer", max_laength=20)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@mail.com",
                "password": "secretpassword",
                "role": "developer",
            }
        },
        str_to_lower=True,
        extra=Extra.ignore,
    )


class UserUpdate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    email: EmailStr
    role: str


class UserInDB(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
