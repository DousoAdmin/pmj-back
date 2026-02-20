from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.gendersModel import Genders
from typing import Optional

def get_all_genders(db: Session, include_inactive: bool = False):
    """Obtiene todos los géneros. Por defecto solo los activos."""
    query = db.query(Genders)
    if not include_inactive and hasattr(Genders, 'GNDR_state'):
        query = query.filter(Genders.GNDR_state == 1)
    return query.all()

def get_gender_by_id(db: Session, gender_id: int):
    """Obtiene un género por su ID."""
    return db.query(Genders).filter(Genders.GNDR_PK == gender_id).first()

def search_genders(
    db: Session,
    name: Optional[str] = None,
    include_inactive: bool = False
):
    """Busca géneros por múltiples criterios."""
    query = db.query(Genders)
    
    if not include_inactive and hasattr(Genders, 'GNDR_state'):
        query = query.filter(Genders.GNDR_state == 1)
    
    filters = []
    if name:
        filters.append(Genders.GNDR_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_gender(db: Session, gender_data):
    """Crea un nuevo género."""
    gender_dict = gender_data.dict(exclude_unset=True)
    new_gender = Genders(**gender_dict)
    db.add(new_gender)
    db.commit()
    db.refresh(new_gender)
    return new_gender

def update_gender(db: Session, gender_id: int, gender_data):
    """Actualiza un género existente."""
    gender = get_gender_by_id(db, gender_id)
    if not gender:
        return None
    
    update_data = gender_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(gender, key, value)
    
    db.commit()
    db.refresh(gender)
    return gender

def delete_gender(db: Session, gender_id: int):
    """Elimina permanentemente un género de la base de datos."""
    gender = get_gender_by_id(db, gender_id)
    if not gender:
        return None
    
    db.delete(gender)
    db.commit()
    return gender

def deactivate_gender(db: Session, gender_id: int):
    """Inactiva un género (soft delete usando campo de estado)."""
    gender = get_gender_by_id(db, gender_id)
    if not gender:
        return None
    
    if not hasattr(Genders, 'GNDR_state'):
        raise ValueError("El campo GNDR_state no existe en la base de datos.")
    
    gender.GNDR_state = 0
    db.commit()
    db.refresh(gender)
    return gender

def activate_gender(db: Session, gender_id: int):
    """Activa un género previamente inactivado."""
    gender = get_gender_by_id(db, gender_id)
    if not gender:
        return None
    
    if not hasattr(Genders, 'GNDR_state'):
        raise ValueError("El campo GNDR_state no existe en la base de datos.")
    
    gender.GNDR_state = 1
    db.commit()
    db.refresh(gender)
    return gender
