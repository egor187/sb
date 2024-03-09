import os
import pytest
from freezegun import freeze_time
from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.models import Link
from db.repositories.visited_links import VisitRepository
from core.config import settings
from db.session import get_engine, get_db
from fastapi.testclient import TestClient
from tests.utils import drop_database, database_exists, create_database
from main import app

import alembic.command
from alembic.config import Config


@pytest.fixture
def repository():
    return VisitRepository()


@pytest.fixture(scope="session")
def mock_settings() -> None:
    settings.cache_clear()
    os.environ["ENVIRONMENT"] = "test"
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5433"


@pytest.fixture(scope="session")
def db_engine(mock_settings):
    if database_exists(settings().postgres_dsn):
        drop_database(settings().postgres_dsn)

    create_database(settings().postgres_dsn)

    engine = get_engine()
    engine.dispose()

    yield engine

    engine.dispose()
    # drop_database(settings().postgres_dsn)


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config(os.path.join(settings().BASE_DIR, "alembic.ini"))
    config.set_main_option("script_location", os.path.join(settings().BASE_DIR, "migrations"))
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="function")
def db_session(db_engine, apply_migrations):
    with db_engine.connect() as conn:
        with conn.begin() as transaction:
            session = Session(bind=conn, expire_on_commit=False)

            yield session

            transaction.rollback()


@pytest.fixture(scope="function")
def api_client(
    db_session: Session
):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def links(request, db_session):
    links_marker = request.node.get_closest_marker("links")
    links = links_marker.args[0] if links_marker else [
        "https://www.test.com",
        "https://www.test2.com",
        "https://www.test3.com",
    ]
    created_at_marker = request.node.get_closest_marker("created_at")
    created_at = created_at_marker.args[0] if created_at_marker else "2000-01-01"
    with freeze_time(created_at):
        db_session.execute(
            insert(Link), [
                {'url': link} for link in links
            ]
        )
        db_session.commit()
