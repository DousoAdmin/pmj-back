from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.documentstatesModel import DocumentStates
from typing import Optional

def get_all_documentstates(db: Session):
    """Obtiene todos los estados de documentos."""
    return db.query(DocumentStates).all()

def get_documentstate_by_id(db: Session, documentstate_id: int):
    """Obtiene un estado de documento por su ID."""
    return db.query(DocumentStates).filter(DocumentStates.DCST_PK == documentstate_id).first()

def search_documentstates(
    db: Session,
    name: Optional[str] = None
):
    """Busca estados de documentos por múltiples criterios."""
    query = db.query(DocumentStates)
    
    filters = []
    if name:
        filters.append(DocumentStates.DCST_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_documentstate(db: Session, documentstate_data):
    """Crea un nuevo estado de documento."""
    documentstate_dict = documentstate_data.dict(exclude_unset=True)
    new_documentstate = DocumentStates(**documentstate_dict)
    db.add(new_documentstate)
    db.commit()
    db.refresh(new_documentstate)
    return new_documentstate

def update_documentstate(db: Session, documentstate_id: int, documentstate_data):
    """Actualiza un estado de documento existente."""
    documentstate = get_documentstate_by_id(db, documentstate_id)
    if not documentstate:
        return None
    
    update_data = documentstate_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(documentstate, key, value)
    
    db.commit()
    db.refresh(documentstate)
    return documentstate

def delete_documentstate(db: Session, documentstate_id: int):
    """Elimina permanentemente un estado de documento de la base de datos."""
    documentstate = get_documentstate_by_id(db, documentstate_id)
    if not documentstate:
        return None
    
    db.delete(documentstate)
    db.commit()
    return documentstate
