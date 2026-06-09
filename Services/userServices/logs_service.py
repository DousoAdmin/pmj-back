from sqlalchemy.orm import Session
from Models.users.logsModel import Logs
from datetime import datetime
from typing import Optional

def get_all_logs(db: Session, limit: int = 100, offset: int = 0):
    """Obtiene todos los registros de log."""
    return db.query(Logs).order_by(Logs.LOGS_timestamp.desc()).offset(offset).limit(limit).all()

def get_log_by_id(db: Session, log_id: int):
    """Obtiene un registro de log por su ID."""
    return db.query(Logs).filter(Logs.LOGS_PK == log_id).first()

def get_logs_by_user(db: Session, user_id: int, limit: int = 100, offset: int = 0):
    """Obtiene los registros de log de un usuario específico."""
    return db.query(Logs).filter(Logs.LOGS_user_FK == user_id).order_by(Logs.LOGS_timestamp.desc()).offset(offset).limit(limit).all()

def create_log(db: Session, log_data):
    """Crea un nuevo registro de log."""
    if hasattr(log_data, "dict"):
        log_dict = log_data.dict(exclude_unset=True)
    else:
        log_dict = dict(log_data)
        
    if "LOGS_timestamp" not in log_dict or log_dict["LOGS_timestamp"] is None:
        log_dict["LOGS_timestamp"] = datetime.utcnow()
        
    new_log = Logs(**log_dict)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def update_log(db: Session, log_id: int, log_data):
    """Actualiza un registro de log existente."""
    log = get_log_by_id(db, log_id)
    if not log:
        return None
        
    if hasattr(log_data, "dict"):
        update_data = log_data.dict(exclude_unset=True)
    else:
        update_data = dict(log_data)
        
    for key, value in update_data.items():
        setattr(log, key, value)
        
    db.commit()
    db.refresh(log)
    return log

def delete_log(db: Session, log_id: int):
    """Elimina permanentemente un registro de log."""
    log = get_log_by_id(db, log_id)
    if not log:
        return None
        
    db.delete(log)
    db.commit()
    return log
