import functools

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine, URL


from core.config import settings


@functools.lru_cache
def get_engine(url: str | URL | None = None, **kwargs) -> Engine:
    return create_engine(url or settings().postgres_dsn, pool_pre_ping=True, **kwargs)


def get_db() -> Session:
    db = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
    try:
        yield db
    finally:
        db.close()
