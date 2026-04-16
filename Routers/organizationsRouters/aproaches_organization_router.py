from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.or_aproaches_shema import (
    AorpachesOrganizationCreate,
    AproacheOrganizationOut,
    AproachesOrganizationResponse,
    AproachesOrganizationUpdate
)
from Services.OrganizationServices.aproaches_organization_service import (
    create_approach,
    get_approaches,
    get_approach_by_id,
    update_approach,
    delete_approach
)
router = APIRouter(
    prefix="/approaches",
    tags=["Approaches"]
)




@router.post("/", response_model=AproachesOrganizationResponse)
def create(
    approach: AorpachesOrganizationCreate,
    db: Session = Depends(get_db)
):
    return create_approach(db, approach)




@router.get("/", response_model=list[AproachesOrganizationResponse])
def get_all(db: Session = Depends(get_db)):
    return get_approaches(db)



@router.get("/{approach_id}", response_model=AproachesOrganizationResponse)
def get_by_id(
    approach_id: int,
    db: Session = Depends(get_db)
):
    approach = get_approach_by_id(db, approach_id)

    if not approach:
        raise HTTPException(status_code=404, detail="Approach not found")

    return approach



@router.put("/{approach_id}", response_model=AproachesOrganizationResponse)
def update(
    approach_id: int,
    approach_data: AproachesOrganizationUpdate,
    db: Session = Depends(get_db)
):
    approach = update_approach(db, approach_id, approach_data)

    if not approach:
        raise HTTPException(status_code=404, detail="Approach not found")

    return approach




@router.delete("/{approach_id}")
def delete(
    approach_id: int,
    db: Session = Depends(get_db)
):
    approach = delete_approach(db, approach_id)

    if not approach:
        raise HTTPException(status_code=404, detail="Approach not found")

    return {"message": "Approach deleted successfully"}



