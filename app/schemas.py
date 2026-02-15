from pydantic import BaseModel
from typing import List

class PermissionBase(BaseModel):
    name: str

class RoleBase(BaseModel):
    name: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
