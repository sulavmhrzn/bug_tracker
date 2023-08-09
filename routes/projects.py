from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.projects import Project
from models.users import User
from schemas import projects as ProjectSchema
from schemas.users import UserOut
from utils.security import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/create")
async def create_project(
    project: ProjectSchema.ProjectBase, user: UserOut = Depends(get_current_user)
):
    is_manager = await User.has_role(email=user.email, role="manager")

    if not is_manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create a project",
        )
    project_obj = ProjectSchema.ProjectCreate(
        **project.model_dump(), created_by=user.id
    )

    project_created = await Project(**project_obj.model_dump()).insert()
    json_encoded = jsonable_encoder(
        ProjectSchema.ProjectOut(**project_created.model_dump())
    )

    return JSONResponse(
        content=json_encoded,
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_projects(user: UserOut = Depends(get_current_user)):
    is_manager = await User.has_role(email=user.email, role="manager")

    if not is_manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized.",
        )
    user = await User.get_user_by_email(email=user.email)
    result = Project.find_many(Project.created_by == user.id)
    projects = []
    async for project in result:
        projects.append(ProjectSchema.ProjectOut(**project.model_dump()))
    return projects