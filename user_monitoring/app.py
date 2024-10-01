import logging
from flask import Flask

from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.data_access.user_repository import UserRepository


def create_app() -> Flask:
    app = Flask("user_monitoring")

    configure_logging()

    with app.app_context():
        setattr(app, 'user_action_repo', UserActionRepository(logger=app.logger))
        setattr(app, 'user_repo', UserRepository(logger=app.logger))

    from user_monitoring.api import api as api_blueprint

    app.register_blueprint(api_blueprint)
    return app


def configure_logging() -> None:
    """
    Set up logging to stdout.
    TODO: Extra configuration is required to log to file or external service.
    """
    logging.basicConfig(level=logging.INFO)
