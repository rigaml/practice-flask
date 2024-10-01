

from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.models.user_action import UserAction, ActionType


class UserAlertConditionWithdrawal(UserAlertCondition):
    """
    Class to check if user makes a withdrawal amount over 100.
    """

    AMOUNT_LIMIT = 100

    @property
    def code(self) -> int:
        return 1100

    def check(self, user_actions: list[UserAction]) -> bool:
        last_user_action = user_actions[-1]
        return last_user_action.type == ActionType.WITHDRAW and last_user_action.amount > self.AMOUNT_LIMIT
