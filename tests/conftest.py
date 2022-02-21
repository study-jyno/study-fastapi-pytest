import pytest
from fastapi import Depends

from starlette.testclient import TestClient

from app import config
from app.database.core import engine, get_db, SessionLocal
from app.database.manage import create_all, delete_all

from .factories import (
    UserFactory,
    ItemFactory,
    UserCertificationFactory,
    ItemParentItemChildFactory,
)

from .database import Session


@pytest.fixture(scope="session")
def testapp():
    # we only want to use test plugins so unregister everybody else
    from app.main import app

    yield app


@pytest.fixture(scope="session")
def db():
    create_all()
    yield
    delete_all()


@pytest.fixture(scope="function", autouse=False)
def session(db):
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = Session
    session.begin_nested()
    yield session
    session.rollback()


# Create Dummy Data
@pytest.fixture(scope="session")
def dummy_db():
    create_all()
    yield


# Create Dummy Data
@pytest.fixture(scope="function", autouse=False)
def dummy_session(dummy_db):
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = Session
    yield session


@pytest.fixture(scope="function")
def client(testapp, session, client):
    yield TestClient(testapp)


@pytest.fixture
def user(session):
    return UserFactory()


@pytest.fixture
def user_certification(session):
    return UserCertificationFactory()


@pytest.fixture
def item(session):
    return ItemFactory()


@pytest.fixture
def item_parent_item_child(session):
    return ItemParentItemChildFactory()


@pytest.fixture
def item_parent_item_child_2(dummy_session):
    return ItemParentItemChildFactory()
