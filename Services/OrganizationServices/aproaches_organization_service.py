from sqlalchemy.orm import Session
from Models.organizations.approaches_model import Approaches
from Schemas.organizationSchema.or_aproaches_shema import (
    AorpachesOrganizationCreate,
    AproacheOrganizationOut,
    AproachesOrganizationResponse,
    AproachesOrganizationUpdate
)
from datetime import date



def create_approach(
    db: Session,
    approach: AorpachesOrganizationCreate
):
    db_approach = Approaches(
        APCH_name=approach.APCH_name,
        APCH_description=approach.APCH_description,
        APCH_date_create=approach.APCH_date_create or date.today()
    )

    db.add(db_approach)
    db.commit()
    db.refresh(db_approach)
    return db_approach



def get_approaches(db: Session):
    return db.query(Approaches).all()



def get_approach_by_id(
    db: Session,
    approach_id: int
):
    return (
        db.query(Approaches)
        .filter(Approaches.APCH_PK == approach_id)
        .first()
    )



def update_approach(
    db: Session,
    approach_id: int,
    approach_data: AproachesOrganizationUpdate
):
    approach = get_approach_by_id(db, approach_id)

    if not approach:
        return None

    if approach_data.APCH_name is not None:
        approach.APCH_name = approach_data.APCH_name

    if approach_data.APCH_description is not None:
        approach.APCH_description = approach_data.APCH_description

    db.commit()
    db.refresh(approach)
    return approach



def delete_approach(
    db: Session,
    approach_id: int
):
    approach = get_approach_by_id(db, approach_id)

    if not approach:
        return None

    db.delete(approach)
    db.commit()
    return approach



