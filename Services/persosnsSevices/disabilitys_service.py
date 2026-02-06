from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.disabilitysModel import Disabilitys
from typing import Optional

def get_all_disabilitys(db: Session, include_inactive: bool = False):
    """Obtiene todas las discapacidades. Por defecto solo las activas."""
    query = db.query(Disabilitys)
    if not include_inactive and hasattr(Disabilitys, 'DSBT_state'):
        query = query.filter(Disabilitys.DSBT_state == 1)
    return query.all()

def get_disability_by_id(db: Session, disability_id: int):
    """Obtiene una discapacidad por su ID."""
    return db.query(Disabilitys).filter(Disabilitys.DSBT_PY == disability_id).first()

def search_disabilitys(
    db: Session,
    name: Optional[str] = None,
    include_inactive: bool = False
):
    """Busca discapacidades por múltiples criterios."""
    query = db.query(Disabilitys)
    
    if not include_inactive and hasattr(Disabilitys, 'DSBT_state'):
        query = query.filter(Disabilitys.DSBT_state == 1)
    
    filters = []
    if name:
        filters.append(Disabilitys.DSBT_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_disability(db: Session, disability_data):
    """Crea una nueva discapacidad."""
    disability_dict = disability_data.dict(exclude_unset=True)
    new_disability = Disabilitys(**disability_dict)
    db.add(new_disability)
    db.commit()
    db.refresh(new_disability)
    return new_disability

def update_disability(db: Session, disability_id: int, disability_data):
    """Actualiza una discapacidad existente."""
    disability = get_disability_by_id(db, disability_id)
    if not disability:
        return None
    
    update_data = disability_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(disability, key, value)
    
    db.commit()
    db.refresh(disability)
    return disability

def delete_disability(db: Session, disability_id: int):
    """Elimina permanentemente una discapacidad de la base de datos."""
    disability = get_disability_by_id(db, disability_id)
    if not disability:
        return None
    
    db.delete(disability)
    db.commit()
    return disability

def deactivate_disability(db: Session, disability_id: int):
    """Inactiva una discapacidad (soft delete usando campo de estado)."""
    disability = get_disability_by_id(db, disability_id)
    if not disability:
        return None
    
    if not hasattr(Disabilitys, 'DSBT_state'):
        raise ValueError("El campo DSBT_state no existe en la base de datos.")
    
    disability.DSBT_state = 0
    db.commit()
    db.refresh(disability)
    return disability

def activate_disability(db: Session, disability_id: int):
    """Activa una discapacidad previamente inactivada."""
    disability = get_disability_by_id(db, disability_id)
    if not disability:
        return None
    
    if not hasattr(Disabilitys, 'DSBT_state'):
        raise ValueError("El campo DSBT_state no existe en la base de datos.")
    
    disability.DSBT_state = 1
    db.commit()
    db.refresh(disability)
    return disability
