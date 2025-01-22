from typing import List

from sqlalchemy import(
    Column,
    String,
    func,
    select,
)

from sqlalchemy.orm import relationship, Session

from .base import CommonModel
from models.task import TaskStatus, Task
# from common.db.engine import engine


class User(CommonModel):
    __tablename__ = 'user'
    __abstract__ = True
    
    name = Column(String(length=50), nullable=True)
    email = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)
    

class Employer(User):
    __tablename__ = 'employer'
    
    created_tasks = relationship('Task', back_populates='created_by')


class Employee(User):
    __tablename__ = 'employee'
    
    tasks = relationship('Task', back_populates='assignee')
    
    @property
    def total_tasks(self):
        return 1
    

    @property
    def completed_tasks(self):
        return 1

