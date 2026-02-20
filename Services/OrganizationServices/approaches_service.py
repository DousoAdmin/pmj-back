from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.Organizations.approachesModel import Approaches
from typing import Optional

def get_all_approaches(db: Session):
    """Obtiene todos los enfoques."""
    return db.query(Approaches).all()

def get_approach_by_id(db: Session, approach_id: int):
    """Obtiene un enfoque por su ID."""
    return db.query(Approaches).filter(Approaches.APCH_PK == approach_id).first()

def search_approaches(
    db: Session,
    name: Optional[str] = None
):
    """Busca enfoques por múltiples criterios."""
    query = db.query(Approaches)
    
    filters = []
    if name:
        filters.append(Approaches.APCH_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_approach(db: Session, approach_data):
    """Crea un nuevo enfoque."""
    approach_dict = approach_data.dict(exclude_unset=True)
    new_approach = Approaches(**approach_dict)
    db.add(new_approach)
    db.commit()
    db.refresh(new_approach)
    return new_approach

def update_approach(db: Session, approach_id: int, approach_data):
    """Actualiza un enfoque existente."""
    approach = get_approach_by_id(db, approach_id)
    if not approach:
        return None
    
    update_data = approach_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(approach, key, value)
    
    db.commit()
    db.refresh(approach)
    return approach

def delete_approach(db: Session, approach_id: int):
    """Elimina permanentemente un enfoque de la base de datos."""
    approach = get_approach_by_id(db, approach_id)
    if not approach:
        return None
    
    db.delete(approach)
    db.commit()
    return approach
