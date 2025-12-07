from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.json_document import JSONDocument, DocumentStatus
from app.models.category import Category
from app.schemas.json_document import (
    JSONDocumentOut,
    JSONDocumentUpdate,
)

router = APIRouter(prefix="/documents", tags=["documents"])


# --------------------------------------------------
# List documents with filters
# --------------------------------------------------

@router.get("/", response_model=List[JSONDocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    json_type_id: Optional[int] = None,
    category_id: Optional[int] = None,
    tag1: Optional[str] = None,
    tag2: Optional[str] = None,
    tag3: Optional[str] = None,
    limit: int = Query(100, gt=0),
    offset: int = Query(0, ge=0),
):
    q = db.query(JSONDocument)

    if json_type_id:
        q = q.filter(JSONDocument.json_type_id == json_type_id)

    if category_id:
        q = q.filter(JSONDocument.category_id == category_id)

    # Tag-based filtering requires joining category table
    if tag1 or tag2 or tag3:
        q = q.join(Category)

        if tag1:
            q = q.filter(Category.tag1 == tag1)
        if tag2:
            q = q.filter(Category.tag2 == tag2)
        if tag3:
            q = q.filter(Category.tag3 == tag3)

    q = q.order_by(JSONDocument.created_at.desc())
    return q.offset(offset).limit(limit).all()


# --------------------------------------------------
# Get single document
# --------------------------------------------------

@router.get("/{document_id}", response_model=JSONDocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(JSONDocument).get(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return doc


# --------------------------------------------------
# Update document metadata (category, name, status, normalized_json)
# --------------------------------------------------

@router.put("/{document_id}", response_model=JSONDocumentOut)
def update_document(
    document_id: int,
    payload: JSONDocumentUpdate,
    db: Session = Depends(get_db),
):
    doc = db.query(JSONDocument).get(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doc, field, value)

    db.commit()
    db.refresh(doc)
    return doc


# --------------------------------------------------
# Delete document
# --------------------------------------------------

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(JSONDocument).get(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    db.delete(doc)
    db.commit()
    return None
