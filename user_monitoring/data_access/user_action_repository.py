"""    
For this coding test, application implements an in-memory database, which means that data will be lost when the server restarts.
"""
import logging
from user_monitoring.DTOs.user_action import ActionType, UserAction
from user_monitoring.models.user_action_model import UserActionModel


class UserActionRepository:
    """
    Encapsulates data access for UserAction.
    """

    def __init__(self, session, logger: logging.Logger) -> None:
        self.session = session
        self.logger = logger

    def add(self, user_action: UserAction) -> UserAction:
        self.logger.info(f"Adding to repository user action: {user_action}")

        user_action_model = UserActionModel(
            user_id=user_action.user_id,
            type=user_action.type.name,
            amount=user_action.amount,
            time=user_action.time
        )

        self.session.add(user_action_model)
        self.session.commit()

        return UserAction(user_action.user_id, user_action.type, user_action.amount, user_action.time)

    def get_by_id(self, user_id: int) -> list[UserAction]:
        self.logger.info(f"Getting all user actions for user_id: {user_id}")

        query = self.session.query(UserActionModel).filter_by(user_id=user_id)

        return [
            UserAction(
                user_action_m.user_id, ActionType[user_action_m.type], user_action_m.amount, user_action_m.time)
            for user_action_m in query.all()
        ]
