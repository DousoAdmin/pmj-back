from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Schemas import user_schema
from Config.database import get_db
from Services import auth_service
from Core import security

router = APIRouter(prefix="/auth", tags=["authentication"])
@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return new_user

@router.post("/login", response_model=user_schema.TokenResponse)
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    auth_user = auth_service.authenticate_user(user.USER_username, user.USER_password, db)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Crear token JWT con los datos del usuario
    access_token = security.create_access_token(data={"sub": auth_user.USER_username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "USER_PK": auth_user.USER_PK,
            "USER_username": auth_user.USER_username
        }
    }

@router.get("/me", response_model=user_schema.UserResponse)
def get_current_user_info(current_user = Depends(security.get_current_user)):
    """Endpoint protegido que requiere autenticación para obtener información del usuario actual"""
    return {
        "USER_PK": current_user.USER_PK,
        "USER_username": current_user.USER_username
    }


