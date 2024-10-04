import logging
from user_monitoring.data_access.user_repository import UserRepository
from user_monitoring.models.user_action import UserAction
from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.services.user_alert_condition import UserAlertCondition


class UserAlertService:
    def __init__(
            self,
            user_alert_conditions: list[UserAlertCondition],
            user_action_repository: UserActionRepository,
            user_repository: UserRepository,
            logger: logging.Logger) -> None:
        self.user_alert_conditions = user_alert_conditions
        self.user_action_repository = user_action_repository
        self.user_repository = user_repository
        self.logger = logger

    def handle_alerts(self, user_action: UserAction):
        """
        Checks user alert conditions based on user actions and returns corresponding alert codes if conditions are met.
        The current user_action is stored in the repository.
        """
        self.logger.info(f"Generating alerts for user action: {user_action}")

        user = self.user_repository.get_by_id(user_action.user_id)

        self.user_action_repository.create(user_action)
        user_actions = self.user_action_repository.get_all(user_action.user_id)

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
