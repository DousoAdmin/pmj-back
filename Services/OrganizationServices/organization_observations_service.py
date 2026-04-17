from sqlalchemy.orm import Session
from Models.organizations.organization_observations_model import OrganizationObservations
from Schemas.organizationSchema.organization_observations_shema import (
    OrganizationObsarvationCreate,
    OrganizationObservationUpdate,
    OrganizationObservationOut,
    OrganizationObservationResponse
)
from datetime import date



def create_observation(
    db: Session,
    observation: OrganizationObsarvationCreate
):
    db_observation = OrganizationObservations(
        OROB_FK_document=observation.OROB_FK_document,
        OROB_comment=observation.OROB_comment,
        OROB_status=observation.OROB_status,
        OROB_date_create=observation.OROB_date_create or date.today(),
        OROB_user_create=observation.OROB_user_create
    )

    db.add(db_observation)
    db.commit()
    db.refresh(db_observation)
    return db_observation



def get_observations(db: Session):
    return db.query(OrganizationObservations).all()



def get_observation_by_id(
    db: Session,
    observation_id: int
):
    return (
        db.query(OrganizationObservations)
        .filter(OrganizationObservations.OROB_PK == observation_id)
        .first()
    )



def get_observations_by_document(
    db: Session,
    document_id: int
):
    return (
        db.query(OrganizationObservations)
        .filter(OrganizationObservations.OROB_FK_document == document_id)
        .all()
    )



def update_observation(
    db: Session,
    observation_id: int,
    observation_data: OrganizationObservationUpdate
):
    observation = get_observation_by_id(db, observation_id)

    if not observation:
        return None

    if observation_data.OROB_comment is not None:
        observation.OROB_comment = observation_data.OROB_comment

    if observation_data.OROB_status is not None:
        observation.OROB_status = observation_data.OROB_status

    db.commit()
    db.refresh(observation)
    return observation



def delete_observation(
    db: Session,
    observation_id: int
):
    observation = get_observation_by_id(db, observation_id)

    if not observation:
        return None

    db.delete(observation)
    db.commit()
    return observation





