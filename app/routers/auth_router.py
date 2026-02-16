from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import dependencies, schemas
from ..services import auth_service, user_service
from .common import error_responses

router = APIRouter()


@router.post(
    "/register",
    response_model=schemas.MessageResponse,
    responses=error_responses(409, 422, 500),
)
def register(user_data: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    return user_service.register_user(db, user_data)


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
    responses=error_responses(401, 422, 500),
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return auth_service.create_token_response(user)


@router.get(
    "/protected",
    response_model=schemas.MessageResponse,
    responses=error_responses(401, 403, 500),
)
def protected_route(permission: bool = Depends(dependencies.has_permission("read_data"))):
    return {"message": "You have access to this protected route"}
