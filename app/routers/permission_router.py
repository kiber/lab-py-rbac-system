from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import dependencies, schemas
from ..services import role_service
from .common import error_responses

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post(
    "/",
    response_model=schemas.PermissionResponse,
    responses=error_responses(409, 422, 500),
)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(dependencies.get_db),
):
    return role_service.create_permission(db, permission.name)


@router.get(
    "/",
    response_model=list[schemas.PermissionResponse],
    responses=error_responses(500),
)
def list_permissions(db: Session = Depends(dependencies.get_db)):
    return role_service.list_permissions(db)


@router.delete(
    "/{permission_id}",
    response_model=schemas.MessageResponse,
    responses=error_responses(404, 422, 500),
)
def delete_permission(permission_id: int, db: Session = Depends(dependencies.get_db)):
    role_service.delete_permission(db, permission_id)
    return {"message": "Permission deleted"}
