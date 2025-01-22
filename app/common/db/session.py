from sqlalchemy.orm import Session

from .engine import engine


def get_session():
    session: Session = Session(engine)
    try:
        yield session
    finally:
        session.close()
