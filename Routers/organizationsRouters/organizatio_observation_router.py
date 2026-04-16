from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_observations_shema import (
    OrganizationObsarvationCreate,
    OrganizationObservationUpdate,
    OrganizationObservationOut,
    OrganizationObservationResponse
)
from Services.OrganizationServices.organization_observations_service import (
    create_observation,
    get_observations,
    get_observation_by_id,
    get_observations_by_document,
    update_observation,
    delete_observation
)
router = APIRouter(
    prefix="/organization-observations",
    tags=["Organization Observations"]
)


@router.post("/", response_model=OrganizationObservationResponse)
def create(
    observation: OrganizationObsarvationCreate,
    db: Session = Depends(get_db)
):
    return create_observation(db, observation)


@router.get("/", response_model=list[OrganizationObservationResponse])
def get_all(db: Session = Depends(get_db)):
    return get_observations(db)


@router.get("/{observation_id}", response_model=OrganizationObservationResponse)
def get_by_id(
    observation_id: int,
    db: Session = Depends(get_db)
):
    observation = get_observation_by_id(db, observation_id)

    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")

    return observation


@router.get("/document/{document_id}", response_model=list[OrganizationObservationResponse])
def get_by_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return get_observations_by_document(db, document_id)


@router.put("/{observation_id}", response_model=OrganizationObservationResponse)
def update(
    observation_id: int,
    observation_data: OrganizationObservationUpdate,
    db: Session = Depends(get_db)
):
    observation = update_observation(db, observation_id, observation_data)

    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")

    return observation


@router.delete("/{observation_id}")
def delete(
    observation_id: int,
    db: Session = Depends(get_db)
):
    observation = delete_observation(db, observation_id)

    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")

    return {"message": "Observation deleted successfully"}
