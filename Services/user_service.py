from sqlalchemy.orm import Session
import Models, Schemas

def get_all_users(db: Session):
    return db.query(Models.user_model.User).all()
