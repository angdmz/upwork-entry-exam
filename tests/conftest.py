from typing import List
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from app import get_app
from common import ObjRef
from logic.users import User
from session.connection import Base
from settings import DatabaseSettings, AppSettings


@pytest.fixture
def db_settings():
    return DatabaseSettings()


class PrefixTestClient(TestClient):
    def __init__(self, starlette_app, prefix, **kwargs):
        super().__init__(starlette_app, **kwargs)
        self.__prefix = prefix

    def request(self, method, url, **kwargs):
        return super().request(method, self.__prefix + url, **kwargs)


@pytest.fixture
def app_settings():
    return AppSettings()


@pytest.fixture
def db_test_settings():
    return DatabaseSettings(db_url_prefix="postgresql")


@pytest.fixture
def db_session_tests(db_test_settings):
    database_url = URL.create(
        drivername=db_test_settings.db_url_prefix,
        username=db_test_settings.db_username,
        password=db_test_settings.db_password,
        host=db_test_settings.db_hostname,
        port=db_test_settings.db_port,
        database=db_test_settings.db_name,
    )
    engine = create_engine(database_url)
    with Session(engine) as session:
        yield session
    session.close()


@pytest.fixture
def client(
    app_settings,
    db_settings,
    db_session_tests
) -> TestClient:

    async def lifespan(application: FastAPI):
        yield

    app = get_app(app_settings, lifespan)
    with PrefixTestClient(app, app_settings.path_prefix) as client:
        # Default customer for most unit tests
        yield client

    # Reset overrides
    app.dependency_overrides = {}
    tables = Base.metadata.tables
    db_session_tests.begin()
    with db_session_tests.connection() as conn:
        # disable foreign keys
        conn.execute(text("BEGIN TRANSACTION;"))
        for table in tables:
            try:
                conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
            except ProgrammingError as e:
                print(e)
        conn.execute(text("END TRANSACTION;"))


@pytest.fixture
def user(client) -> [UUID, User]:

    user = User(email="some_email@gmail.com")
    res = client.post("/users", data=user.model_dump_json())
    user_id = ObjRef.model_validate(res.json()).id
    get_res = client.get(f"/users/{user_id}")
    user_a = User.model_validate(get_res.json())

    return user_id, user_a
