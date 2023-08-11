from typing import Literal, Optional

from beanie import PydanticObjectId
from beanie.operators import In, Push, Set
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.bugs import Bug
from models.projects import Project
from models.users import User
from schemas import bugs as BugSchema
from schemas import users as UserSchema
from utils.security import get_current_user

router = APIRouter(prefix="/bugs", tags=["Bugs"])


@router.post("/")
async def create_bug(
    bug: BugSchema.BugCreate, user: UserSchema.UserOut = Depends(get_current_user)
):
    is_manager = await User.has_role(email=user.email, role="manager")
    if not is_manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create a ticket.",
        )
    project_id = await Project.get(bug.project_id)
    if not project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    # check for every user in assigned_to list if they are in the users collection
    if not await User.find_one(In(User.id, bug.assigned_to)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in the database",
        )

    b = BugSchema.BugInDBCreate(**bug.model_dump(), created_by=user.id)
    await Bug(**b.model_dump()).insert()
    json_encoded = jsonable_encoder(b)
    return JSONResponse(content=json_encoded, status_code=status.HTTP_201_CREATED)


@router.get("/{project_id}")
async def get_bugs(
    project_id: PydanticObjectId,
    severity: Optional[Literal["low", "medium", "high"]] = None,
    status: Optional[str] = None,
    limit: int = 5,
    user: User = Depends(get_current_user),
):
    bugs = []
    result = Bug.find(Bug.project_id == project_id, limit=limit)
    if severity:
        result = result.find(Bug.severity == severity)
    if status:
        result = result.find(Bug.status == status)

    async for bug in result:
        bugs.append(BugSchema.BugInDBOut(**bug.model_dump()))
    return bugs


@router.put("/{bug_id}")
async def update_bug(
    bug_id: PydanticObjectId,
    bug: BugSchema.BugUpdate,
    user: User = Depends(get_current_user),
):
    bug_obj = await Bug.get(bug_id)

    if not bug_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bug ticket not found."
        )
    is_assigned_to = await Bug.is_assigned_to(bug_id=bug_id, user_id=user.id)
    is_created_by = bug_obj.created_by == user.id

    if not is_created_by and not is_assigned_to:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not assigned to this ticket.",
        )

    user_exists = await User.find(In(User.id, bug_obj.assigned_to)).first_or_none()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more users in assigned_to list do not exist.",
        )

    await bug_obj.set(
        bug.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True)
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Bug updated successfully"
    )
