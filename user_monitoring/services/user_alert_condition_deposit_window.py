

from decimal import Decimal
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.DTOs.user_action import UserAction, ActionType


class UserAlertConditionDepositWindow(UserAlertCondition):
    """
    Class to check if the total amount deposited in a 30-seconds window exceeds 200.
    """

    WINDOW_MILLISECONDS = 30000
    AMOUNT_LIMIT = Decimal(200)

    def __init__(self):
        super().__init__()
        self._amount_limit = self.AMOUNT_LIMIT

    @property
    def code(self) -> int:
        return 123

    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:

        assert amount_limit is not None, "amount_limit should never be None here"

        last_user_action = user_actions[-1]
        if last_user_action.type != ActionType.DEPOSIT:
            return False

        sum_deposit_amount = last_user_action.amount
        reverse_iterator = reversed(user_actions)
        next(reverse_iterator, None)
        for current_user_action in reverse_iterator:
            if last_user_action.time - current_user_action.time > self.WINDOW_MILLISECONDS:
                break

            if current_user_action.type != ActionType.DEPOSIT:
                continue

            sum_deposit_amount += current_user_action.amount
            if sum_deposit_amount > amount_limit:
                return True

        return sum_deposit_amount > amount_limit
