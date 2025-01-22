from config.settings import settings
from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from fastapi.requests import Request


def get_engine():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=40
    )
    return engine


engine = get_engine()


class SQLAlchemyPanel(BasePanel):
    async def add_engines(self, request: Request):
        self.engines.add(engine)
