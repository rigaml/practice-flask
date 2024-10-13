from decimal import Decimal

import pytest
from user_monitoring.DTOs.user import User
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_deposit_window import UserAlertConditionDepositWindow


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionDepositWindow()

    assert condition.code == 123


def test_check_when_last_action_withdrawal_then_returns_false(high_risk_user: User) -> None:
    user_actions = [
        UserAction(high_risk_user.user_id, ActionType.WITHDRAW, Decimal(1000), 1234000000),
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(high_risk_user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400)),
     ("normal_risk_user", Decimal(200)),
     ("high_risk_user", Decimal(100)),
     ])
def test_check_when_one_deposit_and_on_limit_then_returns_false(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(deposit_amount), 12340000000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400.01)),
     ("normal_risk_user", Decimal(200.01)),
     ("high_risk_user", Decimal(100.01)),
     ])
def test_check_when_one_deposit_and_over_limit_then_returns_true(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(deposit_amount), 12340000000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400)),
     ("normal_risk_user", Decimal(200)),
     ("high_risk_user", Decimal(100)),
     ])
def test_check_when_multiple_deposits_and_below_limit_then_returns_false(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(20), 12340000001),
        UserAction(user.user_id, ActionType.DEPOSIT, deposit_amount - 30, 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400)),
     ("normal_risk_user", Decimal(200)),
     ("high_risk_user", Decimal(100)),
     ])
def test_check_when_multiple_deposits_and_over_limit_then_returns_true(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(0.01), 12340000000),
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(0.02), 12340000001),
        UserAction(user.user_id, ActionType.DEPOSIT, deposit_amount, 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400)),
     ("normal_risk_user", Decimal(200)),
     ("high_risk_user", Decimal(100)),
     ])
def test_check_when_deposits_and_withdrawls_and_deposits_below_limit_then_returns_false(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(10), 12340000000),
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(90), 12340000001),
        UserAction(user.user_id, ActionType.DEPOSIT, deposit_amount - 10, 12340030000)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, deposit_amount",
    [("low_risk_user", Decimal(400)),
     ("normal_risk_user", Decimal(200)),
     ("high_risk_user", Decimal(100)),
     ])
def test_check_when_deposits_outside_window_the_only_consider_deposits_inside_window_and_then_returns_false(
        user_fixture_name: str,
        deposit_amount: Decimal,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, deposit_amount, 12340000000),
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(90), 12340000001),
        UserAction(user.user_id, ActionType.DEPOSIT, deposit_amount - 90, 12340030001)
    ]

    condition = UserAlertConditionDepositWindow()

    assert not condition.check(user, user_actions)
