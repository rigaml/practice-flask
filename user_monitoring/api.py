from flask import Blueprint, Response, current_app, make_response, request, jsonify
from flask.views import MethodView

from user_monitoring.services.user_alert_condition import UserAlertCondition
from user_monitoring.services.user_alert_condition_deposit_increase import UserAlertConditionDepositIncrease
from user_monitoring.services.user_alert_condition_deposit_window import UserAlertConditionDepositWindow
from user_monitoring.services.user_alert_condition_transaction_window import UserAlertConditionTransactionWindow
from user_monitoring.services.user_alert_condition_withdrawal import UserAlertConditionWithdrawal
from user_monitoring.services.user_alert_condition_withdrawal_consecutive import UserAlertConditionWithdrawalConsecutive
from user_monitoring.services.user_alert_service import UserAlertService
from user_monitoring.utils.validators import validate_user_event


api = Blueprint("api", __name__)


def get_user_alert_conditions() -> list[UserAlertCondition]:
    """Returns the list of user alert conditions should be used for the event."""
    return [
        UserAlertConditionDepositIncrease(),
        UserAlertConditionDepositWindow(),
        UserAlertConditionTransactionWindow(),
        UserAlertConditionWithdrawalConsecutive(),
        UserAlertConditionWithdrawal()
    ]


class UserEventCollection(MethodView):
    def __init__(self) -> None:
        """
        Assuming the parameters for UserAlertService don't change in the lifetime of the app.
        """
        user_alerts_conditions = get_user_alert_conditions()

        self.user_alert_service = UserAlertService(
            user_alerts_conditions,
            current_app.config['SESSION_MAKER'],
            current_app.config['REPOSITORIES'],
            current_app.logger)

    def get(self, action_id: int) -> list[dict]:

        actions = self.user_alert_service.get_user_actions(action_id)
        return actions

    def post(self) -> dict | Response:
        current_app.logger.info("Handling user event")

        if not request.is_json:
            current_app.logger.warning("Received non-JSON request")
            return make_response(jsonify({"error": "Request must be JSON"}), 400)

        user_action_data = request.get_json()
        try:
            user_action = validate_user_event(user_action_data)
        except Exception as e:
            current_app.logger.info(f"Invalid user event {user_action_data} errors: {e}")
            return make_response(jsonify({"error": str(e)}), 400)

        user_alerts = self.user_alert_service.handle_alerts(user_action)

        return user_alerts


api.add_url_rule("/event/<int:action_id>",
                 view_func=UserEventCollection.as_view("user_event_get"), methods=["GET"])
api.add_url_rule("/event",
                 view_func=UserEventCollection.as_view("user_event_post"), methods=["POST"])
