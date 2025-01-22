from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
    DateTime,
    func,
)
from enum import Enum
from sqlalchemy.orm import relationship
from .base import CommonModel


class TaskStatus(str, Enum):
    TODO = 'todo'
    INPROGRESS = 'inprogress'
    COMPLETED = 'completed'


class Task(CommonModel):
    __tablename__ = 'task'

    title = Column(String(length=200))
    description = Column(String(length=1000), nullable=True)
    status  = Column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO
    )
    assignee_id = Column(Integer, ForeignKey('employee.id'), nullable=True)
    created_by_id = Column(Integer, ForeignKey('employer.id'))
    created_date = Column(DateTime, default=func.now())
    start_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    
    assignee = relationship('Employee', back_populates='tasks')
    created_by = relationship('Employer', back_populates='created_tasks')
    
