from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, inspect
from Models.persons.personsModel import Persons
from typing import Optional, List

def _has_state_column():
    """Verifica si el modelo tiene el campo PRSN_state."""
    return hasattr(Persons, 'PRSN_state')

def get_all_persons(db: Session, include_inactive: bool = False):
    """Obtiene todas las personas. Por defecto solo las activas."""
    query = db.query(Persons)
    if not include_inactive and _has_state_column():
        # Filtrar solo personas activas (PRSN_state = 1) si el campo existe
        query = query.filter(Persons.PRSN_state == 1)
    return query.all()

def get_person_by_id(db: Session, person_id: int):
    """Obtiene una persona por su ID."""
    return db.query(Persons).filter(Persons.PRSN_PK == person_id).first()

def get_person_by_identification(db: Session, identification: str):
    """Busca una persona por número de identificación."""
    return db.query(Persons).filter(Persons.PRSN_identification == identification).first()

def get_person_by_email(db: Session, email: str):
    """Busca una persona por email."""
    return db.query(Persons).filter(Persons.PRSN_email == email).first()

def search_persons(
    db: Session,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    identification: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    include_inactive: bool = False
):
    """Busca personas por múltiples criterios. Por defecto solo busca personas activas."""
    query = db.query(Persons)
    
    # Por defecto solo buscar personas activas si el campo existe
    if not include_inactive and _has_state_column():
        query = query.filter(Persons.PRSN_state == 1)
    
    filters = []
    if name:
        filters.append(Persons.PRSN_name.ilike(f"%{name}%"))
    if lastname:
        filters.append(Persons.PRSN_lastname.ilike(f"%{lastname}%"))
    if identification:
        filters.append(Persons.PRSN_identification.ilike(f"%{identification}%"))
    if email:
        filters.append(Persons.PRSN_email.ilike(f"%{email}%"))
    if phone:
        filters.append(Persons.PRSN_phone.ilike(f"%{phone}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_person(db: Session, person_data):
    """Crea una nueva persona."""
    # Verificar si ya existe una persona con el mismo email, teléfono o identificación
    existing_email = get_person_by_email(db, person_data.PRSN_email)
    if existing_email:
        raise ValueError("Ya existe una persona con este email")
    
    existing_identification = get_person_by_identification(db, person_data.PRSN_identification)
    if existing_identification:
        raise ValueError("Ya existe una persona con este número de identificación")
    
    existing_phone = db.query(Persons).filter(Persons.PRSN_phone == person_data.PRSN_phone).first()
    if existing_phone:
        raise ValueError("Ya existe una persona con este teléfono")
    
    # Crear el diccionario excluyendo PRSN_state si no existe en el modelo
    person_dict = person_data.dict(exclude={'PRSN_state'} if not _has_state_column() else set())
    
    # Convertir valores 0 en claves foráneas a None (NULL) para evitar errores de foreign key
    foreign_key_fields = ['PRSN_FK_ethnicity', 'PRSN_FK_disability', 'PRSN_FK_gender', 'PRSN_FK_sexualidentity']
    for field in foreign_key_fields:
        if field in person_dict and person_dict[field] == 0:
            person_dict[field] = None
    
    new_person = Persons(**person_dict)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

def update_person(db: Session, person_id: int, person_data):
    """Actualiza una persona existente."""
    person = get_person_by_id(db, person_id)
    if not person:
        return None
    
    update_data = person_data.dict(exclude_unset=True)
    
    # Convertir valores 0 en claves foráneas a None (NULL) para evitar errores de foreign key
    foreign_key_fields = ['PRSN_FK_ethnicity', 'PRSN_FK_disability', 'PRSN_FK_gender', 'PRSN_FK_sexualidentity']
    for field in foreign_key_fields:
        if field in update_data and update_data[field] == 0:
            update_data[field] = None
    
    # Verificar duplicados solo si se están actualizando estos campos
    if 'PRSN_email' in update_data and update_data['PRSN_email'] != person.PRSN_email:
        existing = get_person_by_email(db, update_data['PRSN_email'])
        if existing and existing.PRSN_PK != person_id:
            raise ValueError("Ya existe una persona con este email")
    
    if 'PRSN_identification' in update_data and update_data['PRSN_identification'] != person.PRSN_identification:
        existing = get_person_by_identification(db, update_data['PRSN_identification'])
        if existing and existing.PRSN_PK != person_id:
            raise ValueError("Ya existe una persona con este número de identificación")
    
    if 'PRSN_phone' in update_data and update_data['PRSN_phone'] != person.PRSN_phone:
        existing = db.query(Persons).filter(Persons.PRSN_phone == update_data['PRSN_phone']).first()
        if existing and existing.PRSN_PK != person_id:
            raise ValueError("Ya existe una persona con este teléfono")
    
    for key, value in update_data.items():
        setattr(person, key, value)
    
    db.commit()
    db.refresh(person)
    return person

def delete_person(db: Session, person_id: int):
    """Elimina permanentemente una persona de la base de datos."""
    person = get_person_by_id(db, person_id)
    if not person:
        return None
    
    db.delete(person)
    db.commit()
    return person

def deactivate_person(db: Session, person_id: int):
    """Inactiva una persona (soft delete usando campo de estado)."""
    person = get_person_by_id(db, person_id)
    if not person:
        return None
    
    if not _has_state_column():
        raise ValueError("El campo PRSN_state no existe en la base de datos. Por favor, crea una migración para agregar esta columna.")
    
    person.PRSN_state = 0  # 0 = inactivo, 1 = activo
    db.commit()
    db.refresh(person)
    return person

def activate_person(db: Session, person_id: int):
    """Activa una persona previamente inactivada."""
    person = get_person_by_id(db, person_id)
    if not person:
        return None
    
    if not _has_state_column():
        raise ValueError("El campo PRSN_state no existe en la base de datos. Por favor, crea una migración para agregar esta columna.")
    
    person.PRSN_state = 1  # 1 = activo
    db.commit()
    db.refresh(person)
    return person