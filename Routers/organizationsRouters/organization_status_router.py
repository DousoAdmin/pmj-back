from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Core.security import get_current_user
from Schemas.organizationSchema.organization_status_schema import (
    OrganizationStatusCreate,
    OrganizationStatusResponse,
    OrganizationStatusUpdate,
    OrganizationStatusOut
)
from Services.organizationServices import organization_status_service

router = APIRouter(prefix="/organization-statuses", tags=["organization-statuses"])


# -------------------------
# GET ALL
# -------------------------
@router.get("/", response_model=list[OrganizationStatusOut])
def list_organization_statuses(db: Session = Depends(get_db)):
    statuses = organization_status_service.get_organization_statuses(db)
    return statuses


# -------------------------
# GET BY ID
# -------------------------
@router.get("/{status_id}", response_model=OrganizationStatusOut)
def get_organization_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: OrganizationStatusResponse = Depends(get_current_user)
):
    status = organization_status_service.get_organization_status(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


# -------------------------
# CREATE
# -------------------------
@router.post("/", response_model=OrganizationStatusOut)
def create_organization_status(
    data: OrganizationStatusCreate,
    db: Session = Depends(get_db),
    current_user: OrganizationStatusResponse = Depends(get_current_user)
):
    return organization_status_service.create_organization_status(db, data)


# -------------------------
# UPDATE
# -------------------------
@router.put("/{status_id}", response_model=OrganizationStatusOut)
def update_organization_status(
    status_id: int,
    data: OrganizationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: OrganizationStatusResponse = Depends(get_current_user)
):
    status = organization_status_service.update_organization_status(db, status_id, data)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


# -------------------------
# DELETE
# -------------------------
@router.delete("/{status_id}")
def delete_organization_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: OrganizationStatusResponse = Depends(get_current_user)
):
    status = organization_status_service.delete_organization_status(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return {"message": "Status deleted successfully"}
