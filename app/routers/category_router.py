from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    obj = Category(
        category_level1=payload.category_level1,
        category_level2=payload.category_level2,
        category_level3=payload.category_level3,
        tag1=payload.tag1,
        tag2=payload.tag2,
        tag3=payload.tag3,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    level1: str | None = None,
    tag1: str | None = None,
):
    query = db.query(Category)
    if level1:
        query = query.filter(Category.category_level1 == level1)
    if tag1:
        query = query.filter(Category.tag1 == tag1)

    return query.order_by(Category.created_at.desc()).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.query(Category).get(category_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return obj


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(Category).get(category_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.query(Category).get(category_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(obj)
    db.commit()
    return None
