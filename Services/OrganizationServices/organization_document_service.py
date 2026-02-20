from sqlalchemy.orm import Session
from Models.organizations.organization_document_model import OrganizationDocument
from Schemas.organizationSchema.organization_document_Shema import (
    OrganizationDocumentCreate,
    OrganizationDocumentUpdate
)
from datetime import date


def create_document(
    db: Session,
    document: OrganizationDocumentCreate
):
    db_document = OrganizationDocument(
        ORDC_FK_organization=document.ORDC_FK_organization,
        ORDC_FK_document_type=document.ORDC_FK_document_type,
        ORDC_file_path=document.ORDC_file_path,
        ORDC_original_name=document.ORDC_original_name,
        ORDC_upload_date=document.ORDC_upload_date or date.today(),
        ORDC_state=document.ORDC_state,
        ORDC_observation=document.ORDC_observation,
        ORDC_user_create=document.ORDC_user_create
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document



def get_documents(db: Session):
    return db.query(OrganizationDocument).all()



def get_document_by_id(
    db: Session,
    document_id: int
):
    return (
        db.query(OrganizationDocument)
        .filter(OrganizationDocument.ORDC_PK == document_id)
        .first()
    )



def get_documents_by_organization(
    db: Session,
    organization_id: int
):
    return (
        db.query(OrganizationDocument)
        .filter(OrganizationDocument.ORDC_FK_organization == organization_id)
        .all()
    )



def get_documents_by_type(
    db: Session,
    document_type_id: int
):
    return (
        db.query(OrganizationDocument)
        .filter(OrganizationDocument.ORDC_FK_document_type == document_type_id)
        .all()
    )



def update_document(
    db: Session,
    document_id: int,
    document_data: OrganizationDocumentUpdate
):
    document = get_document_by_id(db, document_id)

    if not document:
        return None

    if document_data.ORDC_file_path is not None:
        document.ORDC_file_path = document_data.ORDC_file_path

    if document_data.ORDC_original_name is not None:
        document.ORDC_original_name = document_data.ORDC_original_name

    if document_data.ORDC_state is not None:
        document.ORDC_state = document_data.ORDC_state

    if document_data.ORDC_observation is not None:
        document.ORDC_observation = document_data.ORDC_observation

    db.commit()
    db.refresh(document)
    return document



def delete_document(
    db: Session,
    document_id: int
):
    document = get_document_by_id(db, document_id)

    if not document:
        return None

    db.delete(document)
    db.commit()
    return document
