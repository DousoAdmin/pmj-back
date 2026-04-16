from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Core.security import get_current_user
from Schemas.organizationSchema.organization_Shema import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
    OrganizationOut,
)
from Services.OrganizationServices import organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/organization", response_model=list[OrganizationOut])
def list_organizations(db: Session = Depends(get_db)):
    return organization_service.get_organization(db)


@router.get("/{org_id}", response_model=OrganizationOut)
def get_organization_by_id(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: OrganizationResponse = Depends(get_current_user),
):
    org = organization_service.get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(404, "Organization not found")
    return org


@router.post("/New", response_model=OrganizationOut)
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: OrganizationResponse = Depends(get_current_user),
):
    return organization_service.create_organization(db, data)


@router.put("/{org_id}", response_model=OrganizationOut)
def update_organization(
    org_id: int,
    data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: OrganizationResponse = Depends(get_current_user),
):
    org = organization_service.update_organization(db, org_id, data)
    if not org:
        raise HTTPException(404, "Organization not found")
    return org


@router.delete("/{org_id}")
def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: OrganizationResponse = Depends(get_current_user),
):
    org = organization_service.delete_organization(db, org_id)
    if not org:
        raise HTTPException(404, "Organization not found")
    return {"message": "Organization deleted"}
