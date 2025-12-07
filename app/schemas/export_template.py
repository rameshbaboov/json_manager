from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.export_template import ExportFormat

class ExportTemplateBase(BaseModel):
    json_type_id: int
    name: str
    format: ExportFormat
    with_answers: bool = True
    template_path: str
    is_active: bool = True


class ExportTemplateCreate(ExportTemplateBase):
    pass

class ExportTemplateUpdate(BaseModel):
    name: Optional[str] = None
    format: Optional[ExportFormat] = None
    with_answers: Optional[bool] = None
    template_path: Optional[str] = None
    is_active: Optional[bool] = None


class ExportTemplateOut(ExportTemplateBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
