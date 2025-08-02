# routers/project.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from database import get_session
from models import Project, Member, User
from schemas import ProjectCreate, ProjectRead
from database import get_session
from deps import get_current_user, get_admin_user
import logging
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.get("/")
def get_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    member_project_ids = session.exec(
        select(Member.project_id).where(Member.user_id == current_user.id)
    ).all()

    member_projects = session.exec(
        select(Project).where(Project.id.in_(member_project_ids))
    ).all()

    def serialize_project(project):
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": project.created_by,
            "members": [{"id": member.user_id} for member in project.members],
        }

    if current_user.role == "admin":
        created_projects = session.exec(
            select(Project).where(Project.created_by == current_user.id)
        ).all()

        if not created_projects and not member_projects:
            return {"message": "You don't have any projects. Please create one."}

        return {
            "created_projects": [serialize_project(p) for p in created_projects],
            "member_projects": [serialize_project(p) for p in member_projects],
        }

    if not member_projects:
        return {"message": "No project assigned to you."}

    return {"member_projects": [serialize_project(p) for p in member_projects]}


@router.post("/")
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_admin_user),
):
    db_project = Project(
        name=project.name,
        description=project.description,
        created_by=user.id,
    )
    session.add(db_project)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        if "uq_project_name_user" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project with name '{project.name}' already exists for this user.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database integrity error.",
        )

    session.refresh(db_project)

    for user_id in project.members or []:
        member_user = session.get(User, user_id)
        if not member_user:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found."
            )
        session.add(Member(user_id=user_id, project_id=db_project.id))

    session.commit()

    return {"message": "Project Created"}


@router.put("/{project_id}")
def update_project(
    project_id: int,
    project: ProjectCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_admin_user),
):
    db_project = session.exec(
        select(Project).where(Project.id == project_id, Project.created_by == user.id)
    ).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_project.name = project.name
    db_project.description = project.description
    session.add(db_project)
    session.commit()

    session.exec(delete(Member).where(Member.project_id == project_id))

    for user_id in project.members or []:
        member_user = session.get(User, user_id)
        if not member_user:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found."
            )
        session.add(Member(user_id=user_id, project_id=project_id))

    session.commit()

    return {"message": "Project Updated"}


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_admin_user),
):
    try:
        db_project = session.exec(
            select(Project).where(
                Project.id == project_id, Project.created_by == user.id
            )
        ).first()

        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        session.delete(db_project)
        session.commit()
        return {"message": "Project deleted"}

    except Exception as e:
        session.rollback()
        logger.exception("Error deleting project")
        raise HTTPException(status_code=500, detail=str(e))
