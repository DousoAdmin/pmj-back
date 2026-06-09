from sqlalchemy.orm import Session
from Models.users.rolesModel import Roles
from datetime import date
from typing import Optional

def get_all_roles(db: Session, include_inactive: bool = False):
    """Obtiene todos los roles. Por defecto solo los activos."""
    query = db.query(Roles)
    if not include_inactive:
        query = query.filter(Roles.ROLE_state == 1)
    return query.all()

def get_role_by_id(db: Session, role_id: int):
    """Obtiene un rol por su ID."""
    return db.query(Roles).filter(Roles.ROLE_PK == role_id).first()

def get_role_by_name(db: Session, name: str):
    """Obtiene un rol por su nombre."""
    return db.query(Roles).filter(Roles.ROLE_name == name).first()

def create_role(db: Session, role_data):
    """Crea un nuevo rol."""
    if hasattr(role_data, "dict"):
        role_dict = role_data.dict(exclude_unset=True)
    else:
        role_dict = dict(role_data)
        
    if "ROLE_date_create" not in role_dict or role_dict["ROLE_date_create"] is None:
        role_dict["ROLE_date_create"] = date.today()
    if "ROLE_state" not in role_dict or role_dict["ROLE_state"] is None:
        role_dict["ROLE_state"] = 1
        
    new_role = Roles(**role_dict)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def update_role(db: Session, role_id: int, role_data):
    """Actualiza un rol existente."""
    role = get_role_by_id(db, role_id)
    if not role:
        return None
        
    if hasattr(role_data, "dict"):
        update_data = role_data.dict(exclude_unset=True)
    else:
        update_data = dict(role_data)
        
    if "ROLE_date_update" not in update_data or update_data["ROLE_date_update"] is None:
        update_data["ROLE_date_update"] = date.today()
        
    for key, value in update_data.items():
        setattr(role, key, value)
        
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    """Elimina permanentemente un rol de la base de datos."""
    role = get_role_by_id(db, role_id)
    if not role:
        return None
        
    db.delete(role)
    db.commit()
    return role

def deactivate_role(db: Session, role_id: int):
    """Inactiva un rol (soft delete)."""
    role = get_role_by_id(db, role_id)
    if not role:
        return None
        
    role.ROLE_state = 0
    role.ROLE_date_update = date.today()
    db.commit()
    db.refresh(role)
    return role

def activate_role(db: Session, role_id: int):
    """Activa un rol inactivo."""
    role = get_role_by_id(db, role_id)
    if not role:
        return None
        
    role.ROLE_state = 1
    role.ROLE_date_update = date.today()
    db.commit()
    db.refresh(role)
    return role
