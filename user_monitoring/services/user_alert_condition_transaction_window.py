

from decimal import Decimal
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.DTOs.user_action import UserAction


class UserAlertConditionTransactionWindow(UserAlertCondition):
    """
    Class to check if user more than five transactions (deposits or withdrawals) within a 1-minute window.
    """

    WINDOW_MILLISECONDS = 60000
    TRANSACTIONS_COUNT_LIMIT = 5

    def __init__(self):
        super().__init__()
        self._operation_limit = self.TRANSACTIONS_COUNT_LIMIT

    @property
    def code(self) -> int:
        return 500

    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:

        assert operation_limit is not None, "operation_limit should never be None here"

        if len(user_actions) <= operation_limit:
            return False

        if user_actions[-1].time - user_actions[-operation_limit-1].time > self.WINDOW_MILLISECONDS:
            return False

        return True
