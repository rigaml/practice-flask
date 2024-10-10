from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List
from user_monitoring.DTOs.user_action import ActionType, UserAction


@staticmethod
def convert_to_action_type(value: str) -> ActionType:
    """
    Tries to convert a string to an ActionType enum value.

    Raises:
        ValueError: if value is not a valid ActionType.

    """
    try:
        return ActionType[value.upper()]
    except KeyError:
        raise ValueError(f"'{value}' is not a valid ActionType")


@staticmethod
def validate_user_event(data: Dict[str, Any]) -> UserAction:
    """
    Validates that the data contains all the expected fields to be able to create a UserAction.

    Raises:
        ValueError: if data is not valid raises exception with details of fields with errors in the message.
    """
    errors: List[str] = []

    if 'type' not in data or not isinstance(data['type'], str):
        errors.append("'type' must be one of these values (deposit, withdraw)")
    else:
        try:
            action_type = convert_to_action_type(data['type'])
        except ValueError:
            errors.append("'type' must be one of these values (deposit, withdraw)")

    amount = Decimal(0)
    if 'amount' not in data:
        errors.append("'amount' must be provided")
    else:
        try:
            amount = Decimal(data['amount'])
        except InvalidOperation as e:
            errors.append(f"'amount' must be a decimal number: {str(e)}")

    if amount <= 0:
        errors.append("'amount' must be a greater than 0")

    if 'user_id' not in data or not isinstance(data['user_id'], int) or data['user_id'] < 0:
        errors.append("'user_id' must be provided and be a positive integer")

    if 'time' not in data or not isinstance(data['time'], int) or data['time'] < 0:
        errors.append("'time' must be provided and be a positive integer")

    if errors:
        raise ValueError('; '.join(errors))

    return UserAction(data['user_id'], action_type, amount, data['time'])
