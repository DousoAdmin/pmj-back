
from sqlalchemy.orm import Session
from Models.organizations.organization_document_type_model import OrganizationDocumentType
from Schemas.organizationSchema.organization_document_type_shema import (
    OrganizationDocumentTypeCreate,
    OrganizationDocumentTypeOut,
    OrganizationDocumentTypeUpdate,
    OrganizationDocumentTypeRespose   
)
from datetime import date



def create_document_type(
    db: Session,
    doc_type: OrganizationDocumentTypeCreate
):
    db_doc_type = OrganizationDocumentType(
        ODPT_name=doc_type.ODPT_name,
        ODPT_description=doc_type.ODPT_description,
        ODPT_date_create=doc_type.ODPT_date_create or date.today(),
        ODPT_user_create=doc_type.ODPT_user_create
    )

    db.add(db_doc_type)
    db.commit()
    db.refresh(db_doc_type)
    return db_doc_type



def get_document_types(db: Session):
    return db.query(OrganizationDocumentType).all()



def get_document_type_by_id(
    db: Session,
    doc_type_id: int
):
    return (
        db.query(OrganizationDocumentType)
        .filter(OrganizationDocumentType.ODPT_PK == doc_type_id)
        .first()
    )



def update_document_type(
    db: Session,
    doc_type_id: int,
    doc_type_data: OrganizationDocumentTypeUpdate
):
    doc_type = get_document_type_by_id(db, doc_type_id)

    if not doc_type:
        return None

    if doc_type_data.ODPT_name is not None:
        doc_type.ODPT_name = doc_type_data.ODPT_name

    if doc_type_data.ODPT_description is not None:
        doc_type.ODPT_description = doc_type_data.ODPT_description

    if doc_type_data.ODPT_user_update is not None:
        doc_type.ODPT_user_update = doc_type_data.ODPT_user_update
    else:
        doc_type.ODPT_user_update = date.today()

    db.commit()
    db.refresh(doc_type)
    return doc_type



def delete_document_type(
    db: Session,
    doc_type_id: int
):
    doc_type = get_document_type_by_id(db, doc_type_id)

    if not doc_type:
        return None

    db.delete(doc_type)
    db.commit()
    return doc_type
