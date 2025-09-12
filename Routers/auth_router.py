from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Schemas import user_schema
from Config.database import get_db
from Services import auth_service
from Core import security

router = APIRouter()
@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return new_user

@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    auth_user = auth_service.authenticate_user(user.username, user.password, db)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    token = security.create_access_token({"sub": auth_user.username})
    return {"access_token": token, "token_type": "bearer"}