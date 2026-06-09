from sqlalchemy.orm import Session
from Models.users.rolesPermissionModel import RolesPermissions
from datetime import date
from typing import Optional

def get_all_roles_permissions(db: Session, include_inactive: bool = False):
    """Obtiene todas las relaciones de roles y permisos. Por defecto solo las activas."""
    query = db.query(RolesPermissions)
    if not include_inactive:
        query = query.filter(RolesPermissions.RLPR_state == 1)
    return query.all()

def get_role_permission_by_id(db: Session, role_permission_id: int):
    """Obtiene una relación de rol y permiso por su ID."""
    return db.query(RolesPermissions).filter(RolesPermissions.RLPR_PK == role_permission_id).first()

def get_permissions_by_role(db: Session, role_id: int, include_inactive: bool = False):
    """Obtiene todos los permisos asignados a un rol específico."""
    query = db.query(RolesPermissions).filter(RolesPermissions.RLPR_FK_rol == role_id)
    if not include_inactive:
        query = query.filter(RolesPermissions.RLPR_state == 1)
    return query.all()

def create_role_permission(db: Session, role_permission_data):
    """Crea una nueva asociación entre rol y permiso."""
    if hasattr(role_permission_data, "dict"):
        rp_dict = role_permission_data.dict(exclude_unset=True)
    else:
        rp_dict = dict(role_permission_data)
        
    if "RLPR_date_create" not in rp_dict or rp_dict["RLPR_date_create"] is None:
        rp_dict["RLPR_date_create"] = date.today()
    if "RLPR_state" not in rp_dict or rp_dict["RLPR_state"] is None:
        rp_dict["RLPR_state"] = 1
        
    new_rp = RolesPermissions(**rp_dict)
    db.add(new_rp)
    db.commit()
    db.refresh(new_rp)
    return new_rp

def update_role_permission(db: Session, role_permission_id: int, role_permission_data):
    """Actualiza una relación rol-permiso existente."""
    rp = get_role_permission_by_id(db, role_permission_id)
    if not rp:
        return None
        
    if hasattr(role_permission_data, "dict"):
        update_data = role_permission_data.dict(exclude_unset=True)
    else:
        update_data = dict(role_permission_data)
        
    if "RLPR_date_update" not in update_data or update_data["RLPR_date_update"] is None:
        update_data["RLPR_date_update"] = date.today()
        
    for key, value in update_data.items():
        setattr(rp, key, value)
        
    db.commit()
    db.refresh(rp)
    return rp

def delete_role_permission(db: Session, role_permission_id: int):
    """Elimina permanentemente una relación rol-permiso."""
    rp = get_role_permission_by_id(db, role_permission_id)
    if not rp:
        return None
        
    db.delete(rp)
    db.commit()
    return rp

def deactivate_role_permission(db: Session, role_permission_id: int):
    """Inactiva una relación rol-permiso (soft delete)."""
    rp = get_role_permission_by_id(db, role_permission_id)
    if not rp:
        return None
        
    rp.RLPR_state = 0
    rp.RLPR_date_update = date.today()
    db.commit()
    db.refresh(rp)
    return rp

def activate_role_permission(db: Session, role_permission_id: int):
    """Activa una relación rol-permiso inactivada."""
    rp = get_role_permission_by_id(db, role_permission_id)
    if not rp:
        return None
        
    rp.RLPR_state = 1
    rp.RLPR_date_update = date.today()
    db.commit()
    db.refresh(rp)
    return rp
