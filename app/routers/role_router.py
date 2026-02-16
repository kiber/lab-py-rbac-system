from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import dependencies, schemas
from ..services import role_service
from .common import error_responses

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post(
    "/",
    response_model=schemas.RoleResponse,
    responses=error_responses(409, 422, 500),
)
def create_role(role: schemas.RoleCreate, db: Session = Depends(dependencies.get_db)):
    return role_service.create_role(db, role.name)


@router.get(
    "/",
    response_model=list[schemas.RoleResponse],
    responses=error_responses(500),
)
def list_roles(db: Session = Depends(dependencies.get_db)):
    return role_service.list_roles(db)


@router.delete(
    "/{role_id}",
    response_model=schemas.MessageResponse,
    responses=error_responses(404, 422, 500),
)
def delete_role(role_id: int, db: Session = Depends(dependencies.get_db)):
    role_service.delete_role(db, role_id)
    return {"message": "Role deleted"}


@router.put(
    "/{role_id}/permissions",
    response_model=schemas.RoleResponse,
    responses=error_responses(400, 404, 422, 500),
)
def assign_permissions(
    role_id: int,
    data: schemas.AssignPermission,
    db: Session = Depends(dependencies.get_db),
):
    return role_service.assign_permissions_to_role(db, role_id, data.permission_ids)
