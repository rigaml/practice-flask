from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class ActionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


@dataclass
class UserAction:
    user_id: int
    type: ActionType
    amount: Decimal
    time: int

    def dict(self) -> dict:
        return {
            'type': self.type,
            'amount': self.amount,
            'user_id': self.user_id,
            'time': self.time
        }
