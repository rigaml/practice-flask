

from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.models.user_action import UserAction


class UserAlertConditionTransactionWindow(UserAlertCondition):
    """
    MIO REQUIREMENT
    Class to check if user more than five transactions (deposits or withdrawals) within a 1-minute window.
    """

    WINDOW_MILLISECONDS = 60000
    TRANSACTIONS_LIMIT = 5

    @property
    def code(self) -> int:
        return 5

    def check(self, user_actions: list[UserAction]) -> bool:
        if len(user_actions) <= self.TRANSACTIONS_LIMIT:
            return False

        if user_actions[-1].time - user_actions[-self.TRANSACTIONS_LIMIT-1].time > self.WINDOW_MILLISECONDS:
            return False

        return True
