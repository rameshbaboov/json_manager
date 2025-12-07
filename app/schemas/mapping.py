from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.mapping import MappingAction


class MappingProfileBase(BaseModel):
    name: str
    source_type_id: int
    target_type_id: int
    description: Optional[str] = None
    is_active: Optional[bool] = True


class MappingProfileCreate(MappingProfileBase):
    pass


class MappingProfileUpdate(BaseModel):
    name: Optional[str] = None
    source_type_id: Optional[int] = None
    target_type_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class MappingProfileOut(MappingProfileBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MappingRuleBase(BaseModel):
    profile_id: int
    action: MappingAction

    source_json_path: Optional[str] = None
    target_json_path: str

    default_value: Optional[str] = None
    transform_expr: Optional[str] = None
    order_index: int = 0


class MappingRuleCreate(MappingRuleBase):
    pass


class MappingRuleUpdate(BaseModel):
    action: Optional[MappingAction] = None
    source_json_path: Optional[str] = None
    target_json_path: Optional[str] = None
    default_value: Optional[str] = None
    transform_expr: Optional[str] = None
    order_index: Optional[int] = None


class MappingRuleOut(MappingRuleBase):
    id: int

    class Config:
        orm_mode = True
