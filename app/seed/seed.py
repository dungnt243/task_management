import json
import os

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.logger import custom_logger as logger
from common.db.engine import engine
from models import Roles, Permissions


ROOT_PATH = os.path.join(os.getcwd(), 'seed', 'data_seed')
PERMISSION_FILE_NAME = 'permissions.json'
ROLE_FILE_NAME = 'roles.json'


def seed_permission():
    file_path = os.path.join(ROOT_PATH, PERMISSION_FILE_NAME)
    with open(file_path, 'r') as file:
        data = json.load(file)
    logger.info(f'Found {len(data)} permissions. Importing')

    with Session(engine) as session, session.begin():
        stmt = select(Permissions)
        existed = session.execute(stmt).scalar()
        if existed:
            logger.info('Found existing data in Permissions table. Skipping')
        else:
            permission_list = []
            for item in data:
                permission_list.append(Permissions(**item))
                logger.info(f"Adding permissions {item['name']}")
            session.add_all(permission_list)
            session.commit()
            logger.info('Importing permissions successfully')


def seed_roles():
    file_path = os.path.join(ROOT_PATH, ROLE_FILE_NAME)
    with open(file_path, 'r') as file:
        data = json.load(file)
    logger.info(f'Found {len(data)} roles. Importing')

    with Session(engine) as session, session.begin():
        stmt = select(Roles)
        existed = session.execute(stmt).scalar()
        if existed:
            logger.info('Found existing data in Roles table. Skipping')
        else:
            all_permissions = session.query(Permissions).all()
            for item in data:
                permissions = (
                    item.pop('permissions') if 'permissions' in item else []
                )
                role = Roles(**item)
                if permissions == 'all':
                    role.permissions = all_permissions
                elif permissions:
                    permission_qs = (
                        session.query(Permissions)
                        .filter(Permissions.key.in_(permissions))
                        .all()
                    )
                    role.permissions = permission_qs
                logger.info(f'Saving role {role.name}')
                session.add(role)
            session.commit()


def run_data_seed():
    seed_permission()
    seed_roles()
