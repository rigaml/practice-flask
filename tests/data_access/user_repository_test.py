import logging
from unittest.mock import Mock

import pytest

from user_monitoring.DTOs.user import User
from user_monitoring.data_access.user_repository import UserRepository
from user_monitoring.models.user_model import UserModel


@pytest.fixture
def user_repository():
    mock_session = Mock()
    mock_logger = Mock(spec=logging.Logger)

    return UserRepository(session=mock_session, logger=mock_logger), mock_session, mock_logger


def test_get_by_id_when_user_exist_returns_user(user_repository) -> None:
    user_repo, mock_session, mock_logger = user_repository

    user = User(1, "high")

    mock_query = Mock()
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = user
    mock_session.query.return_value = mock_query

    result = user_repo.get_by_id(1)

    mock_logger.info.assert_called()

    mock_session.query.assert_called_once_with(UserModel)
    mock_query.filter_by.assert_called_once_with(user_id=1)

    assert result == user


def test_get_by_id_when_called_and_no_user_actions_retrieved_returns_empty_array(user_repository) -> None:
    user_repo, mock_session, mock_logger = user_repository

    user = None

    mock_query = Mock()
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = user
    mock_session.query.return_value = mock_query

    result = user_repo.get_by_id(1)

    mock_logger.info.assert_called()

    mock_session.query.assert_called_once_with(UserModel)
    mock_query.filter_by.assert_called_once_with(user_id=1)

    assert result == User(1, "medium")
