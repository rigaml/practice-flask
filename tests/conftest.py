from contextlib import contextmanager
from typing import Generator
from unittest.mock import MagicMock, Mock

import pytest
from flask.testing import FlaskClient
from flask import Flask

from user_monitoring.app import create_app
from user_monitoring.data_access.repositories_registry import RepositoriesRegistry
from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.data_access.user_repository import UserRepository
from user_monitoring.DTOs.user import User
from user_monitoring.DTOs.user_action import UserAction


class DummyUserActionRepo(UserActionRepository):
    class_user_actions = []

    def __init__(self, _, __):
        pass

    def add(self, user_action: UserAction) -> UserAction:
        DummyUserActionRepo.class_user_actions.append(user_action)
        print(f"!!!!user_action: {user_action} ({len(DummyUserActionRepo.class_user_actions)})")
        return user_action

    def get_by_id(self, user_id: int) -> list[UserAction]:
        return [user_action for user_action in DummyUserActionRepo.class_user_actions if user_action.user_id == user_id]


class DummyUserRepo(UserRepository):
    class_users = []

    def __init__(self, _, __):
        pass

    def get_by_id(self, user_id: int) -> User:
        for user in DummyUserRepo.class_users:
            if user.user_id == user_id:
                return user

        return User(user_id, "medium")


@contextmanager
def mock_session_context():
    session = MagicMock()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def app() -> Generator[Flask, None, None]:

    repositories_registry = RepositoriesRegistry(
        user_action_repository=DummyUserActionRepo,
        user_repository=DummyUserRepo)

    app = create_app(mock_session_context, repositories_registry)
    with app.app_context():
        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


TEST_USER_ID = 1


@pytest.fixture
def low_risk_user():
    return User(user_id=TEST_USER_ID, risk="low")


@pytest.fixture
def normal_risk_user():
    return User(user_id=TEST_USER_ID, risk="normal")


@pytest.fixture
def high_risk_user():
    return User(user_id=TEST_USER_ID, risk="high")
