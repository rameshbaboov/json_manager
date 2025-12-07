from sqlalchemy import (
    Column, BigInteger, String, DateTime, Boolean,
    ForeignKey, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class ExportFormat(str, enum.Enum):
    DOCX = "DOCX"
    PDF = "PDF"


class ExportTemplate(Base):
    __tablename__ = "export_template"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    json_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)

    name = Column(String(255), nullable=False)       # e.g. QuestionPaper_WithAns
    format = Column(Enum(ExportFormat), nullable=False)
    with_answers = Column(Boolean, nullable=False, default=True)

    template_path = Column(String(500), nullable=False)  # path in storage
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    json_type = relationship("JSONType")
