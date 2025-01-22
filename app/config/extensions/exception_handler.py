from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from .error_code import (
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE,
    HTTP_409_CONFLICT, HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_STATUS_CODES,
)


def http_status_message(status_code):
    return HTTP_STATUS_CODES.get(status_code, '')


def error_data(
    error_code,
    message,
):
    error = {'status': error_code, 'detail': str(message)}
    return error


class APIException(Exception):
    status_code = 500
    http_status_code = HTTP_500_INTERNAL_SERVER_ERROR
    message = None

    def __init__(
        self,
        status_code=None,
        message=None,
        *args,
    ):
        if self.status_code in self.http_status_code:
            self.status_code = status_code
        else:
            self.status_code = self.status_code
        if not message:
            message = self.http_status_code.get(
                status_code, http_status_message(self.status_code)
            )
        self.message = message

    @property
    def description(self):
        return error_data(
            error_code=self.status_code,
            message=self.message,
        )


class BadRequest(APIException):
    status_code = 400
    http_status_code = HTTP_400_BAD_REQUEST


class Unauthorized(APIException):
    status_code = 401
    http_status_code = HTTP_401_UNAUTHORIZED


class Forbidden(APIException):
    status_code = 403
    http_status_code = HTTP_403_FORBIDDEN


class NotFound(APIException):
    status_code = 404
    http_status_code = HTTP_404_NOT_FOUND


class MethodNotAllowed(APIException):
    status_code = 405
    http_status_code = HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptable(APIException):
    status_code = 406
    http_status_code = HTTP_406_NOT_ACCEPTABLE


class Conflict(APIException):
    status_code = 409
    http_status_code = HTTP_409_CONFLICT


class OverLimit(APIException):
    status_code = 413
    http_status_code = HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedMediaType(APIException):
    status_code = 415
    http_status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class UnprocessableEntity(APIException):
    status_code = 422
    http_status_code = HTTP_422_UNPROCESSABLE_ENTITY


class RateLimit(APIException):
    status_code = 429
    http_status_code = HTTP_429_TOO_MANY_REQUESTS


class InternalServerError(APIException):
    status_code = 500
    http_status_code = HTTP_500_INTERNAL_SERVER_ERROR


def api_error_handler(request, error):
    if isinstance(error, APIException):
        code = error.status_code
    elif isinstance(error, HTTPException):
        code = error.status_code
        if code == 404:
            error = NotFound(code)
        elif code == 405:
            error = MethodNotAllowed(405)
    elif isinstance(error, RequestValidationError):
        code = 400
        error = BadRequest(400000, 'Invalid input data')
    else:
        code = 500
        error.description = error_data(code, http_status_message(code))
    msg = 'HTTP_STATUS_CODE_{0}: {1}'.format(code, error.description)
    if code != 404:
        logger.error(msg)
    return JSONResponse(
        error.description,
        status_code=code,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
        },
    )
