from sqlalchemy.orm import Session
from Models.organizations.organizaionStatusesModel import OrganizationStatuses
from Schemas.organizationSchema.organization_status_schema import (
    OrganizationStatusCreate,
    OrganizationStatusUpdate
)


# -------------------------
# GET ALL
# -------------------------
def get_organization_statuses(db: Session):
    return db.query(OrganizationStatuses).all()


# -------------------------
# GET BY ID
# -------------------------
def get_organization_status(db: Session, status_id: int):
    return db.query(OrganizationStatuses).filter(
        OrganizationStatuses.ORST_PK == status_id
    ).first()


# -------------------------
# CREATE
# -------------------------
def create_organization_status(db: Session, data: OrganizationStatusCreate):
    status = OrganizationStatuses(**data.dict())
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


# -------------------------
# UPDATE
# -------------------------
def update_organization_status(
    db: Session,
    status_id: int,
    data: OrganizationStatusUpdate
):
    status = db.query(OrganizationStatuses).filter(
        OrganizationStatuses.ORST_PK == status_id
    ).first()
    
    if not status:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(status, key, value)

    db.commit()
    db.refresh(status)
    return status


# -------------------------
# DELETE
# -------------------------
def delete_organization_status(db: Session, status_id: int):
    status = db.query(OrganizationStatuses).filter(
        OrganizationStatuses.ORST_PK == status_id
    ).first()
    
    if not status:
        return None

    db.delete(status)
    db.commit()
    return status
