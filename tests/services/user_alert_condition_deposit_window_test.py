from decimal import Decimal
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_deposit_window import UserAlertConditionDepositWindow


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionDepositWindow()

    assert condition.code == 123


def test_check_when_last_action_withdrawal_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 1234000000),
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user_actions)


def test_check_when_one_deposit_and_on_limit_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(200), 12340000000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user_actions)


def test_check_when_one_deposit_and_over_limit_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(200.01), 12340000000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert condition.check(user_actions)


def test_check_when_multiple_deposits_and_below_limit_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(90), 12340000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(100), 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user_actions)


def test_check_when_multiple_deposits_and_over_limit_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(90), 12340000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(101), 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert condition.check(user_actions)


def test_check_when_deposits_and_withdrawls_then_only_consider_deposits_and_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(1, ActionType.WITHDRAW, Decimal(90), 12340000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(101), 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user_actions)


def test_check_when_deposits_outside_window_the_only_consider_deposits_inside_window_and_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(90), 12340000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(101), 12340030001)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user_actions)
