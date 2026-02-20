from sqlalchemy.orm import Session
from sqlalchemy import or_, inspect
from Models.persons.ethnicityModel import Ethnicity
from typing import Optional, List

def get_all_ethnicities(db: Session, include_inactive: bool = False):
    """Obtiene todas las etnias. Por defecto solo las activas."""
    query = db.query(Ethnicity)
    if not include_inactive and hasattr(Ethnicity, 'ETNC_state'):
        query = query.filter(Ethnicity.ETNC_state == 1)
    return query.all()

def get_ethnicity_by_id(db: Session, ethnicity_id: int):
    """Obtiene una etnia por su ID."""
    return db.query(Ethnicity).filter(Ethnicity.ETNC_PK == ethnicity_id).first()

def search_ethnicities(
    db: Session,
    name: Optional[str] = None,
    include_inactive: bool = False
):
    """Busca etnias por múltiples criterios."""
    query = db.query(Ethnicity)
    
    if not include_inactive and hasattr(Ethnicity, 'ETNC_state'):
        query = query.filter(Ethnicity.ETNC_state == 1)
    
    filters = []
    if name:
        filters.append(Ethnicity.ETNC_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_ethnicity(db: Session, ethnicity_data):
    """Crea una nueva etnia."""
    ethnicity_dict = ethnicity_data.dict(exclude_unset=True)
    new_ethnicity = Ethnicity(**ethnicity_dict)
    db.add(new_ethnicity)
    db.commit()
    db.refresh(new_ethnicity)
    return new_ethnicity

def update_ethnicity(db: Session, ethnicity_id: int, ethnicity_data):
    """Actualiza una etnia existente."""
    ethnicity = get_ethnicity_by_id(db, ethnicity_id)
    if not ethnicity:
        return None
    
    update_data = ethnicity_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(ethnicity, key, value)
    
    db.commit()
    db.refresh(ethnicity)
    return ethnicity

def delete_ethnicity(db: Session, ethnicity_id: int):
    """Elimina permanentemente una etnia de la base de datos."""
    ethnicity = get_ethnicity_by_id(db, ethnicity_id)
    if not ethnicity:
        return None
    
    db.delete(ethnicity)
    db.commit()
    return ethnicity

def deactivate_ethnicity(db: Session, ethnicity_id: int):
    """Inactiva una etnia (soft delete usando campo de estado)."""
    ethnicity = get_ethnicity_by_id(db, ethnicity_id)
    if not ethnicity:
        return None
    
    if not hasattr(Ethnicity, 'ETNC_state'):
        raise ValueError("El campo ETNC_state no existe en la base de datos.")
    
    ethnicity.ETNC_state = 0
    db.commit()
    db.refresh(ethnicity)
    return ethnicity

def activate_ethnicity(db: Session, ethnicity_id: int):
    """Activa una etnia previamente inactivada."""
    ethnicity = get_ethnicity_by_id(db, ethnicity_id)
    if not ethnicity:
        return None
    
    if not hasattr(Ethnicity, 'ETNC_state'):
        raise ValueError("El campo ETNC_state no existe en la base de datos.")
    
    ethnicity.ETNC_state = 1
    db.commit()
    db.refresh(ethnicity)
    return ethnicity
