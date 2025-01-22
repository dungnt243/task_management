from fastapi import APIRouter
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import Depends

from common.db.session import get_session
from middleware.authentication import get_current_user
from models import (
    User,
    Employee,
    Employer,
    Task,
)
from models.task import TaskStatus

from config.extensions.exception_handler import (
    BadRequest,
)
from schemas.task import TaskListSortFilterCriteria
from loguru import logger

from schemas.task import (
    CreateTaskSchema,
    UpdateTaskSchema
)


router = APIRouter()


ORDER_CRITERIA_MAPPING = {
    'created_date': {
        'desc': Task.created_date.desc(),
        'asc': Task.created_date.asc(),
    },
    'due_date': {
        'desc': Task.due_date.desc(),
        'asc': Task.due_date.asc(),
    },
    'status': {
        'desc': Task.status.desc(),
        'asc': Task.status.asc(),
    },
    
}


@router.post('/create')
def create_task(
    form_data: CreateTaskSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if not isinstance(current_user, Employer):
        raise BadRequest(message='Only Employer can create task.')
    
    assignee_id = form_data.assignee_id
    
    if assignee_id:
        employee = session.query(Employee).filter(
            Employee.id == assignee_id
        ).first()
        if not employee:
            logger.error(f'Employee not found id = {assignee_id}')
            raise BadRequest(f'Employee not found id = {assignee_id}')
    
    task = Task(
        title=form_data.title,
        description=form_data.description,
        status=form_data.status,
        assignee_id=assignee_id or None,
        created_by_id=current_user.id,
        start_date=form_data.start_date,
        due_date=form_data.due_date
    )
    
    session.add(task)
    session.commit()
    
    return {
        'message': 'Task is created successfully'
    }
    

@router.post('/update/{task_id}')
def update_task(
    task_id: int,
    form_data: UpdateTaskSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    task = session.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise BadRequest(message=f'Invalid Task id = {task_id}')
    
    if (
        isinstance(current_user, Employee)
        and task.assignee_id != current_user.id
    ):
        raise BadRequest(message='Empployee can only update the tasks that assigned to them.')
    
    if form_data.assignee_id:
        assignee = session.query(Employee).filter(Employee.id == form_data.assignee_id).first()
        if not assignee:
            raise BadRequest(message=f'Invalid employee id = {form_data.assignee_id}')
    else:
        form_data.assignee_id = None
    
    task_data = form_data.dict(exclude_unset=True)
    for key, value in task_data.items():
        if value is not None:
            setattr(task, key, value)
    session.add(task)
    session.commit()
    
    return {
        'message': 'Task is updated successfully'
    }


@router.get('/detail/{task_id}')
def get_task_detail(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    task = session.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise BadRequest(message=f'Invalid Task id = {task_id}')
    
    if (
        isinstance(current_user, Employee)
        and current_user.id != task.assignee_id
    ):
        raise BadRequest(message='Empployee can only view the tasks that assigned to them.')
    
    assignee = task.assignee
    created_user = task.created_by
    
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'assignee': {
            'id': assignee.id,
            'name': assignee.name,
        } if assignee else None,
        'created_date': task.created_date,
        'start_date': task.start_date,
        'due_date': task.due_date,
        'created_user': {
            'id': created_user.id,
            'name': created_user.name,
        }
    }

# TODO: filter by assignee, status
# sort by create_date, due_date, status
@router.post('/list')
def list_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
    filter_sort_params: Optional[TaskListSortFilterCriteria] = None,
):
    if isinstance(current_user, Employee):
        list_tasks_query = session.query(Task).filter(Task.assignee_id == current_user.id)
    else:
        list_tasks_query = session.query(Task)
    
    if filter_sort_params:
        filter_sort_params = filter_sort_params.model_dump()
        filter_criteria = filter_sort_params.get('filter_criteria')
        order_criteria = filter_sort_params.get('order_criteria')
        if filter_criteria:
            if filter_criteria.get('assignee_id'):
                list_tasks_query = list_tasks_query.filter(Task.assignee_id == filter_criteria.get('assignee_id'))
            if filter_criteria.get('status'):
                list_tasks_query = list_tasks_query.filter(Task.status == filter_criteria.get('status'))
        if order_criteria:
            if order_criteria.get('criteria'):
                list_tasks_query = list_tasks_query.order_by(
                    ORDER_CRITERIA_MAPPING.get(
                        order_criteria.get('criteria'),
                        'created_date'
                    )\
                    .get(
                        order_criteria.get('type'),
                        'desc'
                    )
                )
        else:
            list_tasks_query = list_tasks_query.order_by(Task.id.asc())
    else:
        list_tasks_query = list_tasks_query.order_by(Task.id.asc())
    list_tasks = list_tasks_query.all()
    return {
        'data': [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'assignee': {
                    'id': task.assignee.id,
                    'name': task.assignee.name,
                } if task.assignee else None,
                'created_date': task.created_date,
                'start_date': task.start_date,
                'due_date': task.due_date,
                'created_user': {
                    'id': task.created_by.id,
                    'name': task.created_by.name,
                }
            } for task in list_tasks
        ]
    }
    
    
    
    
    
    