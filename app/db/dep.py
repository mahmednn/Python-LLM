from .database import session_local, engine


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
