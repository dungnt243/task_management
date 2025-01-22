from fastapi import APIRouter

from .authentication import router as authentication_router
from .employee import router as employee_router
from .task import router as task_router

router = APIRouter()

router.include_router(authentication_router, prefix='', tags=['Authentication'])
router.include_router(employee_router, prefix='/employee', tags=['Employee'])
router.include_router(task_router, prefix='/task', tags=['Task'])
