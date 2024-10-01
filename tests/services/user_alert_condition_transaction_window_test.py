from decimal import Decimal
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_transaction_window import UserAlertConditionTransactionWindow


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionTransactionWindow()

    assert condition.code == 5


def test_check_given_5_or_less_transactions_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000002),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000003),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000004)
    ]

    condition = UserAlertConditionTransactionWindow()

    assert not condition.check(user_actions)


def test_check_given_only_5_transactions_in_last_60_seconds_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000002),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000003),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000004),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234060001)
    ]

    condition = UserAlertConditionTransactionWindow()

    assert not condition.check(user_actions)


def test_check_given_more_than_5_transactions_in_last_60_seconds_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000002),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000003),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000004),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234060000)
    ]

    condition = UserAlertConditionTransactionWindow()

    assert condition.check(user_actions)
