from sqlalchemy.orm import Session

from app.core.db import session_local


def get_db() -> Session:
    """
    Get a database session.
    """
    db = session_local()
    try:
        yield db
        db.commit()

    finally:
        db.close()
