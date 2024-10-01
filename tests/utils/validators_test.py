
from decimal import Decimal
import pytest

from user_monitoring.models.user_action import ActionType, UserAction
from user_monitoring.utils.validators import convert_to_action_type, validate_user_event


def test_convert_to_action_type_when_invalid_value_then_raises_value_error():

    value = 'invalid'

    with pytest.raises(ValueError, match=f"'{value}' is not a valid ActionType"):
        convert_to_action_type(value)


@pytest.mark.parametrize(
    "value, expected_action_type",
    [('DEPOSIT', ActionType.DEPOSIT),
     ('WITHDRAW', ActionType.WITHDRAW),
     ])
def test_convert_to_action_type_when_valid_value_then_returns_correct_action_type(value, expected_action_type):

    result = convert_to_action_type(value)

    assert result == expected_action_type


@pytest.mark.parametrize("data", [
    # type validation
    ({'amount': '100', 'user_id': 1, 'time': 1234000000}),
    ({'type': 1, 'amount': '100', 'user_id': 1, 'time': 1234000000}),
    ({'type': 'invalid', 'amount': '100', 'user_id': 1, 'time': 1234000000}),
    # amount validation
    ({'type': 'deposit', 'user_id': 1, 'time': 1234000000}),
    ({'type': 'deposit', 'amount': 'a', 'user_id': 1, 'time': 1234000000}),
    ({'type': 'deposit', 'amount': '-9', 'user_id': 1, 'time': 1234000000}),
    # user_id validation
    ({'type': 'deposit', 'amount': '100', 'time': 1234000000}),
    ({'type': 'deposit', 'amount': '100', 'user_id': 'a', 'time': 1234000000}),
    ({'type': 'deposit', 'amount': '100', 'user_id': -9, 'time': 1234000000}),
    # time validation
    ({'type': 'deposit', 'amount': '100', 'user_id': 1}),
    ({'type': 'deposit', 'amount': '100', 'user_id': 1, 'time': 'a'}),
    ({'type': 'deposit', 'amount': '100', 'user_id': 1, 'time': -9}),
])
def test_validate_user_event_when_invalid_data_then_raises_value_error(data):
    with pytest.raises(ValueError):
        validate_user_event(data)


def test_validate_user_event_when_valid_data_then_returns_user_action():

    data = {'type': 'withdraw', 'amount': '100', 'user_id': 1, 'time': 1234000000}
    expected = UserAction(1, ActionType.WITHDRAW, Decimal(100), 1234000000)

    result = validate_user_event(data)

    assert str(result) == str(expected)
