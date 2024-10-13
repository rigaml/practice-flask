from decimal import Decimal
from user_monitoring.DTOs.user_action import ActionType, UserAction


def test_user_action() -> None:
    user_action = UserAction(1, ActionType.DEPOSIT, Decimal(100), 1234000000)

    print(user_action)
