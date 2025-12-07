from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class JSONType(Base):
    __tablename__ = "json_type"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(50))
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
