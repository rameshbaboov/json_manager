from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from app.models.json_document import DocumentStatus


class JSONDocumentBase(BaseModel):
    batch_id: int
    json_type_id: int
    category_id: Optional[int] = None
    name: Optional[str] = None

    raw_json: Any
    normalized_json: Optional[Any] = None

    status: Optional[DocumentStatus] = DocumentStatus.RAW


class JSONDocumentCreate(JSONDocumentBase):
    pass


class JSONDocumentUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    normalized_json: Optional[Any] = None
    status: Optional[DocumentStatus] = None


class JSONDocumentOut(JSONDocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
