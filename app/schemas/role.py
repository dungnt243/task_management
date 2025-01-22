from typing import List

from pydantic import BaseModel

from models import Roles


class RoleResponse(BaseModel):
    id: int
    name: str
    key: str
    description: str = None

    class Config:
        from_attributes = True
        populate_by_name = True


class RoleListResponse(BaseModel):
    total: int = 0
    data: List[RoleResponse] = []


class NestedPermissionResponse(BaseModel):
    id: int
    key: str
    name: str
    description: str = None

    class Config:
        from_attributes = True
        populate_by_name = True


class RoleDetailResponse(RoleResponse):
    permissions: List[NestedPermissionResponse] = None
