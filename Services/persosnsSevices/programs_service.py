from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.programsModel import Program
from typing import Optional

def get_all_programs(db: Session, include_inactive: bool = False):
    """Obtiene todos los programas. Por defecto solo los activos."""
    query = db.query(Program)
    if not include_inactive and hasattr(Program, 'PRGM_state'):
        query = query.filter(Program.PRGM_state == 1)
    return query.all()

def get_program_by_id(db: Session, program_id: int):
    """Obtiene un programa por su ID."""
    return db.query(Program).filter(Program.PRGM_PK == program_id).first()

def search_programs(
    db: Session,
    name: Optional[str] = None,
    include_inactive: bool = False
):
    """Busca programas por múltiples criterios."""
    query = db.query(Program)
    
    if not include_inactive and hasattr(Program, 'PRGM_state'):
        query = query.filter(Program.PRGM_state == 1)
    
    filters = []
    if name:
        filters.append(Program.PRGM_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_program(db: Session, program_data):
    """Crea un nuevo programa."""
    program_dict = program_data.dict(exclude_unset=True)
    new_program = Program(**program_dict)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program

def update_program(db: Session, program_id: int, program_data):
    """Actualiza un programa existente."""
    program = get_program_by_id(db, program_id)
    if not program:
        return None
    
    update_data = program_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(program, key, value)
    
    db.commit()
    db.refresh(program)
    return program

def delete_program(db: Session, program_id: int):
    """Elimina permanentemente un programa de la base de datos."""
    program = get_program_by_id(db, program_id)
    if not program:
        return None
    
    db.delete(program)
    db.commit()
    return program

def deactivate_program(db: Session, program_id: int):
    """Inactiva un programa (soft delete usando campo de estado)."""
    program = get_program_by_id(db, program_id)
    if not program:
        return None
    
    if not hasattr(Program, 'PRGM_state'):
        raise ValueError("El campo PRGM_state no existe en la base de datos.")
    
    program.PRGM_state = 0
    db.commit()
    db.refresh(program)
    return program

def activate_program(db: Session, program_id: int):
    """Activa un programa previamente inactivado."""
    program = get_program_by_id(db, program_id)
    if not program:
        return None
    
    if not hasattr(Program, 'PRGM_state'):
        raise ValueError("El campo PRGM_state no existe en la base de datos.")
    
    program.PRGM_state = 1
    db.commit()
    db.refresh(program)
    return program
