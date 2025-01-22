from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from models.task import TaskStatus


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    status: Optional[str] = TaskStatus.TODO
    assignee_id: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    
class UpdateTaskSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None


class UserSchema(BaseModel):
    id: int
    name: str


class DetailTaskSchema(BaseModel):
    id: int
    title: str
    description: str
    status: str
    assignee: Optional[UserSchema] = None
    created_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    created_user: Optional[UserSchema] = None


class ListTaskSchema(BaseModel):
    data: Optional[list[DetailTaskSchema]] = []


class TaskListFilterCriteria(BaseModel):
    assignee_id: Optional[int] = None
    status: Optional[str] = None


class TaskListSortCriteria(BaseModel):
    criteria: Optional[str] = None
    type: Optional[str] = 'desc'


class TaskListSortFilterCriteria(BaseModel):
    filter_criteria: Optional[TaskListFilterCriteria] = None
    order_criteria: Optional[TaskListSortCriteria] = None
