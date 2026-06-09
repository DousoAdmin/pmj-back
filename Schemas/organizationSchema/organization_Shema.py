from typing import Optional
from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    ORGZ_name : str
    ORGZ_descriptions : str
    ORGZ_nit : str
    ORGZ_create_date : str
    ORGZ_FK_status : int
    ORGZ_FK_type : int


class OrganizationResponse(BaseModel):
    ORGZ_PK: int
    ORGZ_name: str
    class Config:
        from_attributes = True


#Update
class OrganizationUpdate(BaseModel):
    ORGZ_name : str 
    ORGZ_descriptions : str 
    ORGZ_nit : str 
    ORGZ_create_date : str 
    ORGZ_FK_status : int 
    ORGZ_FK_type : int 


class OrganizationOut(BaseModel):
    ORGZ_PK: int
    ORGZ_name: str
    ORGZ_descriptions: str
    ORGZ_FK_type: int | None = None

    class Config:
        orm_mode = True


class OrganizationSimple(BaseModel):
    id_organizacion: int
    nombre: str
    descripcion: Optional[str] = None
    nit: Optional[str] = None
    fecha_creacion: Optional[str] = None
    id_estado: Optional[int] = None
    nombre_estado: Optional[str] = None
    id_tipo: Optional[int] = None
    nombre_tipo: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationResponse  # Incluir datos del usuario para mostrar en UI