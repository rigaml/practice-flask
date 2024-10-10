from decimal import Decimal
import logging
from unittest.mock import Mock

import pytest

from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.models.user_action_model import UserActionModel


@pytest.fixture
def user_action_repository():
    mock_session = Mock()
    mock_logger = Mock(spec=logging.Logger)

    return UserActionRepository(session=mock_session, logger=mock_logger), mock_session, mock_logger


def test_add_adds_user_action(user_action_repository) -> None:
    user_action_repo, mock_session, mock_logger = user_action_repository

    user_action = UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000)

    result = user_action_repo.add(user_action)

    mock_logger.info.assert_called_once()

    mock_session.add.assert_called_once_with(
        UserActionModel(user_action.user_id, user_action.type, user_action.amount, user_action.time))
    mock_session.commit.assert_called_once()

    assert result == user_action


def test_get_all_when_user_actions_exist_returns_user_actions(user_action_repository) -> None:
    user_action_repo, mock_session, mock_logger = user_action_repository

    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001)
    ]

    mock_query = Mock()
    mock_query.filter_by.return_value = mock_query
    mock_query.all.return_value = user_actions
    mock_session.query.return_value = mock_query

    result = user_action_repo.get_by_id(1)

    mock_logger.info.assert_called()

    mock_session.query.assert_called_once_with(UserActionModel)
    mock_query.filter_by.assert_called_once_with(user_id=1)
    assert len(result) == 2

    assert result[0] == user_actions[0]
    assert result[1] == user_actions[1]


def test_get_all_when_no_user_actions_exist_returns_empty_array(user_action_repository) -> None:
    user_action_repo, mock_session, mock_logger = user_action_repository

    user_actions = []

    mock_query = Mock()
    mock_query.filter_by.return_value = mock_query
    mock_query.all.return_value = user_actions
    mock_session.query.return_value = mock_query

    result = user_action_repo.get_by_id(1)

    mock_logger.info.assert_called()

    mock_session.query.assert_called_once_with(UserActionModel)
    mock_query.filter_by.assert_called_once_with(user_id=1)
    assert len(result) == 0
