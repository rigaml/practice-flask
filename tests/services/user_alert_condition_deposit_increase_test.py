from decimal import Decimal

import pytest
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_deposit_increase import UserAlertConditionDepositIncrease


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionDepositIncrease()

    assert condition.code == 300


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_last_action_withdrawal_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]
    user_actions.append(UserAction(user.user_id, ActionType.WITHDRAW, Decimal(1), count+1))

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_less_actions_than_deposit_required_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count-1)
    ]

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_last_deposits_do_not_increase_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(6), index) for index in range(count)
    ]

    condition = UserAlertConditionDepositIncrease()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_last_deposits_increase_count_limit_then_returns_true(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_deposits_previous_to_count_limit_did_not_increase_but_last_do_then_returns_true(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(1), 0)
    ]

    user_actions.extend([
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index+1) for index in range(count)
    ])

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_deposits_count_limit_increase_even_withdrawal_in_between_then_returns_true(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]
    user_actions.insert(1, UserAction(user.user_id, ActionType.WITHDRAW, Decimal(1), count+1))

    condition = UserAlertConditionDepositIncrease()

    assert condition.check(user, user_actions)
