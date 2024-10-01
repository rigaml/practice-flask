from decimal import Decimal
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_withdrawal_consecutive import UserAlertConditionWithdrawalConsecutive


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionWithdrawalConsecutive()

    assert condition.code == 30


def test_check_when_less_than_3_actions_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(2), 1234000001),
    ]

    condition = UserAlertConditionWithdrawalConsecutive()

    assert not condition.check(user_actions)


def test_check_when_one_deposit_in_last_actions_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(2), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(3), 1234000002)
    ]

    condition = UserAlertConditionWithdrawalConsecutive()

    assert not condition.check(user_actions)


def test_check_when_last_actions_withdrawal_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(2), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(3), 1234000002)
    ]

    condition = UserAlertConditionWithdrawalConsecutive()

    assert condition.check(user_actions)
