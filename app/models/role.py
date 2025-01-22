from typing import Any, List

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from .base import CommonModel
from .user_role import user_role
from .role_permission import role_permission


class Roles(CommonModel):
    __tablename__ = 'roles'
    name = Column(String(length=50), nullable=False)
    key = Column(String(length=50), nullable=False, unique=True)
    description = Column(Text(), nullable=True)

    users: Mapped[List['Users']] = relationship(  # noqa: F821
        secondary=user_role, back_populates='roles'
    )
    permissions: Mapped[List['Permissions']] = relationship(  # noqa: F821
        secondary=role_permission, back_populates='roles'
    )
