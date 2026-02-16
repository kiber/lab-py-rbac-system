from fastapi import status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import auth, models
from ..config import ALGORITHM, SECRET_KEY
from ..errors import raise_api_error


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.password):
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Invalid credentials",
        )
    return user


def create_token_response(user: models.User) -> dict[str, str]:
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user_from_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
    except JWTError:
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_token",
            message="Invalid credentials",
        )

    if not username:
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_token",
            message="Invalid credentials",
        )

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Invalid credentials",
        )
    return user
