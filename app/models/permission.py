from typing import Any, List

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from .base import CommonModel
from .role_permission import role_permission


class Permissions(CommonModel):
    __tablename__ = 'permissions'
    name = Column(String(length=50), nullable=False)
    key = Column(String(length=50), nullable=False, unique=True)
    description = Column(Text(), nullable=True)

    roles: Mapped[List['Roles']] = relationship(  # noqa: F821
        secondary=role_permission, back_populates='permissions'
    )
