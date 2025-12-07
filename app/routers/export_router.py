from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.export_template import ExportTemplate, ExportFormat
from app.models.json_document import JSONDocument
from app.schemas.export_template import (
    ExportTemplateCreate,
    ExportTemplateUpdate,
    ExportTemplateOut
)
from app.utils.export_service import generate_export


router = APIRouter(prefix="/export", tags=["export"])


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

@router.post("/templates", response_model=ExportTemplateOut, status_code=status.HTTP_201_CREATED)
def create_export_template(payload: ExportTemplateCreate, db: Session = Depends(get_db)):
    obj = ExportTemplate(
        json_type_id=payload.json_type_id,
        name=payload.name,
        format=payload.format,
        with_answers=payload.with_answers,
        template_path=payload.template_path,
        is_active=payload.is_active,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/templates", response_model=List[ExportTemplateOut])
def list_templates(db: Session = Depends(get_db), json_type_id: int | None = None):
    q = db.query(ExportTemplate)
    if json_type_id:
        q = q.filter(ExportTemplate.json_type_id == json_type_id)
    return q.order_by(ExportTemplate.created_at.desc()).all()


@router.get("/templates/{template_id}", response_model=ExportTemplateOut)
def get_template(template_id: int, db: Session = Depends(get_db)):
    t = db.query(ExportTemplate).get(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")
    return t


@router.put("/templates/{template_id}", response_model=ExportTemplateOut)
def update_template(template_id: int, payload: ExportTemplateUpdate, db: Session = Depends(get_db)):
    t = db.query(ExportTemplate).get(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")

    data = payload.dict(exclude_unset=True)
    for f, v in data.items():
        setattr(t, f, v)

    db.commit()
    db.refresh(t)
    return t


@router.delete("/templates/{template_id}", status_code=204)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    t = db.query(ExportTemplate).get(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(t)
    db.commit()
    return None


# ---------------------------------------------------------
# Export document
# ---------------------------------------------------------

@router.post("/document/{document_id}")
def export_document(
    document_id: int,
    format: ExportFormat,
    with_answers: bool = True,
    template_id: int | None = None,
    db: Session = Depends(get_db),
):
    doc = db.query(JSONDocument).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_bytes, file_name = generate_export(
        db=db,
        document=doc,
        export_format=format,
        with_answers=with_answers,
        template_id=template_id,
    )

    return {
        "file_name": file_name,
        "file_data_base64": file_bytes,
    }


# ---------------------------------------------------------
# Export batch
# ---------------------------------------------------------

@router.post("/batch/{batch_id}")
def export_batch(
    batch_id: int,
    format: ExportFormat,
    with_answers: bool = True,
    template_id: int | None = None,
    db: Session = Depends(get_db),
):
    docs = db.query(JSONDocument).filter(JSONDocument.batch_id == batch_id).all()
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found in batch")

    outputs = []

    for doc in docs:
        file_bytes, file_name = generate_export(
            db=db,
            document=doc,
            export_format=format,
            with_answers=with_answers,
            template_id=template_id,
        )
        outputs.append({
            "document_id": doc.id,
            "file_name": file_name,
            "file_data_base64": file_bytes,
        })

    return outputs
