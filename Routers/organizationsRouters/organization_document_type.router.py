from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_document_type_shema import (
    OrganizationDocumentTypeCreate,
    OrganizationDocumentTypeUpdate, 
    OrganizationDocumentTypeRespose
)
from Services.organizationServices.organization_document_type_service import (
    create_document_type,
    get_document_types,
    get_document_type_by_id,
    update_document_type,
    delete_document_type
)
router = APIRouter(
    prefix="/organization-document-types",
    tags=["Organization Document Types"]
)


@router.post("/", response_model=OrganizationDocumentTypeRespose)
def create(
    doc_type: OrganizationDocumentTypeCreate,
    db: Session = Depends(get_db)
):
    return create_document_type(db, doc_type)



@router.get("/", response_model=list[OrganizationDocumentTypeRespose])
def get_all(db: Session = Depends(get_db)):
    return get_document_types(db)



@router.get("/", response_model=list[OrganizationDocumentTypeRespose])
def get_all(db: Session = Depends(get_db)):
    return get_document_types(db)



@router.get("/{doc_type_id}", response_model=OrganizationDocumentTypeRespose)
def get_by_id(
    doc_type_id: int,
    db: Session = Depends(get_db)
):
    doc_type = get_document_type_by_id(db, doc_type_id)

    if not doc_type:
        raise HTTPException(status_code=404, detail="Document type not found")

    return doc_type



@router.put("/{doc_type_id}", response_model=OrganizationDocumentTypeRespose)
def update(
    doc_type_id: int,
    doc_type_data: OrganizationDocumentTypeUpdate,
    db: Session = Depends(get_db)
):
    doc_type = update_document_type(db, doc_type_id, doc_type_data)

    if not doc_type:
        raise HTTPException(status_code=404, detail="Document type not found")

    return doc_type



@router.delete("/{doc_type_id}")
def delete(
    doc_type_id: int,
    db: Session = Depends(get_db)
):
    doc_type = delete_document_type(db, doc_type_id)

    if not doc_type:
        raise HTTPException(status_code=404, detail="Document type not found")

    return {"message": "Document type deleted successfully"}



