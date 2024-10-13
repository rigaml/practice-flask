import logging

from user_monitoring.DTOs.user import User
from user_monitoring.models.user_model import UserModel


class UserRepository:
    """
    Encapsulates data access for User.
    """

    def __init__(self, session, logger: logging.Logger) -> None:
        self.session = session
        self.logger = logger

    def get_by_id(self, user_id: int) -> User:
        """
        Gets the user with the given user_id and if not found returns a default user.
        """
        self.logger.info(f"Getting user with user_id: {user_id}")

        user_data = self.session.query(UserModel).filter_by(user_id=user_id).first()
        if user_data:
            return User(user_id, user_data.risk)

        return User(user_id, "medium")
