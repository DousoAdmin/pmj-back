from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Schemas import user_schema
from Config.database import get_db
from Services import auth_service
from Core import security

router = APIRouter(prefix="/satatesPersons", tags=["satatesPersons"])

@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return new_user

    


