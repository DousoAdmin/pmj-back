from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, EmailStr
from Schemas import user_schema
from Config.database import get_db
from Services import auth_service
from Services.persosnsSevices.userpersonal_service import get_user_personas_by_user
from Services.persosnsSevices import persons_service
from Core import security
from datetime import date
from typing import Optional

class CurrentPersonInfo(BaseModel):
    id_persona: int
    nombre: str
    identificacion: str
    tipo_documento: Optional[int]
    nacimiento: date
    email: EmailStr
    telefono: str
    ubicacion: str
    etnia: Optional[int]
    discapacidad: Optional[int]
    genero: Optional[int]
    identidad_sexual: Optional[int]

    class Config:
        from_attributes = True

class CurrentUserInfoResponse(BaseModel):
    id_usuario: int
    username: str
    person: CurrentPersonInfo

router = APIRouter(prefix="/auth", tags=["authentication"])
@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(user, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503, 
            detail="No se pudo conectar a la base de datos. Revisa DB_USER, DB_PASSWORD y DB_NAME en env/.env.",
        )
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return new_user

@router.post("/login", response_model=user_schema.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa 'username' y 'password' en lugar de 'USER_username' y 'USER_password'
    try:
        auth_user = auth_service.authenticate_user(form_data.username, form_data.password, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a la base de datos. Revisa DB_USER, DB_PASSWORD y DB_NAME en env/.env.",
        )
    if not auth_user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Crear token JWT con los datos del usuario
    access_token = security.create_access_token(data={"sub": auth_user.USER_username})
    
    return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                    "id": auth_user.USER_PK,
                "username": auth_user.USER_username
            }
    }

@router.get("/me", response_model=CurrentUserInfoResponse)
def get_current_user_info(current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    """Endpoint protegido que requiere autenticación para obtener información del usuario actual"""
    try:
        user_personas = get_user_personas_by_user(db, current_user.USER_PK)
        if not user_personas:
            raise HTTPException(status_code=404, detail="No se encontró la relación usuario-persona para el usuario actual")

        person_id = user_personas[0].USPS_FK_person
        person = persons_service.get_person_by_id(db, person_id)
        if not person:
            raise HTTPException(status_code=404, detail="No se encontró la persona asociada al usuario actual")

        return {
            "id_usuario": current_user.USER_PK,
            "username": current_user.USER_username,
            "person": {
                "id_persona": person.PRSN_PK,
                "nombre": person.PRSN_name,
                "identificacion": person.PRSN_identification,
                "tipo_documento": person.PRSN_FK_typedocumentspersons,
                "nacimiento": person.PRSN_brithday,
                "email": person.PRSN_email,
                "telefono": person.PRSN_phone,
                "ubicacion": person.PRSN_location,
                "etnia": person.PRSN_FK_ethnicity,
                "discapacidad": person.PRSN_FK_disability,
                "genero": person.PRSN_FK_gender,
                "identidad_sexual": person.PRSN_FK_sexualidentity
            }
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Error al consultar la base de datos al obtener la información de persona."
        )


