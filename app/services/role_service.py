from fastapi import status
from sqlalchemy.orm import Session

from .. import models
from ..errors import raise_api_error


def create_permission(db: Session, name: str):
    existing_permission = (
        db.query(models.Permission).filter(models.Permission.name == name).first()
    )
    if existing_permission:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="permission_exists",
            message="Permission already exists",
        )

    permission = models.Permission(name=name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def list_permissions(db: Session):
    return db.query(models.Permission).all()


def delete_permission(db: Session, permission_id: int) -> None:
    permission = db.get(models.Permission, permission_id)
    if permission is None:
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="permission_not_found",
            message="Permission not found",
        )
    db.delete(permission)
    db.commit()


def create_role(db: Session, name: str):
    existing_role = db.query(models.Role).filter(models.Role.name == name).first()
    if existing_role:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="role_exists",
            message="Role already exists",
        )

    role = models.Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def list_roles(db: Session):
    return db.query(models.Role).all()


def delete_role(db: Session, role_id: int) -> None:
    role = db.get(models.Role, role_id)
    if role is None:
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="role_not_found",
            message="Role not found",
        )
    db.delete(role)
    db.commit()


def assign_permissions_to_role(db: Session, role_id: int, permission_ids: list[int]):
    role = db.get(models.Role, role_id)
    if role is None:
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="role_not_found",
            message="Role not found",
        )

    if len(permission_ids) != len(set(permission_ids)):
        raise_api_error(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="duplicate_permission_ids",
            message="permission_ids contains duplicates",
        )

    permissions = db.query(models.Permission).filter(
        models.Permission.id.in_(permission_ids)
    ).all()

    if len(permissions) != len(permission_ids):
        found_ids = {permission.id for permission in permissions}
        missing_ids = [
            permission_id
            for permission_id in permission_ids
            if permission_id not in found_ids
        ]
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="permissions_not_found",
            message="One or more permissions were not found",
            details={"missing_ids": missing_ids},
        )

    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role
