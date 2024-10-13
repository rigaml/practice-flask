from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String
from user_monitoring.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    risk = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
