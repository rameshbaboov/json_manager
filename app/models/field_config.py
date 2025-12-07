from sqlalchemy import (
    Column, BigInteger, String, Text, DateTime, Boolean,
    ForeignKey, Integer, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class FieldConfigSet(Base):
    __tablename__ = "field_config_set"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    json_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)

    name = Column(String(255), nullable=False)         # e.g. UI_Default
    description = Column(Text)
    is_default = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    json_type = relationship("JSONType")
