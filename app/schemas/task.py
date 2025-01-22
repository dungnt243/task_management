from typing import Optional
import re

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    status: str
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


class TaskListFilterCriteria(BaseModel):
    assignee_id: Optional[int] = None
    status: Optional[str] = None


class TaskListSortCriteria(BaseModel):
    criteria: Optional[str] = None
    type: Optional[str] = 'desc'


class TaskListSortFilterCriteria(BaseModel):
    filter_criteria: Optional[TaskListFilterCriteria] = None
    order_criteria: Optional[TaskListSortCriteria] = None
