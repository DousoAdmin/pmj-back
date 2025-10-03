from sqlalchemy.orm import Session
import Models, Schemas
from Core import security
from datetime import datetime

def register_user(user: Schemas.user_schema.UserCreate, db: Session):
    db_user = db.query(Models.user_model.User).filter(
        Models.user_model.User.USER_username == user.USER_username
    ).first()
    if db_user:
        return None

    hashed_password = security.hash_password(user.USER_password)
    new_user = Models.user_model.User(
        USER_FK_user_create = user.USER_FK_user_create,
        USER_FK_user_update = user.USER_FK_user_update,
        USER_username = user.USER_username,
        USER_password = hashed_password,
        USER_date_create = datetime.utcnow(),
        USER_date_update = datetime.utcnow(),
        USER_FK_state_user = user.USER_FK_state_user,
        USER_reset_password = user.USER_reset_password,
        USER_address_ip = user.USER_address_ip
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

