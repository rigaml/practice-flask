from typing import Generator
from unittest.mock import MagicMock

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
    def __init__(self, _):
        self.user_actions = []

    def add(self, user_action: UserAction) -> UserAction:
        self.user_actions.append(user_action)
        return user_action

    def get_by_id(self, user_id: int) -> list[UserAction]:
        return [user_action for user_action in self.user_actions if user_action.user_id == user_id]


class DummyUserRepo(UserRepository):
    def __init__(self, _):
        self.users = []

    def get_by_id(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user

        return User(user_id, "medium")


@ pytest.fixture
def app() -> Generator[Flask, None, None]:
    session_maker = MagicMock()

    repositories_registry = RepositoriesRegistry(
        user_action_repository=DummyUserActionRepo,
        user_repository=DummyUserRepo)

    app = create_app(session_maker, repositories_registry)
    with app.app_context():
        yield app


@ pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


TEST_USER_ID = 1


@ pytest.fixture
def low_risk_user():
    return User(user_id=TEST_USER_ID, risk="low")


@ pytest.fixture
def normal_risk_user():
    return User(user_id=TEST_USER_ID, risk="normal")


@ pytest.fixture
def high_risk_user():
    return User(user_id=TEST_USER_ID, risk="high")
