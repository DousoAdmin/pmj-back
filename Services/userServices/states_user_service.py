from sqlalchemy.orm import Session
from Models.users.statesuserModel import StatesUser
from datetime import date
from typing import Optional

def get_all_states_users(db: Session):
    """Obtiene todos los estados de usuario."""
    return db.query(StatesUser).all()

def get_state_user_by_id(db: Session, state_user_id: int):
    """Obtiene un estado de usuario por su ID."""
    return db.query(StatesUser).filter(StatesUser.STTS_PK == state_user_id).first()

def get_state_user_by_name(db: Session, name: str):
    """Obtiene un estado de usuario por su nombre."""
    return db.query(StatesUser).filter(StatesUser.STTS_name == name).first()

def create_state_user(db: Session, state_user_data):
    """Crea un nuevo estado de usuario."""
    if hasattr(state_user_data, "dict"):
        su_dict = state_user_data.dict(exclude_unset=True)
    else:
        su_dict = dict(state_user_data)
        
    if "STTS_date_create" not in su_dict or su_dict["STTS_date_create"] is None:
        su_dict["STTS_date_create"] = date.today()
        
    new_state = StatesUser(**su_dict)
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state

def update_state_user(db: Session, state_user_id: int, state_user_data):
    """Actualiza un estado de usuario existente."""
    state_user = get_state_user_by_id(db, state_user_id)
    if not state_user:
        return None
        
    if hasattr(state_user_data, "dict"):
        update_data = state_user_data.dict(exclude_unset=True)
    else:
        update_data = dict(state_user_data)
        
    for key, value in update_data.items():
        setattr(state_user, key, value)
        
    db.commit()
    db.refresh(state_user)
    return state_user

def delete_state_user(db: Session, state_user_id: int):
    """Elimina permanentemente un estado de usuario."""
    state_user = get_state_user_by_id(db, state_user_id)
    if not state_user:
        return None
        
    db.delete(state_user)
    db.commit()
    return state_user
