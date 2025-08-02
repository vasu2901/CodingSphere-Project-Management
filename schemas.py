from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ProjectCreate(BaseModel):
    name: str
    description: str
    members: Optional[List[int]] = []  # list of user IDs


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_by: int
    members: List[int] = []  # full user info here

    class Config:
        from_attributes = True
