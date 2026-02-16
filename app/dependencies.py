from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .services import auth_service, user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return auth_service.get_current_user_from_token(db, token)

def has_permission(permission_name: str):
    def wrapper(user: User = Depends(get_current_user)):
        user_service.ensure_user_has_permission(user, permission_name)
        return True
    return wrapper
