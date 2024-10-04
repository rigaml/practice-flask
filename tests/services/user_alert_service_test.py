from decimal import Decimal
from unittest.mock import MagicMock

from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.services.user_alert_service import UserAlertService


def test_handle_alerts_when_no_conditions_met_returns_alert_false() -> None:

    user_action = UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000)

    mock_logger = MagicMock()
    mock_user_repository = MagicMock()
    mock_user_action_repository = MagicMock()

    user_alert_service = UserAlertService(
        user_alert_conditions=[],
        user_repository=mock_user_repository,
        user_action_repository=mock_user_action_repository,
        logger=mock_logger
    )

    user_alert = user_alert_service.handle_alerts(user_action)

    mock_logger.info.assert_called_once()

    mock_user_repository.get_by_id.assert_called_once_with(user_action.user_id)

    mock_user_action_repository.create.assert_called_once_with(user_action)
    mock_user_action_repository.get_all.assert_called_once_with(user_action.user_id)

    assert user_alert == {"alert": False, "alert_codes": [], "user_id": user_action.user_id}


def test_handle_alerts_when_multiple_conditions_met_returns_alert_with_codes() -> None:

    user_action = UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000)

    mock_logger = MagicMock()
    mock_user_action_repository = MagicMock()
    mock_user_repository = MagicMock()

    mock_alert_true_code11 = MagicMock(spec=UserAlertCondition)
    mock_alert_true_code11.check.return_value = True
    mock_alert_true_code11.code = 11

    mock_alert_false_code22 = MagicMock(spec=UserAlertCondition)
    mock_alert_false_code22.check.return_value = False
    mock_alert_false_code22.code = 22

    mock_alert_true_code33 = MagicMock(spec=UserAlertCondition)
    mock_alert_true_code33.check.return_value = True
    mock_alert_true_code33.code = 33

    user_alert_conditions: list[UserAlertCondition] = [
        mock_alert_true_code11,
        mock_alert_false_code22,
        mock_alert_true_code33
    ]

    user_alert_service = UserAlertService(
        user_alert_conditions=user_alert_conditions,
        user_action_repository=mock_user_action_repository,
        user_repository=mock_user_repository,
        logger=mock_logger
    )

    user_alert = user_alert_service.handle_alerts(user_action)

    mock_logger.info.assert_called_once()

    mock_user_repository.get_by_id.assert_called_once_with(user_action.user_id)

    mock_user_action_repository.create.assert_called_once_with(user_action)
    mock_user_action_repository.get_all.assert_called_once_with(user_action.user_id)

    assert user_alert == {"alert": True, "alert_codes": [11, 33], "user_id": user_action.user_id}
