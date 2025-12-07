from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    category_level1: str
    category_level2: Optional[str] = None
    category_level3: Optional[str] = None

    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_level1: Optional[str] = None
    category_level2: Optional[str] = None
    category_level3: Optional[str] = None

    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
