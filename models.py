from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey
from datetime import datetime
from sqlalchemy import UniqueConstraint


class Member(SQLModel, table=True):
    user_id: int = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    )
    project_id: int = Field(
        sa_column=Column(ForeignKey("project.id", ondelete="CASCADE"), primary_key=True)
    )

    user: Optional["User"] = Relationship(back_populates="memberships")
    project: Optional["Project"] = Relationship(back_populates="members")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="user")

    projects: List["Project"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    memberships: List[Member] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )


class Project(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("name", "created_by", name="uq_project_name_user"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    created_by: int = Field(sa_column=Column(ForeignKey("user.id", ondelete="CASCADE")))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    creator: Optional[User] = Relationship(back_populates="projects")
    members: List[Member] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
