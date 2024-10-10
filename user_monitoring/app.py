import logging
from typing import Any
from flask import Flask

from user_monitoring.config import Config
from user_monitoring.api import api as api_blueprint
from user_monitoring.data_access.repositories_registry import RepositoriesRegistry


def create_app(
        session_maker: Any,
        repositories_registry: RepositoriesRegistry) -> Flask:

    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['SESSION_MAKER'] = session_maker
    app.config['REPOSITORIES'] = repositories_registry

    configure_logging()

    app.register_blueprint(api_blueprint)

    return app


def configure_logging() -> None:
    """
    Set up logging to stdout.
    TODO: Extra configuration is required to log to file or external service.
    """
    logging.basicConfig(level=logging.INFO)
