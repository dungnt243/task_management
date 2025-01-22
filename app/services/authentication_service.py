from datetime import datetime, timedelta

import jwt
from config.settings import settings
from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return password_context.hash(password + settings.SECRET_KEY)

def verify_password(password: str, hashed_password: str):
    return password_context.verify(
        password + settings.SECRET_KEY,
        hashed_password,
    )

def create_token(data: dict, expires_delta: timedelta):
    expired_time = datetime.now() + expires_delta
    data.update({'expired_time': expired_time.strftime('%m/%d/%Y, %H:%M:%S')})
    encoded_jwt = jwt.encode(
        data,
        settings.SECRET_KEY,
    )
    return encoded_jwt
