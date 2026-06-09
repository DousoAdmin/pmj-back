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

# Importar modelos y servicios necesarios para la relación de roles y organizaciones
from Models.users.rolesModel import Roles
from Models.organizations.organizations_model import Organizations
from Services.userServices.users_roles_organizations_service import create_user_role_organization
from Services.persosnsSevices.userpersonal_service import create_user_persona


router = APIRouter(prefix="/users", tags=["user"])

@router.post("/Create_User", response_model=UserRegister)
def registrar_usuario(user: UserRegister, db: Session = Depends(get_db)):
    try:
       
        db_data_dict = PersonCreate(
            PRSN_name=user.full_name,
            PRSN_identification=user.identification,
            PRSN_FK_typedocumentspersons=user.type_document,
            PRSN_brithday=user.birthday,
            PRSN_email=user.email,
            PRSN_phone=user.phone,
            PRSN_location=user.location,
            PRSN_FK_ethnicity=user.etnia,
            PRSN_FK_disability=user.discapacidad,
            PRSN_FK_gender=user.genero,
            PRSN_FK_sexualidentity=user.identidad_sexual
        ) # Convertir a diccionario para pasar al servicio
        
        # Pasar el diccionario al servicio, no el objeto Persons
        new_person = persons_service.create_person(db, db_data_dict)
        if not new_person:
            return JSONResponse(
                status_code=500,
                content={
                    "status": 500,
                    "message": "No se pudo crear la persona",
                    "person_id": None,
                    "user_id": None
                }
            )
        else:
            data_user = UserCreate(
                USER_FK_user_create= 1,  # Aquí puedes asignar el ID del usuario que crea, si lo tienes
                USER_FK_user_update=1,  # Aquí puedes asignar el ID del usuario que actualiza, si lo tienes
                USER_username=user.email,  # Usar el email como username
                USER_password=user.password,  # Aquí deberías hashear la contraseña real
                USER_FK_state_user=2,  # Asumiendo que 2 es el estado activo
                USER_reset_password=0,  # Asumiendo que no se requiere reset de contraseña
                USER_address_ip="127.0.0.1"
            )
            new_user = register_user(data_user, db)
            if not new_user:
                # Si el usuario no se crea, hacer rollback de la persona creada
                db.rollback()
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": 400,
                        "message": "Ya existe un usuario con este nombre de usuario / email.",
                        "person_id": new_person.PRSN_PK if hasattr(new_person, 'PRSN_PK') else None,
                        "user_id": None
                    }
                )
            else:
                # 2) Crear la relación de usuario, rol 1 y organización 1
                uro_data = {
                    "USRL_FK_rol": 1,
                    "USRL_FK_organization": 1,
                    "USRL_FK_user": new_user.USER_PK,
                    "USRL_user_create": 1,
                    "USRL_user_update": 1,
                    "USRL_state": 1
                }
                create_user_role_organization(db, uro_data)

                # 3) Crear la relación de usuario y persona (UserPersonas)
                up_data = {
                    "USPS_FK_user": new_user.USER_PK,
                    "USPS_FK_person": new_person.PRSN_PK,
                    "USPS_FK_create": 1,
                    "USPS_FK_update": 1,
                    "USPS_state": 1
                }
                create_user_persona(db, up_data)
                
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={
                        "status": 201,
                        "message": "Creacion de usuariode manera correcta",
                        "person_id": new_person.PRSN_PK if hasattr(new_person, 'PRSN_PK') else None,
                        "user_id": new_user.USER_PK if hasattr(new_user, 'USER_PK') else None
                    }
                )

    except ValueError as ve:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"status": 400, "error": "Validación", "detail": str(ve)}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": 500, "error": "Error interno", "detail": str(e)}
        )
