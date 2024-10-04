from abc import ABC, abstractmethod
from decimal import Decimal

from user_monitoring.models.user import User
from user_monitoring.models.user_action import UserAction


class UserAlertCondition(ABC):
    """
    Base class for user alert conditions.
    Implements the Template Method pattern for checking user actions against alert conditions.
    """

    def __init__(self):
        self._amount_limit = None
        self._operation_limit = None

    @property
    @abstractmethod
    def code(self) -> int:
        """Defines code to be used if alert condition is met"""
        pass

    def check(self, user: User, user_actions: list[UserAction]) -> bool:
        """
        Checks if the user action meets the condition depending on the particular user risk.
        Follows the template pattern so subclasses can define different user actions conditions.

        Args:
            user: details from the user performing the action.
            user_actions: should contain at least one element and elements should be in time ascending order.
        """
        amount_limit, operation_limit = self._update_limits(user)

        return self._check_user_action(user_actions, amount_limit, operation_limit)

    def _update_limits(self, user: User) -> tuple[Decimal | None, int | None]:
        """
        Updates the amount and operation limits depending on the user risk. 
        The more risk the lower the limits and the less risk the higher the limits. 
        """
        amount_limit = self._amount_limit
        operation_limit = self._operation_limit

        if user.risk == "high":
            if amount_limit != None:
                amount_limit /= 2

            if operation_limit != None:
                operation_limit = operation_limit // 2 + 1
        elif user.risk == "low":
            if amount_limit != None:
                amount_limit *= 2

            if operation_limit != None:
                operation_limit *= 2

        return amount_limit, operation_limit

    @abstractmethod
    def _check_user_action(self, user_actions: list[UserAction], amount_limit: Decimal | None, operation_limit: int | None) -> bool:
        """
        User action check to be defined by the subclass.
        """
        pass
