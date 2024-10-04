from decimal import Decimal

import pytest

from user_monitoring.models.user import User
from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_withdrawal import UserAlertConditionWithdrawal


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionWithdrawal()

    assert condition.code == 1100


def test_check_when_last_action_deposit_returns_false(high_risk_user: User) -> None:
    user_actions = [
        UserAction(high_risk_user.user_id, ActionType.DEPOSIT, Decimal(200), 1234000000),
    ]

    condition = UserAlertConditionWithdrawal()

    assert not condition.check(high_risk_user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, withdraw_amount",
    [("low_risk_user", Decimal(199.99)),
     ("normal_risk_user", Decimal(99.99)),
     ("high_risk_user", Decimal(49.99)),
     ])
def test_check_when_last_action_withdrawal_below_amount_limit_returns_false(
        user_fixture_name: str,
        withdraw_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(100), 1234000000),
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(100), 1234000001),
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(withdraw_amount), 1234000002)
    ]

    condition = UserAlertConditionWithdrawal()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, withdraw_amount",
    [("low_risk_user", Decimal(200.01)),
     ("normal_risk_user", Decimal(100.01)),
     ("high_risk_user", Decimal(50.01)),
     ])
def test_check_when_last_action_withdrawal_over_amount_limit_returns_true(
        user_fixture_name: str,
        withdraw_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)
    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(100), 1234000000),
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(100), 1234000001),
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(withdraw_amount), 1234000002)
    ]

    condition = UserAlertConditionWithdrawal()

    assert condition.check(user, user_actions)
