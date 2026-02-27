from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_aproaches_shema import (
    OrganizatioAprochesUpdate,
    OrganizatioAproachesOut,
    OrganizationAproachesCreate,
    OrganizationAproachesResponse
)
from Services.organizationServices.organization_aproaches_services import (
    create_organization_approach,
    get_organization_approaches,
    get_organization_approach_by_id,
    get_approaches_by_organization,
    update_organization_approach,
    delete_organization_approach
)
router = APIRouter(
    prefix="/organization-approaches",
    tags=["Organization Approaches"]
)



@router.post("/", response_model=OrganizationAproachesResponse)
def create(
    org_approach: OrganizationAproachesCreate,
    db: Session = Depends(get_db)
):
    return create_organization_approach(db, org_approach)



@router.get("/", response_model=list[OrganizationAproachesResponse])
def get_all(db: Session = Depends(get_db)):
    return get_organization_approaches(db)



@router.get("/{org_approach_id}", response_model=OrganizationAproachesResponse)
def get_by_id(
    org_approach_id: int,
    db: Session = Depends(get_db)
):
    org_approach = get_organization_approach_by_id(db, org_approach_id)

    if not org_approach:
        raise HTTPException(status_code=404, detail="Organization approach not found")

    return org_approach



@router.get("/organization/{organization_id}", response_model=list[OrganizationAproachesResponse])
def get_by_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    return get_approaches_by_organization(db, organization_id)




@router.put("/{org_approach_id}", response_model=OrganizationAproachesResponse)
def update(
    org_approach_id: int,
    org_approach_data: OrganizatioAprochesUpdate,
    db: Session = Depends(get_db)
):
    org_approach = update_organization_approach(db, org_approach_id, org_approach_data)

    if not org_approach:
        raise HTTPException(status_code=404, detail="Organization approach not found")

    return org_approach



@router.delete("/{org_approach_id}")
def delete(
    org_approach_id: int,
    db: Session = Depends(get_db)
):
    org_approach = delete_organization_approach(db, org_approach_id)

    if not org_approach:
        raise HTTPException(status_code=404, detail="Organization approach not found")

    return {"message": "Organization approach deleted successfully"}
