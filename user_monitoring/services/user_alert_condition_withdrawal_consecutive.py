

from decimal import Decimal
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.models.user_action import UserAction, ActionType


class UserAlertConditionWithdrawalConsecutive(UserAlertCondition):
    """
    Class to check if the user makes 3 consecutive withdrawals.
    """

    WITHDRAW_COUNT_LIMIT = 3

    def __init__(self):
        super().__init__()
        self._operation_limit = self.WITHDRAW_COUNT_LIMIT

    @property
    def code(self) -> int:
        return 30

    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:

        assert operation_limit is not None, "operation_limit should never be None here"

        if len(user_actions) < operation_limit:
            return False

        return all(user_action.type == ActionType.WITHDRAW for user_action in user_actions[-operation_limit:])
