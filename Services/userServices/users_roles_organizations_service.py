from sqlalchemy.orm import Session
from Models.users.usersRolesOrganizationsModel import UsersRolesOrganizations
from datetime import date
from typing import Optional

def get_all_users_roles_organizations(db: Session, include_inactive: bool = False):
    """Obtiene todas las asignaciones de usuarios, roles y organizaciones. Por defecto solo las activas."""
    query = db.query(UsersRolesOrganizations)
    if not include_inactive:
        query = query.filter(UsersRolesOrganizations.USRL_state == 1)
    return query.all()

def get_user_role_organization_by_id(db: Session, uro_id: int):
    """Obtiene una asignación específica por su ID."""
    return db.query(UsersRolesOrganizations).filter(UsersRolesOrganizations.USRL_PK == uro_id).first()

def get_user_role_organizations_by_user(db: Session, user_id: int, include_inactive: bool = False):
    """Obtiene todas las asignaciones de un usuario específico."""
    query = db.query(UsersRolesOrganizations).filter(UsersRolesOrganizations.USRL_FK_user == user_id)
    if not include_inactive:
        query = query.filter(UsersRolesOrganizations.USRL_state == 1)
    return query.all()

def get_user_role_organizations_by_organization(db: Session, organization_id: int, include_inactive: bool = False):
    """Obtiene todas las asignaciones de una organización específica."""
    query = db.query(UsersRolesOrganizations).filter(UsersRolesOrganizations.USRL_FK_organization == organization_id)
    if not include_inactive:
        query = query.filter(UsersRolesOrganizations.USRL_state == 1)
    return query.all()

def create_user_role_organization(db: Session, uro_data):
    """Crea una nueva asignación de usuario, rol y organización."""
    if hasattr(uro_data, "dict"):
        uro_dict = uro_data.dict(exclude_unset=True)
    else:
        uro_dict = dict(uro_data)
        
    if "USRL_date_create" not in uro_dict or uro_dict["USRL_date_create"] is None:
        uro_dict["USRL_date_create"] = date.today()
    if "USRL_state" not in uro_dict or uro_dict["USRL_state"] is None:
        uro_dict["USRL_state"] = 1
        
    new_uro = UsersRolesOrganizations(**uro_dict)
    db.add(new_uro)
    db.commit()
    db.refresh(new_uro)
    return new_uro

def update_user_role_organization(db: Session, uro_id: int, uro_data):
    """Actualiza una asignación de usuario, rol y organización existente."""
    uro = get_user_role_organization_by_id(db, uro_id)
    if not uro:
        return None
        
    if hasattr(uro_data, "dict"):
        update_data = uro_data.dict(exclude_unset=True)
    else:
        update_data = dict(uro_data)
        
    if "USRL_date_update" not in update_data or update_data["USRL_date_update"] is None:
        update_data["USRL_date_update"] = date.today()
        
    for key, value in update_data.items():
        setattr(uro, key, value)
        
    db.commit()
    db.refresh(uro)
    return uro

def delete_user_role_organization(db: Session, uro_id: int):
    """Elimina permanentemente una asignación de usuario, rol y organización."""
    uro = get_user_role_organization_by_id(db, uro_id)
    if not uro:
        return None
        
    db.delete(uro)
    db.commit()
    return uro

def deactivate_user_role_organization(db: Session, uro_id: int):
    """Inactiva una asignación de usuario, rol y organización (soft delete)."""
    uro = get_user_role_organization_by_id(db, uro_id)
    if not uro:
        return None
        
    uro.USRL_state = 0
    uro.USRL_date_update = date.today()
    db.commit()
    db.refresh(uro)
    return uro

def activate_user_role_organization(db: Session, uro_id: int):
    """Activa una asignación de usuario, rol y organización inactivada."""
    uro = get_user_role_organization_by_id(db, uro_id)
    if not uro:
        return None
        
    uro.USRL_state = 1
    uro.USRL_date_update = date.today()
    db.commit()
    db.refresh(uro)
    return uro
