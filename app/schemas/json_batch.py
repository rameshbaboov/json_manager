from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JSONBatchBase(BaseModel):
    name: str
    json_type_id: int
    category_id: Optional[int] = None
    source: Optional[str] = None
    uploaded_by: Optional[str] = None
    notes: Optional[str] = None


class JSONBatchCreate(JSONBatchBase):
    pass


class JSONBatchUpdate(BaseModel):
    name: Optional[str] = None
    json_type_id: Optional[int] = None
    category_id: Optional[int] = None
    notes: Optional[str] = None


class JSONBatchOut(JSONBatchBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
