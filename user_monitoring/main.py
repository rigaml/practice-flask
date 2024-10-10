from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_monitoring.config import Config
from user_monitoring.data_access.repositories_registry import RepositoriesRegistry
from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.data_access.user_repository import UserRepository
from user_monitoring.app import create_app

if Config.DB_URI is None:
    raise ValueError("DB_URI environment variable is not set")

session_maker = sessionmaker(bind=create_engine(Config.DB_URI))

repositories_registry = RepositoriesRegistry(
    user_action_repository=UserActionRepository,
    user_repository=UserRepository)

app = create_app(session_maker, repositories_registry)
