from sqlalchemy.orm import Session
from Models.organizations.organization_type_model import OrganizationTypes
from Schemas.organizationSchema.organization_type_shema import (
    OrganizationTypeCreate,
    OrganizationTypeUpdate,
    OrganizationTypeOut,
    OrganizationTypeResponse)
from datetime import date


#Crear

def create_organization_type(
    db: Session,
    org_type: OrganizationTypeCreate
):
    db_org_type = OrganizationTypes(
        ORTP_name=org_type.ORTP_name,
        ORTP_description=org_type.ORTP_description,
        ORTP_date_create=org_type.ORTP_date_create or date.today()
    )
    db.add(db_org_type)
    db.commit()
    db.refresh(db_org_type)
    return db_org_type



#Traer Todos 
def get_organization_types(db: Session):
    return db.query(OrganizationTypes).all()



#Obtener por id
def get_organization_type_by_id(
    db: Session,
    org_type_id: int
):
    return (
        db.query(OrganizationTypes)
        .filter(OrganizationTypes.ORTP_PK == org_type_id)
        .first()
    )


#Actualizar
def update_organization_type(
    db: Session,
    org_type_id: int,
    org_type_data: OrganizationTypeUpdate
):
    org_type = get_organization_type_by_id(db, org_type_id)

    if not org_type:
        return None

    if org_type_data.ORTP_name is not None:
        org_type.ORTP_name = org_type_data.ORTP_name

    if org_type_data.ORTP_description is not None:
        org_type.ORTP_description = org_type_data.ORTP_description

    db.commit()
    db.refresh(org_type)
    return org_type



#Eliminar
def delete_organization_type(
    db: Session,
    org_type_id: int
):
    org_type = get_organization_type_by_id(db, org_type_id)

    if not org_type:
        return None

    db.delete(org_type)
    db.commit()
    return org_type


