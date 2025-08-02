from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from schemas import UserCreate, UserLogin
from models import User
from database import get_session
from auth import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_pw, role="user")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "role": db_user.role}


@router.post("/adminRegister")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_pw, role="admin")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "role": db_user.role}


@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token, expire = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expired_At": expire.isoformat(),
    }
