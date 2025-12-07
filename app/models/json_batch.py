from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class JSONBatch(Base):
    __tablename__ = "json_batch"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    json_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("category.id"))
    source = Column(String(255))
    uploaded_by = Column(String(255))
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    notes = Column(Text)

    json_type = relationship("JSONType")
    category = relationship("Category")
