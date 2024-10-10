from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Numeric, String
from user_monitoring.models.base import Base


class UserActionModel(Base):

    __tablename__ = 'user_actions'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
