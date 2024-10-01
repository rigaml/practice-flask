from decimal import Decimal
from unittest.mock import MagicMock

from user_monitoring.data_access import user_action_repository
from user_monitoring.models.user_action import ActionType, UserAction


def test_create_when_called_adds_user_action() -> None:
    mock_logger = MagicMock()
    user_action = UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000)

    user_action_repo = user_action_repository.UserActionRepository(mock_logger)

    user_action_repo.create(user_action)

    mock_logger.info.assert_called_once()
    assert user_action in user_action_repo.user_actions_fake


def test_get_all_when_called_with_existing_user_id_returns_user_actions_for_id() -> None:
    mock_logger = MagicMock()

    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(2, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(3, ActionType.WITHDRAW, Decimal(1), 1234000001)
    ]

    user_action_repo = user_action_repository.UserActionRepository(mock_logger)

    for user_action in user_actions:
        user_action_repo.create(user_action)

    user_action_retrieved = user_action_repo.get_all(1)

    mock_logger.info.assert_called()
    assert len(user_action_retrieved) == 2


def test_get_all_when_called_with_non_existing_user_id_returns_empty_array() -> None:
    mock_logger = MagicMock()

    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(2, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(3, ActionType.WITHDRAW, Decimal(1), 1234000001)
    ]

    user_action_repo = user_action_repository.UserActionRepository(mock_logger)

    for user_action in user_actions:
        user_action_repo.create(user_action)

    user_action_retrieved = user_action_repo.get_all(33)

    mock_logger.info.assert_called()
    assert user_action_retrieved == []
