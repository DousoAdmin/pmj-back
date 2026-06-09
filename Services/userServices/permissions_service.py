from sqlalchemy.orm import Session
from Models.users.permissionsModel import Permissions
from datetime import date
from typing import Optional

def get_all_permissions(db: Session):
    """Obtiene todos los permisos."""
    return db.query(Permissions).all()

def get_permission_by_id(db: Session, permission_id: int):
    """Obtiene un permiso por su ID."""
    return db.query(Permissions).filter(Permissions.PRMS_PK == permission_id).first()

def get_permission_by_system_name(db: Session, system_name: str):
    """Obtiene un permiso por su nombre de sistema."""
    return db.query(Permissions).filter(Permissions.PRMS_system_name == system_name).first()

def create_permission(db: Session, permission_data):
    """Crea un nuevo permiso."""
    if hasattr(permission_data, "dict"):
        permission_dict = permission_data.dict(exclude_unset=True)
    else:
        permission_dict = dict(permission_data)
        
    if "PRMS_date_create" not in permission_dict or permission_dict["PRMS_date_create"] is None:
        permission_dict["PRMS_date_create"] = date.today()
        
    new_permission = Permissions(**permission_dict)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

def update_permission(db: Session, permission_id: int, permission_data):
    """Actualiza un permiso existente."""
    permission = get_permission_by_id(db, permission_id)
    if not permission:
        return None
        
    if hasattr(permission_data, "dict"):
        update_data = permission_data.dict(exclude_unset=True)
    else:
        update_data = dict(permission_data)
        
    if "PRMS_date_update" not in update_data or update_data["PRMS_date_update"] is None:
        update_data["PRMS_date_update"] = date.today()
        
    for key, value in update_data.items():
        setattr(permission, key, value)
        
    db.commit()
    db.refresh(permission)
    return permission

def delete_permission(db: Session, permission_id: int):
    """Elimina permanentemente un permiso."""
    permission = get_permission_by_id(db, permission_id)
    if not permission:
        return None
        
    db.delete(permission)
    db.commit()
    return permission
