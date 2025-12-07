from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.field_config import ExportMaskType

class FieldConfigSetBase(BaseModel):
    json_type_id: int
    name: str
    description: Optional[str] = None
    is_default: bool = False


class FieldConfigSetCreate(FieldConfigSetBase):
    pass


class FieldConfigSetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None


class FieldConfigSetOut(FieldConfigSetBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FieldConfigBase(BaseModel):
    config_set_id: int

    json_path: str
    label: Optional[str] = None

    order_index: int = 0
    show_in_ui: bool = True
    show_in_export: bool = True
    required: bool = False

    export_mask_type: ExportMaskType = ExportMaskType.NONE

class FieldConfigCreate(FieldConfigBase):
    pass

class FieldConfigUpdate(BaseModel):
    json_path: Optional[str] = None
    label: Optional[str] = None
    order_index: Optional[int] = None
    show_in_ui: Optional[bool] = None
    show_in_export: Optional[bool] = None
    required: Optional[bool] = None
    export_mask_type: Optional[ExportMaskType] = None


class FieldConfigOut(FieldConfigBase):
    id: int

    class Config:
        orm_mode = True
