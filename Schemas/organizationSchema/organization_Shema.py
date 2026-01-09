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
        orm_mode = True 

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationResponse  # Incluir datos del usuario para mostrar en UI