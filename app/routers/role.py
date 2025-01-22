from fastapi.routing import APIRouter
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from common.db.engine import engine
from config.extensions.exception_handler import NotFound
from models import Roles
from schemas.role import RoleListResponse, RoleDetailResponse

router = APIRouter()


@router.get('', response_model=RoleListResponse)
def get_all_roles():
    with Session(engine) as session, session.begin():
        count = session.execute(select(func.count(Roles.id))).scalar()
        roles = session.execute(select(Roles)).scalars()
        response = RoleListResponse(total=count, data=roles)
        return response


@router.get('/{role_id}', response_model=RoleDetailResponse)
def get_role_item(role_id: int):
    with Session(engine) as session, session.begin():
        role = session.execute(
            select(Roles).where(Roles.id == role_id)
        ).scalar()
        if role:
            response = RoleDetailResponse.model_validate(role)
            return response
        else:
            return NotFound()
