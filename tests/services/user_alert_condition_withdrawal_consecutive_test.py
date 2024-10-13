from decimal import Decimal

import pytest
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_withdrawal_consecutive import UserAlertConditionWithdrawalConsecutive


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionWithdrawalConsecutive()

    assert condition.code == 30


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_less_than_count_limit_withdrawals_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(index+1), index) for index in range(count-1)
    ]

    condition = UserAlertConditionWithdrawalConsecutive()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_one_deposit_in_last_count_limit_operations_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(1), 0)
    ]
    user_actions.extend([
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(index+1), index+1) for index in range(count-1)
    ])

    condition = UserAlertConditionWithdrawalConsecutive()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 6),
     ("normal_risk_user", 3),
     ("high_risk_user", 2),
     ])
def test_check_when_last_count_limit_actions_are_withdrawals_then_returns_true(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.WITHDRAW, Decimal(index+1), index) for index in range(count)
    ]

    condition = UserAlertConditionWithdrawalConsecutive()

    assert condition.check(user, user_actions)
