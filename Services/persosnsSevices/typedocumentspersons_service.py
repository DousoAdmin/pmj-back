from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from Models.persons.typedocumentspersonsModel import TypeDocumentsPersons


def get_all_type_documents_persons(db: Session):
    return db.query(TypeDocumentsPersons).all()


def get_type_document_person_by_id(db: Session, tpdu_id: int):
    return db.query(TypeDocumentsPersons).filter(TypeDocumentsPersons.TPDU_PK == tpdu_id).first()


def search_type_documents_persons(
    db: Session,
    name: Optional[str] = None,
    code: Optional[str] = None,
):
    query = db.query(TypeDocumentsPersons)

    filters = []
    if name:
        filters.append(TypeDocumentsPersons.TPDU_name.ilike(f"%{name}%"))
    if code:
        filters.append(TypeDocumentsPersons.TPDU_code.ilike(f"%{code}%"))

    if filters:
        query = query.filter(or_(*filters))

    return query.all()


def create_type_document_person(db: Session, type_document_data):
    payload = type_document_data.model_dump(exclude_unset=True) if hasattr(type_document_data, "model_dump") else type_document_data.dict(exclude_unset=True)
    new_item = TypeDocumentsPersons(**payload)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_type_document_person(db: Session, tpdu_id: int, type_document_data):
    item = get_type_document_person_by_id(db, tpdu_id)
    if not item:
        return None

    update_data = type_document_data.model_dump(exclude_unset=True) if hasattr(type_document_data, "model_dump") else type_document_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_type_document_person(db: Session, tpdu_id: int):
    item = get_type_document_person_by_id(db, tpdu_id)
    if not item:
        return None

    db.delete(item)
    db.commit()
    return item
