from sqlalchemy import (
    Column, BigInteger, String, DateTime, ForeignKey, Enum, JSON
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class DocumentStatus(str, enum.Enum):
    RAW = "RAW"
    PARSED = "PARSED"
    CONVERTED = "CONVERTED"
    ERROR = "ERROR"


class JSONDocument(Base):
    __tablename__ = "json_document"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    batch_id = Column(BigInteger, ForeignKey("json_batch.id"), nullable=False)
    json_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("category.id"))
    name = Column(String(255))

    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.RAW)

    raw_json = Column(JSON, nullable=False)
    normalized_json = Column(JSON)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime)

    batch = relationship("JSONBatch")
    json_type = relationship("JSONType")
    category = relationship("Category")
