
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


from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.organizations.organization_document_type_model import OrganizationDocumentType
from typing import Optional

def get_all_organization_document_types(db: Session):
    """Obtiene todos los tipos de documentos de organización."""
    return db.query(OrganizationDocumentType).all()

def get_organization_document_type_by_id(db: Session, organization_document_type_id: int):
    """Obtiene un tipo de documento de organización por su ID."""
    return db.query(OrganizationDocumentType).filter(OrganizationDocumentType.ODPT_PK == organization_document_type_id).first()

def search_organization_document_types(
    db: Session,
    name: Optional[str] = None
):
    """Busca tipos de documentos de organización por múltiples criterios."""
    query = db.query(OrganizationDocumentType)
    
    filters = []
    if name:
        filters.append(OrganizationDocumentType.ODPT_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_organization_document_type(db: Session, organization_document_type_data):
    """Crea un nuevo tipo de documento de organización."""
    organization_document_type_dict = organization_document_type_data.dict(exclude_unset=True)
    new_organization_document_type = OrganizationDocumentType(**organization_document_type_dict)
    db.add(new_organization_document_type)
    db.commit()
    db.refresh(new_organization_document_type)
    return new_organization_document_type

def update_organization_document_type(db: Session, organization_document_type_id: int, organization_document_type_data):
    """Actualiza un tipo de documento de organización existente."""
    organization_document_type = get_organization_document_type_by_id(db, organization_document_type_id)
    if not organization_document_type:
        return None
    
    update_data = organization_document_type_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(organization_document_type, key, value)
    
    db.commit()
    db.refresh(organization_document_type)
    return organization_document_type

def delete_organization_document_type(db: Session, organization_document_type_id: int):
    """Elimina permanentemente un tipo de documento de organización de la base de datos."""
    organization_document_type = get_organization_document_type_by_id(db, organization_document_type_id)
    if not organization_document_type:
        return None
    
    db.delete(organization_document_type)
    db.commit()
    return organization_document_type
