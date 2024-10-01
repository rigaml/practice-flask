

from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.models.user_action import UserAction, ActionType


class UserAlertConditionWithdrawalConsecutive(UserAlertCondition):
    """
    Class to check if the user makes 3 consecutive withdrawals.
    """

    COUNT_WITHDRAW_LIMIT = 3

    @property
    def code(self) -> int:
        return 30

    def check(self, user_actions: list[UserAction]) -> bool:
        if len(user_actions) < self.COUNT_WITHDRAW_LIMIT:
            return False

        return all(user_action.type == ActionType.WITHDRAW for user_action in user_actions[-self.COUNT_WITHDRAW_LIMIT:])
