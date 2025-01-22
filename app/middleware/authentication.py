from typing import Annotated

from common.db.engine import engine
from config.extensions.exception_handler import Unauthorized
from routers.authentication import USER_TYPE_MAPPING
from sqlalchemy.orm import Session

from fastapi import Depends

from .security import JWTBearer

security = JWTBearer()

async def get_current_user(credentials: Annotated[str, Depends(security)]):
    decoded_jwt = security.decode_jwt(credentials.credentials)
    user_type = decoded_jwt.get('user_type')
    user_email = decoded_jwt.get('email')
    user_model = USER_TYPE_MAPPING.get(user_type)
    session = Session(engine)
    user = session.query(user_model).where(user_model.email == user_email).first()
    if user is None:
        raise Unauthorized(message='User not found')
    return user
