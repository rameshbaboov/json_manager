from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.json_type import JSONType
from app.schemas.json_type import (
    JSONTypeCreate,
    JSONTypeUpdate,
    JSONTypeOut,
)

router = APIRouter(prefix="/json-types", tags=["json-types"])


@router.post("/", response_model=JSONTypeOut, status_code=status.HTTP_201_CREATED)
def create_json_type(payload: JSONTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(JSONType).filter(JSONType.code == payload.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"JSON type with code '{payload.code}' already exists",
        )

    obj = JSONType(
        code=payload.code,
        name=payload.name,
        version=payload.version,
        description=payload.description,
        is_active=payload.is_active,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=List[JSONTypeOut])
def list_json_types(
    db: Session = Depends(get_db),
    is_active: bool | None = None,
):
    query = db.query(JSONType)
    if is_active is not None:
        query = query.filter(JSONType.is_active == is_active)
    return query.order_by(JSONType.created_at.desc()).all()


@router.get("/{json_type_id}", response_model=JSONTypeOut)
def get_json_type(json_type_id: int, db: Session = Depends(get_db)):
    obj = db.query(JSONType).get(json_type_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JSON type not found")
    return obj


@router.put("/{json_type_id}", response_model=JSONTypeOut)
def update_json_type(
    json_type_id: int,
    payload: JSONTypeUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(JSONType).get(json_type_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JSON type not found")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{json_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_json_type(json_type_id: int, db: Session = Depends(get_db)):
    obj = db.query(JSONType).get(json_type_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JSON type not found")

    db.delete(obj)
    db.commit()
    return None
