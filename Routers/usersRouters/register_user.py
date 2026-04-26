from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from Models.persons.personsModel import Persons
from Schemas.userShemas.user_schema import UserRegister, UserCreate
from Services.userServices import user_service
from Services.auth_service import register_user
from Schemas.personsSchemas.persosns_schema import PersonCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Config.database import get_db
from Services.persosnsSevices import persons_service


router = APIRouter(prefix="/users", tags=["user"])

@router.post("/Create_User", response_model=UserRegister)
def registrar_usuario(user: UserRegister, db: Session = Depends(get_db)):
    try:
        db_data_dict = PersonCreate(
            PRSN_name=user.FULL_NAME,
            PRSN_identification=user.IDENTIFICATION,
            PRSN_FK_typedocumentspersons=user.TYPE_DOCUMENT,
            PRSN_brithday=user.BIRTHDAY,
            PRSN_email=user.EMAIL,
            PRSN_phone=user.PHONE,
            PRSN_location=user.LOCATION,
            PRSN_FK_ethnicity=user.ETNIA,
            PRSN_FK_disability=user.DISCAPACIDAD,
            PRSN_FK_gender=user.GENERO,
            PRSN_FK_sexualidentity=user.IDENTIDAD_SEXUAL
        ) # Convertir a diccionario para pasar al servicio
        
        # Pasar el diccionario al servicio, no el objeto Persons
        new_person = persons_service.create_person(db, db_data_dict)

        data_user = UserCreate(
            USER_FK_user_create= 1,  # Aquí puedes asignar el ID del usuario que crea, si lo tienes
            USER_FK_user_update=1,  # Aquí puedes asignar el ID del usuario que actualiza, si lo tienes
            USER_username=user.EMAIL,  # Usar el email como username
            USER_password="Colombia2026*",  # Aquí deberías hashear la contraseña real
            USER_FK_state_user=1,  # Asumiendo que 1 es el estado activo
            USER_reset_password=0,  # Asumiendo que no se requiere reset de contraseña
            USER_address_ip="127.0.0.1"
        )
        
        new_user = register_user(db, data_user)
      
                
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Transformación correcta (BACK → DB)",
                "person_id": new_person.PRSN_PK if hasattr(new_person, 'PRSN_PK') else None,
                "user_id": new_user.USER_PK if hasattr(new_user, 'USER_PK') else None
            }
        )

    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={"status": 400, "error": "Validación", "detail": str(ve)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "error": "Error interno", "detail": str(e)}
        )