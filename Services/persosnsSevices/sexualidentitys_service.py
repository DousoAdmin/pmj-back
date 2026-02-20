from sqlalchemy.orm import Session
from sqlalchemy import or_
from Models.persons.sexualidentitysModel import Sexualidentitys
from typing import Optional

def get_all_sexualidentitys(db: Session):
    """Obtiene todas las identidades sexuales."""
    return db.query(Sexualidentitys).all()

def get_sexualidentity_by_id(db: Session, sexualidentity_id: int):
    """Obtiene una identidad sexual por su ID."""
    return db.query(Sexualidentitys).filter(Sexualidentitys.SXID_PK == sexualidentity_id).first()

def search_sexualidentitys(
    db: Session,
    name: Optional[str] = None
):
    """Busca identidades sexuales por múltiples criterios."""
    query = db.query(Sexualidentitys)
    
    filters = []
    if name:
        filters.append(Sexualidentitys.SXID_name.ilike(f"%{name}%"))
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.all()

def create_sexualidentity(db: Session, sexualidentity_data):
    """Crea una nueva identidad sexual."""
    sexualidentity_dict = sexualidentity_data.dict(exclude_unset=True)
    new_sexualidentity = Sexualidentitys(**sexualidentity_dict)
    db.add(new_sexualidentity)
    db.commit()
    db.refresh(new_sexualidentity)
    return new_sexualidentity

def update_sexualidentity(db: Session, sexualidentity_id: int, sexualidentity_data):
    """Actualiza una identidad sexual existente."""
    sexualidentity = get_sexualidentity_by_id(db, sexualidentity_id)
    if not sexualidentity:
        return None
    
    update_data = sexualidentity_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(sexualidentity, key, value)
    
    db.commit()
    db.refresh(sexualidentity)
    return sexualidentity

def delete_sexualidentity(db: Session, sexualidentity_id: int):
    """Elimina permanentemente una identidad sexual de la base de datos."""
    sexualidentity = get_sexualidentity_by_id(db, sexualidentity_id)
    if not sexualidentity:
        return None
    
    db.delete(sexualidentity)
    db.commit()
    return sexualidentity
