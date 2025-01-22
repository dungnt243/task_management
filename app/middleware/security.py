from datetime import datetime

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config.extensions.exception_handler import (
    Unauthorized,
)

from config.settings import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=403, detail='Invalid authentication scheme.')
        is_token_valid = self.verify_jwt(credentials.credentials)
        if not is_token_valid:
            raise HTTPException(status_code=403, detail='Invalid token.')
        return credentials

    def verify_jwt(self, token: str) -> bool:
        return bool(self.decode_jwt(token))

    def decode_jwt(self, token: str) -> dict:
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            expired_time = datetime.strptime(decoded_data['expired_time'], '%m/%d/%Y, %H:%M:%S')
            if expired_time < datetime.now():
                return Unauthorized(message='Access token is expired.')
            if decoded_data.get('is_refresh_token'):
                return Unauthorized(message='Access token is Invalid.')
            return decoded_data
        except jwt.ExpiredSignatureError:
            return {}
