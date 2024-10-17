import logging
from typing import Any
from user_monitoring.data_access.repositories_registry import RepositoriesRegistry
from user_monitoring.DTOs.user_action import UserAction
from user_monitoring.services.user_alert_condition import UserAlertCondition


class UserAlertService:
    def __init__(
            self,
            user_alert_conditions: list[UserAlertCondition],
            session_maker: Any,
            repositories_registry: RepositoriesRegistry,
            logger: logging.Logger) -> None:
        self.user_alert_conditions = user_alert_conditions
        self.session_maker = session_maker
        self.repositories_registry = repositories_registry
        self.logger = logger

    def get_user_actions(self, user_id: int) -> list[dict]:
        with self.session_maker() as session:
            user_action_repository = self.repositories_registry.user_action_repository(session, self.logger)
            return [user_action.dict() for user_action in user_action_repository.get_by_id(user_id)]

    def handle_alerts(self, user_action: UserAction):
        """
        Checks user alert conditions based on user actions and returns corresponding alert codes if conditions are met.
        The current user_action is stored in the repository.
        """
        self.logger.info(f"Generating alerts for user action: {user_action}")

        with self.session_maker() as session:
            user_repository = self.repositories_registry.user_repository(session, self.logger)
            user_action_repository = self.repositories_registry.user_action_repository(session, self.logger)

            user = user_repository.get_by_id(user_action.user_id)
            user_action_repository.add(user_action)
            user_actions = user_action_repository.get_by_id(user_action.user_id)

        user_alert = {
            "alert": False,
            "alert_codes": [],
            "user_id": user_action.user_id,
        }

        for user_alert_condition in self.user_alert_conditions:
            if user_alert_condition.check(user, user_actions):
                user_alert["alert"] = True
                user_alert["alert_codes"].append(user_alert_condition.code)

        return user_alert
