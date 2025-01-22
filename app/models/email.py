from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship

from .base import CommonModel

class EmailType(str, Enum):
    RESET_PASSWORD = 'reset_password'

class Email(CommonModel):
    __tablename__ = 'email'
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='emails')
    created_at = Column(DateTime, nullable=True)
    is_user_password_changed = Column(Boolean, default=False)
    type = Column(SQLAlchemyEnum(EmailType), default=EmailType.RESET_PASSWORD)
