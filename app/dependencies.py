from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import SessionLocal
from .errors import raise_api_error
from .models import User
from .config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_token",
            message="Invalid credentials",
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Invalid credentials",
        )
    return user

def has_permission(permission_name: str):
    def wrapper(user: User = Depends(get_current_user)):
        user_permissions = [
            perm.name
            for role in user.roles
            for perm in role.permissions
        ]
        if permission_name not in user_permissions:
            raise_api_error(
                status_code=status.HTTP_403_FORBIDDEN,
                code="permission_denied",
                message="Permission denied",
            )
        return True
    return wrapper
