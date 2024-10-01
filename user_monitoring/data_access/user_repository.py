import logging

from user_monitoring.models.user import User


class UserRepository:
    """
    Encapsulates data access for User.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.user_fake = {
            1: {"risk": "low"},
            2: {"risk": "medium"},
            3: {"risk": "high"}
        }

        self.logger = logger

    def get_by_id(self, user_id: int) -> User | None:
        user_data = self.user_fake.get(user_id)
        if user_data:
            return User(user_id, user_data["risk"])

        return User(user_id, "medium")
