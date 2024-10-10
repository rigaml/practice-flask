

from decimal import Decimal
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.DTOs.user_action import UserAction, ActionType


class UserAlertConditionDepositIncrease(UserAlertCondition):
    """
    Class to check if a user makes 3 consecutive deposits where each one is larger than the previous 
    deposit (withdrawals in between deposits can be ignored).
    """

    DEPOSIT_COUNT_LIMIT = 3

    def __init__(self):
        super().__init__()
        self._operation_limit = self.DEPOSIT_COUNT_LIMIT

    @property
    def code(self) -> int:
        return 300

    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:

        assert operation_limit is not None, "operation_limit should never be None here"

        last_user_action = user_actions[-1]
        if last_user_action.type != ActionType.DEPOSIT:
            return False

        count_deposits_increase = 1
        later_deposit_amount = last_user_action.amount
        reverse_iterator = reversed(user_actions)
        next(reverse_iterator, None)
        for current_user_action in reverse_iterator:
            # Ignoring withdrawals in between deposits
            if current_user_action.type != ActionType.DEPOSIT:
                continue

            if current_user_action.amount < later_deposit_amount:
                count_deposits_increase += 1
                if count_deposits_increase >= operation_limit:
                    return True
            else:
                return False

            later_deposit_amount = current_user_action.amount

        return False
