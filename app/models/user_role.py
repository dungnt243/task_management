from sqlalchemy import Column, ForeignKey, Table

from .base import CommonModel

user_role = Table(
    'user_role',
    CommonModel.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id')),
)
