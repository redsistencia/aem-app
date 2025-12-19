from src.db.session import SessionLocal
from sqlalchemy.orm import Session

# Dependencias de auth
def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
