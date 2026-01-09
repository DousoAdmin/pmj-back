from sqlalchemy.future import select
from sqlalchemy.orm import Session
import Models
from Schemas import user_schema


# Obtener todos
def get_users(db: Session):
    result = db.query(Models.users.userModel.User).all()
    return result


# Obtener por ID
def get_user(db: Session, user_id: int):
    return db.get(Models.userModel.users, user_id)


# Crear usuario
def create_user(db: Session, user: user_schema):
    new_user = Models.userModel.users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Actualizar usuario
def update_user(db: Session, user_id: int, data: user_schema):
    db_user = db.get(Models.userModel.users, user_id)
    if not db_user:
        return None

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Eliminar usuario
def delete_user(db: Session, user_id: int):
    db_user = db.get(Models.userModel.users, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
