from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

from app.core.security import create_access_token, verify_password, hash_password

def create_user(db: Session, user_data: UserCreate) -> User:
    password_hash = hash_password(user_data.password)
    user = User(username=user_data.username, email=user_data.email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)

    return db.scalar(statement)

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = db.scalar(statement)

    if user is None or not verify_password(password, user.password_hash):
        return None 

    return user