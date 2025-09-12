from sqlalchemy.orm import Session
import Models, Schemas
from Core import security

def register_user(user: Schemas.user_schema.UserCreate, db: Session):
    db_user = db.query(Models.user_model.User).filter(
        Models.user_model.User.username == user.username
    ).first()
    if db_user:
        return None

    hashed_password = security.hash_password(user.password)
    new_user = Models.user_model.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Models.user_model.User).filter(
        Models.user_model.User.username == username
    ).first()
    if not user or not security.verify_password(password, user.password):
        return None
    return user

