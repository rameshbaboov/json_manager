from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.mapping import (
    MappingProfile,
    MappingRule,
    MappingAction,
)
from app.models.json_document import JSONDocument
from app.schemas.mapping import (
    MappingProfileCreate,
    MappingProfileUpdate,
    MappingProfileOut,
    MappingRuleCreate,
    MappingRuleUpdate,
    MappingRuleOut,
)
from app.utils.mapping_engine import apply_mapping_profile

router = APIRouter(prefix="/mapping", tags=["mapping"])


# ---------------------------------------------------------
# Profiles
# ---------------------------------------------------------

@router.post("/profiles", response_model=MappingProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: MappingProfileCreate, db: Session = Depends(get_db)):
    obj = MappingProfile(
        name=payload.name,
        source_type_id=payload.source_type_id,
        target_type_id=payload.target_type_id,
        description=payload.description,
        is_active=payload.is_active,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/profiles", response_model=List[MappingProfileOut])
def list_profiles(db: Session = Depends(get_db)):
    return db.query(MappingProfile).order_by(MappingProfile.created_at.desc()).all()


@router.get("/profiles/{profile_id}", response_model=MappingProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    obj = db.query(MappingProfile).get(profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")
    return obj


@router.put("/profiles/{profile_id}", response_model=MappingProfileOut)
def update_profile(profile_id: int, payload: MappingProfileUpdate, db: Session = Depends(get_db)):
    obj = db.query(MappingProfile).get(profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    obj = db.query(MappingProfile).get(profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(obj)
    db.commit()
    return None


# ---------------------------------------------------------
# Rules
# ---------------------------------------------------------

@router.post("/rules", response_model=MappingRuleOut, status_code=status.HTTP_201_CREATED)
def create_rule(payload: MappingRuleCreate, db: Session = Depends(get_db)):
    obj = MappingRule(
        profile_id=payload.profile_id,
        action=payload.action,
        source_json_path=payload.source_json_path,
        target_json_path=payload.target_json_path,
        default_value=payload.default_value,
        transform_expr=payload.transform_expr,
        order_index=payload.order_index,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/rules/{profile_id}", response_model=List[MappingRuleOut])
def list_rules(profile_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MappingRule)
        .filter(MappingRule.profile_id == profile_id)
        .order_by(MappingRule.order_index.asc())
        .all()
    )


@router.put("/rules/{rule_id}", response_model=MappingRuleOut)
def update_rule(rule_id: int, payload: MappingRuleUpdate, db: Session = Depends(get_db)):
    obj = db.query(MappingRule).get(rule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    obj = db.query(MappingRule).get(rule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(obj)
    db.commit()
    return None


# ---------------------------------------------------------
# Convert a document using a mapping profile
# ---------------------------------------------------------

@router.post("/convert-document/{profile_id}/{document_id}", response_model=Any)
def convert_document(profile_id: int, document_id: int, db: Session = Depends(get_db)):
    profile = db.query(MappingProfile).get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    doc = db.query(JSONDocument).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    result_json = apply_mapping_profile(profile_id, doc.raw_json, db)
    return {
        "document_id": document_id,
        "source_type_id": profile.source_type_id,
        "target_type_id": profile.target_type_id,
        "converted_json": result_json,
    }


# ---------------------------------------------------------
# Convert a whole batch
# ---------------------------------------------------------

@router.post("/convert-batch/{profile_id}/{batch_id}", response_model=List[Any])
def convert_batch(profile_id: int, batch_id: int, db: Session = Depends(get_db)):
    profile = db.query(MappingProfile).get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    docs = db.query(JSONDocument).filter(JSONDocument.batch_id == batch_id).all()
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found in batch")

    results = []
    for doc in docs:
        converted = apply_mapping_profile(profile_id, doc.raw_json, db)
        results.append({
            "document_id": doc.id,
            "converted_json": converted,
        })

    return results
