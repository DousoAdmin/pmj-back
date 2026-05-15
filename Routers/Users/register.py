from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator

router = APIRouter(prefix="/users", tags=["Userssss"])


class UserRegister(BaseModel):
    FULL_NAME: str = Field(..., min_length=3, max_length=50)
    IDENTIFICATION: str = Field(..., min_length=5, max_length=15)
    TYPE_DOCUMENT: str
    BIRTHDAY: str
    EMAIL: EmailStr
    PHONE: str
    LOCATION: str

    # ❌ No null o vacío
    @field_validator("*")
    def no_vacios(cls, value):
        if value is None or str(value).strip() == "":
            raise ValueError("El campo no puede estar vacío")
        return value

    # 🔢 Documento numérico
    @field_validator("IDENTIFICATION")
    def validar_doc(cls, value):
        if not value.isdigit():
            raise ValueError("El número de documento debe ser numérico")
        return value
    

@router.post("/registro")
def registrar_usuario(user: UserRegister):
    try:
        # MAPEO EXACTO SEGÚN TU EXCEL
        db_data = {
            "PRSN_NAME": user.FULL_NAME,
            "PRSN_IDENTIFICATION": user.IDENTIFICATION,
            "PRSN_TYPE_DOCUMENT": user.TYPE_DOCUMENT,
            "PRSN_BIRTHDAY": user.BIRTHDAY,
            "PRSN_EMAIL": user.EMAIL,
            "PRSN_PHONE": user.PHONE,
            "PRSN_LOCATION": user.LOCATION
        }

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Transformación correcta (BACK → DB)",
                "input": user.dict(),
                "transformado": db_data
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