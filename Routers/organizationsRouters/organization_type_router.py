from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_type_shema import (
    OrganizationTypeCreate,
    OrganizationTypeUpdate,
    OrganizationTypeResponse
)
from Services.OrganizationServices.organization_type_service import (
    create_organization_type,
    get_organization_types,
    get_organization_type_by_id,
    update_organization_type,
    delete_organization_type
)


router = APIRouter(
    prefix="/organization-types",
    tags=["Organization Types"]
)



@router.post("/", response_model=OrganizationTypeResponse)
def create(
    org_type: OrganizationTypeCreate,
    db: Session = Depends(get_db)
):
    return create_organization_type(db, org_type)



@router.get("/", response_model=list[OrganizationTypeResponse])
def get_all(db: Session = Depends(get_db)):
    return get_organization_types(db)



@router.get("/{org_type_id}", response_model=OrganizationTypeResponse)
def get_by_id(
    org_type_id: int,
    db: Session = Depends(get_db)
):
    org_type = get_organization_type_by_id(db, org_type_id)

    if not org_type:
        raise HTTPException(status_code=404, detail="Organization Type not found")

    return org_type



@router.put("/{org_type_id}", response_model=OrganizationTypeResponse)
def update(
    org_type_id: int,
    org_type_data: OrganizationTypeUpdate,
    db: Session = Depends(get_db)
):
    org_type = update_organization_type(db, org_type_id, org_type_data)

    if not org_type:
        raise HTTPException(status_code=404, detail="Organization Type not found")

    return org_type



@router.delete("/{org_type_id}")
def delete(
    org_type_id: int,
    db: Session = Depends(get_db)
):
    org_type = delete_organization_type(db, org_type_id)

    if not org_type:
        raise HTTPException(status_code=404, detail="Organization Type not found")

    return {"message": "Organization Type deleted successfully"}
