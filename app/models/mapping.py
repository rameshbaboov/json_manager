from sqlalchemy import (
    Column, BigInteger, String, Text, DateTime, Boolean,
    ForeignKey, Integer, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class MappingAction(str, enum.Enum):
    MAP = "MAP"         # copy source → target
    IGNORE = "IGNORE"   # drop the field
    DEFAULT = "DEFAULT" # use default_value when source missing
    ADD = "ADD"         # add new field to target

class MappingProfile(Base):
    __tablename__ = "mapping_profile"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    source_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)
    target_type_id = Column(BigInteger, ForeignKey("json_type.id"), nullable=False)

    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    source_type = relationship("JSONType", foreign_keys=[source_type_id])
    target_type = relationship("JSONType", foreign_keys=[target_type_id])


class MappingRule(Base):
    __tablename__ = "mapping_rule"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    profile_id = Column(BigInteger, ForeignKey("mapping_profile.id"), nullable=False)
    action = Column(Enum(MappingAction), nullable=False)

    source_json_path = Column(String(500))  # nullable when ADD/DEFAULT
    target_json_path = Column(String(500), nullable=False)

    default_value = Column(Text)  # used for DEFAULT and ADD
    transform_expr = Column(Text) # optional expression to modify values

    order_index = Column(Integer, nullable=False, default=0)

    profile = relationship("MappingProfile")
