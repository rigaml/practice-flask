from decimal import Decimal
from enum import Enum


class ActionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class UserAction:
    def __init__(self, user_id: int, type: ActionType, amount: Decimal, time: int):
        self.type = type
        self.amount = amount
        self.user_id = user_id
        self.time = time

    def __repr__(self) -> str:
        return (f"UserAction(type={self.type!r}, amount={self.amount!r}, "
                f"user_id={self.user_id!r}, time={self.time!r})")
