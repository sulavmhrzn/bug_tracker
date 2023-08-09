from datetime import timedelta

from beanie.exceptions import RevisionIdWasChanged
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import settings
from models.users import User
from schemas import users as UserSchema
from utils.password import hash_password
from utils.security import create_access_token, get_current_user

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


@router.post("/access-token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            detail="invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED
        )
    if not user.is_active:
        raise HTTPException(
            detail="user is inactive", status_code=status.HTTP_401_UNAUTHORIZED
        )
    token = create_access_token(
        sub=user.email,
        expire_time_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/dashboard")
async def dashboard(user: User = Depends(get_current_user)):
    return UserSchema.Userout(**user.model_dump())
