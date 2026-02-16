from fastapi import status
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..errors import raise_api_error


def register_user(db: Session, user_data: schemas.UserCreate) -> dict[str, str]:
    existing_user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()
    existing_email = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if existing_user:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="username_exists",
            message="Username already registered",
        )
    if existing_email:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="email_exists",
            message="Email already registered",
        )

    hashed = auth.hash_password(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


def assign_roles_to_user(db: Session, user_id: int, role_ids: list[int]):
    user = db.get(models.User, user_id)
    if user is None:
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="user_not_found",
            message="User not found",
        )

    if len(role_ids) != len(set(role_ids)):
        raise_api_error(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="duplicate_role_ids",
            message="role_ids contains duplicates",
        )

    roles = db.query(models.Role).filter(models.Role.id.in_(role_ids)).all()
    if len(roles) != len(role_ids):
        found_ids = {role.id for role in roles}
        missing_ids = [role_id for role_id in role_ids if role_id not in found_ids]
        raise_api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="roles_not_found",
            message="One or more roles were not found",
            details={"missing_ids": missing_ids},
        )

    user.roles = roles
    db.commit()
    db.refresh(user)
    return user


def ensure_user_has_permission(user: models.User, permission_name: str) -> None:
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
