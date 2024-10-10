from decimal import Decimal

import pytest
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.services.user_alert_condition_transaction_window import UserAlertConditionTransactionWindow


def test_code_returns_expected_value() -> None:
    condition = UserAlertConditionTransactionWindow()

    assert condition.code == 500


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 10),
     ("normal_risk_user", 5),
     ("high_risk_user", 3),
     ])
def test_check_when_count_limit_transactions_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]

    condition = UserAlertConditionTransactionWindow()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 10),
     ("normal_risk_user", 5),
     ("high_risk_user", 3),
     ])
def test_check_when_count_limit_transactions_in_last_60_seconds_then_returns_false(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]
    user_actions.append(UserAction(user.user_id, ActionType.WITHDRAW, Decimal(1), 60000+1))

    condition = UserAlertConditionTransactionWindow()

    assert not condition.check(user, user_actions)


@pytest.mark.parametrize(
    "user_fixture_name, count",
    [("low_risk_user", 10),
     ("normal_risk_user", 5),
     ("high_risk_user", 3),
     ])
def test_check_when_more_than_count_limit_transactions_in_last_60_seconds_then_returns_true(
        user_fixture_name: str,
        count: int,
        request: pytest.FixtureRequest) -> None:

    user = request.getfixturevalue(user_fixture_name)

    user_actions = [
        UserAction(user.user_id, ActionType.DEPOSIT, Decimal(index+1), index) for index in range(count)
    ]

    user_actions.append(UserAction(user.user_id, ActionType.WITHDRAW, Decimal(1), 60000))

    condition = UserAlertConditionTransactionWindow()

    assert condition.check(user, user_actions)
