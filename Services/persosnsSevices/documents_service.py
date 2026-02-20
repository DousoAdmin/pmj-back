from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.documentsModel import Documents
from typing import Optional

def get_all_documents(db: Session):
    """Obtiene todos los documentos."""
    return db.query(Documents).all()

def get_document_by_id(db: Session, document_id: int):
    """Obtiene un documento por su ID."""
    return db.query(Documents).filter(Documents.DCMT_PK == document_id).first()

def search_documents(
    db: Session,
    name: Optional[str] = None
):
    """Busca documentos por múltiples criterios."""
    query = db.query(Documents)
    
    filters = []
    if name:
        filters.append(Documents.DCMT_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_document(db: Session, document_data):
    """Crea un nuevo documento."""
    document_dict = document_data.dict(exclude_unset=True)
    # Convertir valores 0 en claves foráneas a None
    if 'DCMT_FK_state' in document_dict and document_dict['DCMT_FK_state'] == 0:
        document_dict['DCMT_FK_state'] = None
    new_document = Documents(**document_dict)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

def update_document(db: Session, document_id: int, document_data):
    """Actualiza un documento existente."""
    document = get_document_by_id(db, document_id)
    if not document:
        return None
    
    update_data = document_data.dict(exclude_unset=True)
    
    # Convertir valores 0 en claves foráneas a None
    if 'DCMT_FK_state' in update_data and update_data['DCMT_FK_state'] == 0:
        update_data['DCMT_FK_state'] = None
    
    for key, value in update_data.items():
        setattr(document, key, value)
    
    db.commit()
    db.refresh(document)
    return document

def delete_document(db: Session, document_id: int):
    """Elimina permanentemente un documento de la base de datos."""
    document = get_document_by_id(db, document_id)
    if not document:
        return None
    
    db.delete(document)
    db.commit()
    return document
