from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from common.db.session import get_session
from middleware.authentication import get_current_user
from models import User, Employee, Employer

from config.extensions.exception_handler import (
    BadRequest,
)

router = APIRouter()


@router.get('/list')
def get_list_employee(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if not isinstance(current_user, Employer):
        raise BadRequest(message='Only Employer can view list employees.')
    
    employees = session.query(Employee).all()
    
    return {
        # TODO: avoid n+1 query
        'data': [
            {   
                'id': employee.id,
                'name': employee.name,
                'total_tasks': employee.total_tasks,
                'completed_tasks': employee.completed_tasks,
            } for employee in employees
        ]
    }

@router.get('/me')
def get_detail_user(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return {
        'name': current_user.name,
        'email': current_user.email,
        'user_type': 'employee' if isinstance(current_user, Employee) else 'employer'
    }
    
    
