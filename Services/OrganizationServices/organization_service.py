from sqlalchemy.orm import Session
from Models.Organizations.organizations_model import Organizations
from Schemas.organizationSchema.organization_Shema import OrganizationCreate, OrganizationUpdate


def get_organization(db: Session):
    return db.query(Organizations).all()


def get_organization_by_id(db: Session, org_id: int):
    return db.query(Organizations).filter(Organizations.ORGZ_PK == org_id).first()


def create_organization(db: Session, data: OrganizationCreate):
    payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
    payload["ORGZ_creation_date"] = payload.pop("ORGZ_create_date", None)
    payload["ORGZ_FK_statu"] = payload.pop("ORGZ_FK_status", None)
    org = Organizations(**payload)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def update_organization(db: Session, org_id: int, data: OrganizationUpdate):
    org = get_organization_by_id(db, org_id)
    if not org:
        return None

    update_data = data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else data.dict(exclude_unset=True)
    if "ORGZ_create_date" in update_data:
        update_data["ORGZ_creation_date"] = update_data.pop("ORGZ_create_date")
    if "ORGZ_FK_status" in update_data:
        update_data["ORGZ_FK_statu"] = update_data.pop("ORGZ_FK_status")

    for key, value in update_data.items():
        setattr(org, key, value)

    db.commit()
    db.refresh(org)
    return org


def delete_organization(db: Session, org_id: int):
    org = get_organization_by_id(db, org_id)
    if not org:
        return None
    db.delete(org)
    db.commit()
    return org
