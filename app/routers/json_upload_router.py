from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.json_batch import JSONBatch
from app.models.json_document import JSONDocument, DocumentStatus
from app.schemas.json_batch import JSONBatchCreate, JSONBatchOut
from app.schemas.json_document import JSONDocumentOut

router = APIRouter(prefix="/batches", tags=["batches"])


# ----- Request / Response models for upload -----

class JSONUploadItem(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    raw_json: Any


class BatchUploadRequest(BaseModel):
    batch: JSONBatchCreate
    documents: List[JSONUploadItem]


class BatchUploadResult(BaseModel):
    batch: JSONBatchOut
    documents: List[JSONDocumentOut]

    class Config:
        orm_mode = True


# ----- Endpoints -----


@router.post(
    "/upload-json",
    response_model=BatchUploadResult,
    status_code=status.HTTP_201_CREATED,
)
def upload_json_batch(
    payload: BatchUploadRequest,
    db: Session = Depends(get_db),
):
    if not payload.documents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No documents provided",
        )

    # Create batch
    batch_data = payload.batch
    batch = JSONBatch(
        name=batch_data.name,
        json_type_id=batch_data.json_type_id,
        category_id=batch_data.category_id,
        source=batch_data.source,
        uploaded_by=batch_data.uploaded_by,
        notes=batch_data.notes,
    )
    db.add(batch)
    db.flush()  # get batch.id without full commit

    # Create documents
    doc_objects: List[JSONDocument] = []
    for item in payload.documents:
        doc = JSONDocument(
            batch_id=batch.id,
            json_type_id=batch_data.json_type_id,
            category_id=item.category_id or batch_data.category_id,
            name=item.name,
            raw_json=item.raw_json,
            status=DocumentStatus.RAW,
        )
        db.add(doc)
        doc_objects.append(doc)

    db.commit()
    db.refresh(batch)
    for doc in doc_objects:
        db.refresh(doc)

    return BatchUploadResult(
        batch=batch,
        documents=doc_objects,
    )


@router.get("/", response_model=List[JSONBatchOut])
def list_batches(
    db: Session = Depends(get_db),
    json_type_id: int | None = None,
):
    query = db.query(JSONBatch)
    if json_type_id is not None:
        query = query.filter(JSONBatch.json_type_id == json_type_id)

    return query.order_by(JSONBatch.uploaded_at.desc()).all()


@router.get("/{batch_id}", response_model=JSONBatchOut)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(JSONBatch).get(batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )
    return batch
