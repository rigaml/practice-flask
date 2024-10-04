import logging

from user_monitoring.models.user import User


class UserRepository:
    """
    Encapsulates data access for User.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.user_fake = {
            100: {"risk": "low"},
            200: {"risk": "medium"},
            300: {"risk": "high"}
        }

        self.logger = logger

    def get_by_id(self, user_id: int) -> User:
        """
        Get the user with the given user_id and if not found returns a default user.
        """
        user_data = self.user_fake.get(user_id)
        if user_data:
            return User(user_id, user_data["risk"])

        return User(user_id, "medium")
