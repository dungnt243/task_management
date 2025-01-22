from sqlalchemy import Column, ForeignKey, Table


from .base import CommonModel

role_permission = Table(
    'role_permission',
    CommonModel.metadata,
    Column('user_id', ForeignKey('roles.id')),
    Column('permission_id', ForeignKey('permissions.id')),
)
