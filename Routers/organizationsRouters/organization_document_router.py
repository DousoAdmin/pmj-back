from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_document_Shema import (
    OrganizationDocumentCreate,
    OrganizationDocumentUpdate,
    OrganizationDocumentResponse
)
from Services.organizationServices.organization_document_service import (
    create_document,
    get_documents,
    get_document_by_id,
    get_documents_by_organization,
    get_documents_by_type,
    update_document,
    delete_document
)
router = APIRouter(
    prefix="/organization-documents",
    tags=["Organization Documents"]
)



@router.post("/", response_model=OrganizationDocumentResponse)
def create(
    document: OrganizationDocumentCreate,
    db: Session = Depends(get_db)
):
    return create_document(db, document)



@router.get("/", response_model=list[OrganizationDocumentResponse])
def get_all(db: Session = Depends(get_db)):
    return get_documents(db)



@router.get("/{document_id}", response_model=OrganizationDocumentResponse)
def get_by_id(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document



@router.get("/organization/{organization_id}", response_model=list[OrganizationDocumentResponse])
def get_by_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    return get_documents_by_organization(db, organization_id)



@router.get("/type/{document_type_id}", response_model=list[OrganizationDocumentResponse])
def get_by_type(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    return get_documents_by_type(db, document_type_id)



@router.put("/{document_id}", response_model=OrganizationDocumentResponse)
def update(
    document_id: int,
    document_data: OrganizationDocumentUpdate,
    db: Session = Depends(get_db)
):
    document = update_document(db, document_id, document_data)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document



@router.delete("/{document_id}")
def delete(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = delete_document(db, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}
