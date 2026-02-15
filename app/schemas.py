from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import List

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes for bcrypt")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class AssignPermission(BaseModel):
    permission_ids: List[int]


class AssignRole(BaseModel):
    role_ids: List[int]
