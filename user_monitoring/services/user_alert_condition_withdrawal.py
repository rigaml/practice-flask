

from decimal import Decimal
from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.DTOs.user_action import UserAction, ActionType


class UserAlertConditionWithdrawal(UserAlertCondition):
    """
    Class to check if user makes a withdrawal amount over the limit.
    """

    AMOUNT_LIMIT = Decimal(100)

    def __init__(self):
        super().__init__()
        self._amount_limit = self.AMOUNT_LIMIT

    @property
    def code(self) -> int:

        return 1100

    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:
        """
        Check if the last user action is a withdrawal exceeding the amount limit.

        Args:
            user_actions: List of user actions to check.
            amount_limit: The limit for withdrawal amount, adjusted for user risk.
            operation_limit: Not used as for this case there is no limit of operations.

        Returns:
            bool: True if the last action is a withdrawal exceeding the amount limit, False otherwise.
        """

        assert amount_limit is not None, "amount_limit should never be None here"

        last_user_action = user_actions[-1]

        return last_user_action.type == ActionType.WITHDRAW and last_user_action.amount > amount_limit
