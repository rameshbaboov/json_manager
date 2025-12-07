from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JSONTypeBase(BaseModel):
    code: str
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class JSONTypeCreate(JSONTypeBase):
    pass


class JSONTypeUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class JSONTypeOut(JSONTypeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
