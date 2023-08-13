from typing import Literal, Optional

from beanie import PydanticObjectId
from beanie.operators import In
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.bugs import Bug
from models.projects import Project
from models.users import User
from schemas import bugs as BugSchema
from schemas import users as UserSchema
from utils.security import get_current_user
from utils.telegram_notification import send_message

router = APIRouter(prefix="/bugs", tags=["Bugs"])


def send_message_to_telegram(text: str):
    send_message(text=text)


@router.post("/")
async def create_bug(
    bug: BugSchema.BugCreate,
    background_tasks: BackgroundTasks,
    user: UserSchema.UserOut = Depends(get_current_user),
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

    if not await User.find_one(In(User.id, bug.assigned_to)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in the database",
        )
    b = BugSchema.BugInDBCreate(**bug.model_dump(), created_by=user.id)
    await Bug(**b.model_dump()).insert()

    json_encoded = jsonable_encoder(b)

    format_message = f"**New bug ticket created:**\nTitle: {b.title}\nDescription: {b.description}\nSeverity: {b.severity}\nStatus: {b.status}\nCreated by: {str(b.created_by)}\nProject ID: {str(b.project_id)}"
    background_tasks.add_task(send_message_to_telegram, format_message)
    return JSONResponse(content=json_encoded, status_code=status.HTTP_201_CREATED)


@router.get("/projects/{project_id}")
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
    bugs = await result.project(BugSchema.BugInDBOut).to_list()

    return bugs


@router.put("/{bug_id}")
async def update_bug(
    bug_id: PydanticObjectId,
    bug: BugSchema.BugUpdate,
    background_tasks: BackgroundTasks,
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

    b = await bug_obj.set(
        bug.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True)
    )
    format_message = f"**Bug ticket updated:**\nTitle: {b.title}\nDescription: {b.description}\nSeverity: {b.severity}\nStatus: {b.status}\nCreated by: {str(b.created_by)}\nProject ID: {str(b.project_id)}"
    background_tasks.add_task(send_message_to_telegram, format_message)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Bug updated successfully"
    )


@router.delete("/{bug_id}")
async def delete_bug(bug_id: PydanticObjectId, user: User = Depends(get_current_user)):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bug ticket not found."
        )
    is_created_by = bug.created_by == user.id
    if not is_created_by:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorzied to perforrm this action",
        )

    await bug.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{bug_id}")
async def get_bug(
    bug_id: PydanticObjectId,
    user: User = Depends(get_current_user),
):
    bug = (
        await Bug.find(Bug.id == bug_id)
        .aggregate(
            [
                {
                    "$lookup": {
                        "from": "User",
                        "localField": "assigned_to",
                        "foreignField": "_id",
                        "as": "assigned_to",
                    }
                },
                {
                    "$lookup": {
                        "from": "Project",
                        "localField": "project_id",
                        "foreignField": "_id",
                        "as": "project",
                    }
                },
            ],
            projection_model=BugSchema.BugDetailOut,
        )
        .to_list()
    )

    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found"
        )
    return bug[0]
