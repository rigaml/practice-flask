from typing import Type

from user_monitoring.data_access.user_action_repository import UserActionRepository
from user_monitoring.data_access.user_repository import UserRepository


class RepositoriesRegistry:
    def __init__(self, user_action_repository: Type[UserActionRepository], user_repository: Type[UserRepository]):
        self.user_action_repository = user_action_repository
        self.user_repository = user_repository
