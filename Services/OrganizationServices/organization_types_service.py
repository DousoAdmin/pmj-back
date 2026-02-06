from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.Organizations.organizationTypeModel import OrganizationTypes
from typing import Optional

def get_all_organization_types(db: Session):
    """Obtiene todos los tipos de organización."""
    return db.query(OrganizationTypes).all()

def get_organization_type_by_id(db: Session, organization_type_id: int):
    """Obtiene un tipo de organización por su ID."""
    return db.query(OrganizationTypes).filter(OrganizationTypes.ORTP_PK == organization_type_id).first()

def search_organization_types(
    db: Session,
    name: Optional[str] = None
):
    """Busca tipos de organización por múltiples criterios."""
    query = db.query(OrganizationTypes)
    
    filters = []
    if name:
        filters.append(OrganizationTypes.ORTP_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_organization_type(db: Session, organization_type_data):
    """Crea un nuevo tipo de organización."""
    organization_type_dict = organization_type_data.dict(exclude_unset=True)
    new_organization_type = OrganizationTypes(**organization_type_dict)
    db.add(new_organization_type)
    db.commit()
    db.refresh(new_organization_type)
    return new_organization_type

def update_organization_type(db: Session, organization_type_id: int, organization_type_data):
    """Actualiza un tipo de organización existente."""
    organization_type = get_organization_type_by_id(db, organization_type_id)
    if not organization_type:
        return None
    
    update_data = organization_type_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(organization_type, key, value)
    
    db.commit()
    db.refresh(organization_type)
    return organization_type

def delete_organization_type(db: Session, organization_type_id: int):
    """Elimina permanentemente un tipo de organización de la base de datos."""
    organization_type = get_organization_type_by_id(db, organization_type_id)
    if not organization_type:
        return None
    
    db.delete(organization_type)
    db.commit()
    return organization_type
