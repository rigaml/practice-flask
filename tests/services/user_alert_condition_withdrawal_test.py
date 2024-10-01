from decimal import Decimal
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_withdrawal import UserAlertConditionWithdrawal


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionWithdrawal()

    assert condition.code == 1100


def test_check_when_last_action_deposit_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(200), 1234000000),
    ]

    condition = UserAlertConditionWithdrawal()

    assert not condition.check(user_actions)


def test_check_when_last_action_withdrawal_below_amount_limit_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(100), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(100), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(99.99), 1234000002)
    ]

    condition = UserAlertConditionWithdrawal()

    assert not condition.check(user_actions)


def test_check_when_last_action_withdrawal_over_amount_limit_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(100), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(100), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(100.01), 1234000002)
    ]

    condition = UserAlertConditionWithdrawal()

    assert condition.check(user_actions)
