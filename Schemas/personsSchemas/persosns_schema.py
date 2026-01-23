from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional

class PersonCreate(BaseModel):
    PRSN_name: str = Field(..., min_length=1, max_length=100)
    PRSN_lastname: str = Field(..., min_length=1, max_length=100)
    PRSN_phone: str = Field(..., min_length=1, max_length=45)
    PRSN_email: EmailStr = Field(..., max_length=100)
    PRSN_brithday: date
    PRSN_identification: str = Field(..., min_length=1, max_length=45)
    PRSN_location: str = Field(..., min_length=1, max_length=255)
    PRSN_FK_ethnicity: Optional[int] = Field(None, description="ID de etnia (debe ser mayor a 0 o None)")
    PRSN_FK_disability: Optional[int] = Field(None, description="ID de discapacidad (debe ser mayor a 0 o None)")
    PRSN_FK_gender: Optional[int] = Field(None, description="ID de género (debe ser mayor a 0 o None)")
    PRSN_FK_sexualidentity: Optional[int] = Field(None, description="ID de identidad sexual (debe ser mayor a 0 o None)")
    
    @field_validator('PRSN_FK_ethnicity', 'PRSN_FK_disability', 'PRSN_FK_gender', 'PRSN_FK_sexualidentity', mode='before')
    @classmethod
    def convert_zero_to_none_and_validate(cls, v):
        """Convierte 0 a None y valida que si hay valor, sea mayor a 0."""
        if v is None:
            return None
        if v == 0:
            return None
        if v < 1:
            raise ValueError("El ID debe ser mayor a 0 o None")
        return v

class PersonUpdate(BaseModel):
    PRSN_name: Optional[str] = Field(None, min_length=1, max_length=100)
    PRSN_lastname: Optional[str] = Field(None, min_length=1, max_length=100)
    PRSN_phone: Optional[str] = Field(None, min_length=1, max_length=45)
    PRSN_email: Optional[EmailStr] = Field(None, max_length=100)
    PRSN_brithday: Optional[date] = None
    PRSN_identification: Optional[str] = Field(None, min_length=1, max_length=45)
    PRSN_location: Optional[str] = Field(None, min_length=1, max_length=255)
    PRSN_FK_ethnicity: Optional[int] = Field(None, description="ID de etnia (debe ser mayor a 0 o None)")
    PRSN_FK_disability: Optional[int] = Field(None, description="ID de discapacidad (debe ser mayor a 0 o None)")
    PRSN_FK_gender: Optional[int] = Field(None, description="ID de género (debe ser mayor a 0 o None)")
    PRSN_FK_sexualidentity: Optional[int] = Field(None, description="ID de identidad sexual (debe ser mayor a 0 o None)")
    
    @field_validator('PRSN_FK_ethnicity', 'PRSN_FK_disability', 'PRSN_FK_gender', 'PRSN_FK_sexualidentity', mode='before')
    @classmethod
    def convert_zero_to_none_and_validate(cls, v):
        """Convierte 0 a None y valida que si hay valor, sea mayor a 0."""
        if v is None:
            return None
        if v == 0:
            return None
        if v < 1:
            raise ValueError("El ID debe ser mayor a 0 o None")
        return v

class personsResponse(BaseModel):
    PRSN_PK: int
    PRSN_name: str
    PRSN_lastname: str
    PRSN_phone: str
    PRSN_email: EmailStr
    PRSN_brithday: date
    PRSN_identification: str
    PRSN_location: str
    # PRSN_state se agregará cuando se cree la migración de base de datos
    # PRSN_state: Optional[int] = None  # 1 = activo, 0 = inactivo
    PRSN_FK_ethnicity: Optional[int]
    PRSN_FK_disability: Optional[int]
    PRSN_FK_gender: Optional[int]
    PRSN_FK_sexualidentity: Optional[int]
    
    class Config:
        from_attributes = True
 