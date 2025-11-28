from sqlalchemy.orm import Session
import Models

def get_all_persons(db: Session):
    return db.query(Models.persons.personsModel.Persons).all()

def get_person_by_id(db: Session, person_id: int):
    return db.query(Models.persons.personsModel.Persons).filter(Models.persons.personsModel.Persons.PRSN_PK == person_id).first()

def create_person(db: Session, person_data):
    new_person = Models.persons.personsModel.Persons(**person_data.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person