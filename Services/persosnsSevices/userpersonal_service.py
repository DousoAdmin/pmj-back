from sqlalchemy.orm import Session
from Models.persons.userpersonalModel import UserPersonas
from datetime import date
from typing import Optional

def get_all_user_personas(db: Session, include_inactive: bool = False):
    """Obtiene todas las asociaciones de usuarios y personas. Por defecto solo las activas."""
    query = db.query(UserPersonas)
    if not include_inactive:
        query = query.filter(UserPersonas.USPS_state == 1)
    return query.all()

def get_user_persona_by_id(db: Session, usps_id: int):
    """Obtiene una asociación de usuario y persona por su ID."""
    return db.query(UserPersonas).filter(UserPersonas.USPS_PK == usps_id).first()

def get_user_personas_by_user(db: Session, user_id: int, include_inactive: bool = False):
    """Obtiene todas las asociaciones de un usuario específico."""
    query = db.query(UserPersonas).filter(UserPersonas.USPS_FK_user == user_id)
    if not include_inactive:
        query = query.filter(UserPersonas.USPS_state == 1)
    return query.all()

def get_user_personas_by_person(db: Session, person_id: int, include_inactive: bool = False):
    """Obtiene todas las asociaciones de una persona específica."""
    query = db.query(UserPersonas).filter(UserPersonas.USPS_FK_person == person_id)
    if not include_inactive:
        query = query.filter(UserPersonas.USPS_state == 1)
    return query.all()

def create_user_persona(db: Session, user_persona_data):
    """Crea una nueva asociación entre un usuario y una persona."""
    if hasattr(user_persona_data, "dict"):
        up_dict = user_persona_data.dict(exclude_unset=True)
    else:
        up_dict = dict(user_persona_data)
        
    if "USPS_date_create" not in up_dict or up_dict["USPS_date_create"] is None:
        up_dict["USPS_date_create"] = date.today()
    if "USPS_state" not in up_dict or up_dict["USPS_state"] is None:
        up_dict["USPS_state"] = 1
        
    new_up = UserPersonas(**up_dict)
    db.add(new_up)
    db.commit()
    db.refresh(new_up)
    return new_up

def update_user_persona(db: Session, usps_id: int, user_persona_data):
    """Actualiza una asociación usuario-persona existente."""
    up = get_user_persona_by_id(db, usps_id)
    if not up:
        return None
        
    if hasattr(user_persona_data, "dict"):
        update_data = user_persona_data.dict(exclude_unset=True)
    else:
        update_data = dict(user_persona_data)
        
    if "USPS_date_update" not in update_data or update_data["USPS_date_update"] is None:
        update_data["USPS_date_update"] = date.today()
        
    for key, value in update_data.items():
        setattr(up, key, value)
        
    db.commit()
    db.refresh(up)
    return up

def delete_user_persona(db: Session, usps_id: int):
    """Elimina permanentemente una asociación usuario-persona."""
    up = get_user_persona_by_id(db, usps_id)
    if not up:
        return None
        
    db.delete(up)
    db.commit()
    return up

def deactivate_user_persona(db: Session, usps_id: int):
    """Inactiva una asociación usuario-persona (soft delete)."""
    up = get_user_persona_by_id(db, usps_id)
    if not up:
        return None
        
    up.USPS_state = 0
    up.USPS_date_update = date.today()
    db.commit()
    db.refresh(up)
    return up

def activate_user_persona(db: Session, usps_id: int):
    """Activa una asociación usuario-persona inactivada."""
    up = get_user_persona_by_id(db, usps_id)
    if not up:
        return None
        
    up.USPS_state = 1
    up.USPS_date_update = date.today()
    db.commit()
    db.refresh(up)
    return up
