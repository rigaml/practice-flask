"""    
For this coding test, application implements an in-memory database, which means that data will be lost when the server restarts.

TODO: When developing a real application, a persistent database (ex. PostgreSQL, MySQL...) should be used.

"""
import logging
from user_monitoring.models.user_action import UserAction


class UserActionRepository:
    """
    Encapsulates data access for UserAction.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.user_actions_fake = []
        self.logger = logger

    def create(self, user_action: UserAction) -> None:
        self.logger.info(f"Adding to repository user action: {user_action}")
        self.user_actions_fake.append(user_action)

    def get_all(self, user_id: int) -> list[UserAction]:
        self.logger.info(f"Getting all user actions for user_id: {user_id}")
        return [user_action for user_action in self.user_actions_fake if user_action.user_id == user_id]
