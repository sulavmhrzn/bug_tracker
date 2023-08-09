from beanie.exceptions import RevisionIdWasChanged
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models.users import User
from schemas import users as UserSchema
from utils.password import hash_password

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/signup")
async def signup(user: UserSchema.UserCreate):
    user.password = hash_password(user.password)
    try:
        new_user = await User(
            email=user.email, hashed_password=user.password, role=user.role
        ).save()
    except RevisionIdWasChanged:
        raise HTTPException(
            detail={"msg": "user already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content=UserSchema.Userout(
            email=new_user.email, role=new_user.role
        ).model_dump(),
        status_code=status.HTTP_201_CREATED,
    )
