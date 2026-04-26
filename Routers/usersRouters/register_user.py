from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from Models.persons.personsModel import Persons
from Schemas.userShemas.user_schema import UserRegister
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Config.database import get_db
from Services.persosnsSevices import persons_service




router = APIRouter(prefix="/users", tags=["user"])
@router.post("/Create_User", response_model=UserRegister)
def registrar_usuario(user: UserRegister,  db: Session = Depends(get_db)):
    try:
        #Se transforma la inf 
        # MAPEO EXACTO SEGÚN TU EXCEL
        class PersonData:
            """Clase simple para mapear datos transformados"""
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
            def dict(self, exclude=None):
                """Retorna un diccionario de los atributos"""
                result = self.__dict__.copy()
                if exclude:
                    for key in exclude:
                        result.pop(key, None)
                return result
        
        db_data_dict = {
            "PRSN_name": user.FULL_NAME,
            "PRSN_identification": user.IDENTIFICATION,
            "PRSN_FK_typedocumentspersons": user.TYPE_DOCUMENT,
            "PRSN_brithday": user.BIRTHDAY,
            "PRSN_email": user.EMAIL,
            "PRSN_phone": user.PHONE,
            "PRSN_location": user.LOCATION,
            "PRSN_FK_ethnicity": user.ETNIA,
            "PRSN_FK_disability": user.DISCAPACIDAD,
            "PRSN_FK_gender": user.GENERO,
            "PRSN_FK_sexualidentity": user.IDENTIDAD_SEXUAL
        }
        
        # Convertir el diccionario a un objeto con atributos
        db_data = PersonData(**db_data_dict)
        
        new_user = persons_service.create_person(db, db_data)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Transformación correcta (BACK → DB)",
                "input": user.dict(),
                "transformado": db_data_dict,
                "user_id": new_user.PRSN_PK if hasattr(new_user, 'PRSN_PK') else None
            }
        )

    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "error": "Validación",
                "detail": str(ve)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "error": "Error interno",
                "detail": str(e)
            }
        )