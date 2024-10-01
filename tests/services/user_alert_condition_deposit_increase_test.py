from decimal import Decimal
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_deposit_increase import UserAlertConditionDepositIncrease


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionDepositIncrease()

    assert condition.code == 300


def test_check_when_last_action_withdrawal_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(3), 1234000002),
        UserAction(1, ActionType.WITHDRAW, Decimal(1), 123456784),
    ]

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user_actions)


def test_check_when_less_actions_than_deposit_required_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000001)
    ]

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user_actions)


def test_check_when_last_deposits_do_not_increase_returns_false() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000002),
    ]

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user_actions)


def test_check_when_last_deposits_increase_increase_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(3), 1234000002),
    ]

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user_actions)


def test_check_when_last_deposits_increase_but_previous_dont_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000001),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000002),
        UserAction(1, ActionType.DEPOSIT, Decimal(3), 1234000003),
    ]

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user_actions)


def test_check_when_deposits_increase_and_withdrawal_between_returns_true() -> None:
    user_actions = [
        UserAction(1, ActionType.DEPOSIT, Decimal(1), 1234000000),
        UserAction(1, ActionType.DEPOSIT, Decimal(2), 1234000001),
        UserAction(1, ActionType.WITHDRAW, Decimal(2), 1234000002),
        UserAction(1, ActionType.DEPOSIT, Decimal(3), 1234000003),
    ]

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user_actions)
