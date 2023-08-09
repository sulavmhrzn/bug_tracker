from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from models.users import User
from schemas.users import Userout

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/access-token")


def create_access_token(sub: str, expire_time_delta: Optional[datetime] = None):
    if expire_time_delta:
        expire = datetime.utcnow() + expire_time_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(claims=to_encode, key=settings.JWT_SECRET_KEY, algorithm="HS256")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    except JWTError:
        raise credentials_exception
    email = payload.get("sub")
    if not email:
        raise credentials_exception

    user = await User.get_user_by_email(email=email)
    if not user:
        raise credentials_exception
    return user
