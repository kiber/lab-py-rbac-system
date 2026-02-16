from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import dependencies, schemas
from ..services import user_service
from .common import error_responses

router = APIRouter(prefix="/users", tags=["users"])


@router.put(
    "/{user_id}/roles",
    response_model=schemas.UserResponse,
    responses=error_responses(400, 404, 422, 500),
)
def assign_roles(
    user_id: int,
    data: schemas.AssignRole,
    db: Session = Depends(dependencies.get_db),
):
    return user_service.assign_roles_to_user(db, user_id, data.role_ids)
