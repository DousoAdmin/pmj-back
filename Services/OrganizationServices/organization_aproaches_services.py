from sqlalchemy.orm import Session
from Models.organizations.organization_approaches_model import OrganizationsApproaches
from Schemas.organizationSchema.organization_aproaches_shema import (
    OrganizationAproachesCreate,
    OrganizatioAprochesUpdate,
    OrganizatioAproachesOut,
    OrganizationAproachesResponse
)
from datetime import date



def create_organization_approach(
    db: Session,
    org_approach: OrganizationAproachesCreate
):
    db_org_approach = OrganizationsApproaches(
        ORAP_FK_organization=org_approach.ORAP_FK_organization,
        ORAP_FK_approach=org_approach.ORAP_FK_approach,
        ORAP_date_create=org_approach.ORAP_date_create or str(date.today()),
        ORAP_user_create=org_approach.ORAP_user_create
    )

    db.add(db_org_approach)
    db.commit()
    db.refresh(db_org_approach)
    return db_org_approach



def get_organization_approaches(db: Session):
    return db.query(OrganizationsApproaches).all()



def get_organization_approach_by_id(
    db: Session,
    org_approach_id: int
):
    return (
        db.query(OrganizationsApproaches)
        .filter(OrganizationsApproaches.ORAP_PK == org_approach_id)
        .first()
    )



def get_approaches_by_organization(
    db: Session,
    organization_id: int
):
    return (
        db.query(OrganizationsApproaches)
        .filter(OrganizationsApproaches.ORAP_FK_organization == organization_id)
        .all()
    )



def update_organization_approach(
    db: Session,
    org_approach_id: int,
    org_approach_data: OrganizatioAprochesUpdate
):
    org_approach = get_organization_approach_by_id(db, org_approach_id)

    if not org_approach:
        return None

    if org_approach_data.ORAP_date_create is not None:
        org_approach.ORAP_date_create = org_approach_data.ORAP_date_create

    if org_approach_data.ORAP_user_create is not None:
        org_approach.ORAP_user_create = org_approach_data.ORAP_user_create

    db.commit()
    db.refresh(org_approach)
    return org_approach



def delete_organization_approach(
    db: Session,
    org_approach_id: int
):
    org_approach = get_organization_approach_by_id(db, org_approach_id)

    if not org_approach:
        return None

    db.delete(org_approach)
    db.commit()
    return org_approach


