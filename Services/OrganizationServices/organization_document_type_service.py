from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.Organizations.organizationDocumentTypeModel import OrganizationDocumentType
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
