from abc import ABC, abstractmethod

from user_monitoring.models.user_action import UserAction


class UserAlertCondition(ABC):
    """
    Base class for user alert conditions.
    """
    @property
    @abstractmethod
    def code(self) -> int:
        """Defines code to be used if alert condition is met"""
        pass

    @abstractmethod
    def check(self, user_actions: list[UserAction]) -> bool:
        """Checks if the user actions satisfies the condition defined in the code.

        Args:
            user_actions: should contain at least one element and elements should be in time ascending order.
        """
        pass
