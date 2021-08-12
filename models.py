from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.sql import func

from db_conf import Base


class Advertisement(Base):
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    body = Column(String)
    price = Column(Float, nullable=True)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
