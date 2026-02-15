from sqlalchemy.orm import Session
from . import models

# -------- PERMISSIONS --------

def create_permission(db: Session, name: str):
    permission = models.Permission(name=name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def get_permissions(db: Session):
    return db.query(models.Permission).all()

def delete_permission(db: Session, permission_id: int):
    permission = db.query(models.Permission).get(permission_id)
    db.delete(permission)
    db.commit()


# -------- ROLES --------

def create_role(db: Session, name: str):
    role = models.Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_roles(db: Session):
    return db.query(models.Role).all()

def delete_role(db: Session, role_id: int):
    role = db.query(models.Role).get(role_id)
    db.delete(role)
    db.commit()


def assign_permissions_to_role(db: Session, role_id: int, permission_ids: list):
    role = db.query(models.Role).get(role_id)
    permissions = db.query(models.Permission).filter(
        models.Permission.id.in_(permission_ids)
    ).all()
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role


def assign_roles_to_user(db: Session, user_id: int, role_ids: list):
    user = db.query(models.User).get(user_id)
    roles = db.query(models.Role).filter(
        models.Role.id.in_(role_ids)
    ).all()
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user
