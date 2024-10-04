from typing import Generator

import pytest
from flask.testing import FlaskClient
from flask import Flask

from user_monitoring.app import create_app
from user_monitoring.models.user import User


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app()
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
