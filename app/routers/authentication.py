from fastapi import APIRouter

from config.extensions import exception_handler as custom_exec
from config.logger import logger
from schemas.user import (
    UserRegisterFormData,
)
from config.settings import settings
from sqlalchemy.orm import Session
from common.db.engine import engine
from models import User, Employee, Employer
from config.extensions.exception_handler import (
    BadRequest,
    Unauthorized,
)

from schemas.user import (
    UserLoginFormData,
    UserRegisterFormData,
)

from datetime import datetime, timedelta

from services.authentication_service import (
    create_token,
    hash_password,
    verify_password,
)

router = APIRouter()

USER_TYPE_MAPPING = {
    'employer': Employer,
    'employee': Employee,
}


@router.post('/register')
def register(form_data: UserRegisterFormData):
    email = form_data.email
    user_type = form_data.user_type
    password = form_data.password
    with Session(engine) as session, session.begin():
        user_model = USER_TYPE_MAPPING.get(user_type)
        if not user_model:
            raise BadRequest(f'Invalid user type {user_type}. User_type should be "employee" or "employer"')
        existing_user = (
            session.query(Employer).where(Employer.email == email).first()
            or session.query(Employee).where(Employee.email == email).first()
        )
        # Check if the user already exists
        if existing_user:
            raise BadRequest(message='User already exists.')

        hashed_password = hash_password(password)
        new_user = user_model(
            email=email,
            password=hashed_password,
            name=email.split('@')[0],
        )
        session.add(new_user)
        session.commit()

    return {'message': 'User registered successfully'}


@router.post('/login')
def login(form_data: UserLoginFormData):
    email = form_data.email
    password = form_data.password
    with Session(engine) as session, session.begin():
        user = (
            session.query(Employer).where(Employer.email == email).first()
            or session.query(Employee).where(Employee.email == email).first()
        )
        if user is None:
            raise Unauthorized(status_code=401, message='User is not found.')

        if not verify_password(password, user.password):
            raise Unauthorized(message='Password is invalid.')

        access_token = create_token(
            data={
                'email': email,
                'user_type': 'employee' if isinstance(user, Employee) else 'employer'
            },
            expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
        )

        return {
            'access_token': access_token,
        }
