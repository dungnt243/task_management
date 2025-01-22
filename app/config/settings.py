import os
from functools import lru_cache
from typing import List, Union

from pydantic import PostgresDsn, computed_field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    AUTO_RELOAD: bool = False

    # App configuration
    APP_HOST: str = 'localhost'
    APP_PORT: int = 8000
    APP_NAME: str = '11STO2206'
    BACKEND_CORS_ORIGIN: Union[List[str], str] = ['*']
    API_PREFIX_URL: str = '/api/v1'
    APP_SECRET_KEY: str = ''
    SECRET_KEY: str = ''

    # Database configuration
    DB_HOST: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    MAIL_HOST: str
    MAIL_SENDER: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    FRONTEND_BASE_URL: str
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        sqlalchemy_uri = PostgresDsn.build(
            scheme='postgresql+psycopg2',
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=f"{self.DB_NAME or ''}",
            port=int(self.DB_PORT),
        ).unicode_string()
        os.environ['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
        return sqlalchemy_uri

    @field_validator('BACKEND_CORS_ORIGIN')
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.startswith('['):
                v = v[1 : len(v) - 1]
            if v.endswith(']'):
                v = v[: len(v) - 2]
            return [
                i.strip().replace('"', '').replace("'", '')
                for i in v.split(',')
            ]
        elif isinstance(v, (list, str)):
            return v

    LOG_INFO_FILE: str = 'logs/info/infos.log'
    LOG_ERROR_FILE: str = 'logs/error/errors.log'
    LOG_CUSTOM_FILE: str = 'logs/custom/customs.log'
    LOG_SQL_FILE: str = 'logs/sql/sql.log'
    LOG_ROTATION: str = '1 days'
    LOG_RETENTION: str = '20 days'
    LOG_FORMAT: str = (
        '[<level>{level}</level>] | '
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS} </green> | '
        '<cyan>{name}</cyan>:<cyan>{module}</cyan> | '
        '{line} | '
        '<level>{message}</level>'
    )

    LOG_DIAGNOSE: bool = True
    SQL_ECHO: bool = False

    class Config:
        case_sensitive = True
        env_file = '.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
