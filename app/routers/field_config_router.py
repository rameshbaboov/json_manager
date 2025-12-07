from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.field_config import FieldConfigSet, FieldConfig
from app.schemas.field_config import (
    FieldConfigSetCreate,
    FieldConfigSetUpdate,
    FieldConfigSetOut,
    FieldConfigCreate,
    FieldConfigUpdate,
    FieldConfigOut,
)

router = APIRouter(prefix="/field-config", tags=["field-config"])


# ---------------------------------------------------------
# FIELD CONFIG SETS
# ---------------------------------------------------------

@router.post("/sets", response_model=FieldConfigSetOut, status_code=status.HTTP_201_CREATED)
def create_config_set(payload: FieldConfigSetCreate, db: Session = Depends(get_db)):
    obj = FieldConfigSet(
        json_type_id=payload.json_type_id,
        name=payload.name,
        description=payload.description,
        is_default=payload.is_default,
    )

    if payload.is_default:
        db.query(FieldConfigSet).filter(
            FieldConfigSet.json_type_id == payload.json_type_id
        ).update({"is_default": False})

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/sets", response_model=List[FieldConfigSetOut])
def list_config_sets(
    db: Session = Depends(get_db),
    json_type_id: int | None = None,
):
    q = db.query(FieldConfigSet)
    if json_type_id:
        q = q.filter(FieldConfigSet.json_type_id == json_type_id)
    return q.order_by(FieldConfigSet.created_at.desc()).all()


@router.get("/sets/{set_id}", response_model=FieldConfigSetOut)
def get_config_set(set_id: int, db: Session = Depends(get_db)):
    obj = db.query(FieldConfigSet).get(set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field config set not found")
    return obj


@router.put("/sets/{set_id}", response_model=FieldConfigSetOut)
def update_config_set(set_id: int, payload: FieldConfigSetUpdate, db: Session = Depends(get_db)):
    obj = db.query(FieldConfigSet).get(set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field config set not found")

    incoming = payload.dict(exclude_unset=True)

    if "is_default" in incoming and incoming["is_default"] is True:
        db.query(FieldConfigSet).filter(
            FieldConfigSet.json_type_id == obj.json_type_id
        ).update({"is_default": False})

    for f, v in incoming.items():
        setattr(obj, f, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/sets/{set_id}", status_code=204)
def delete_config_set(set_id: int, db: Session = Depends(get_db)):
    obj = db.query(FieldConfigSet).get(set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field config set not found")

    db.delete(obj)
    db.commit()
    return None


# ---------------------------------------------------------
# FIELD CONFIG ITEMS
# ---------------------------------------------------------

@router.post("/items", response_model=FieldConfigOut, status_code=status.HTTP_201_CREATED)
def create_field_config(payload: FieldConfigCreate, db: Session = Depends(get_db)):
    obj = FieldConfig(
        config_set_id=payload.config_set_id,
        json_path=payload.json_path,
        label=payload.label,
        order_index=payload.order_index,
        show_in_ui=payload.show_in_ui,
        show_in_export=payload.show_in_export,
        required=payload.required,
        export_mask_type=payload.export_mask_type,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/items/{set_id}", response_model=List[FieldConfigOut])
def list_field_configs(set_id: int, db: Session = Depends(get_db)):
    return (
        db.query(FieldConfig)
        .filter(FieldConfig.config_set_id == set_id)
        .order_by(FieldConfig.order_index.asc())
        .all()
    )


@router.put("/items/{config_id}", response_model=FieldConfigOut)
def update_field_config(
    config_id: int,
    payload: FieldConfigUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(FieldConfig).get(config_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field config item not found")

    incoming = payload.dict(exclude_unset=True)
    for f, v in incoming.items():
        setattr(obj, f, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/items/{config_id}", status_code=204)
def delete_field_config(config_id: int, db: Session = Depends(get_db)):
    obj = db.query(FieldConfig).get(config_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field config item not found")

    db.delete(obj)
    db.commit()
    return None
