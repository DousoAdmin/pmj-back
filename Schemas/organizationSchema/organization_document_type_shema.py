from pydantic import BaseModel
from datetime import date


class OrganizationDocumentTypeCreate(BaseModel):
    ODPT_name : str
    ODPT_description : str
    ODPT_date_create : str
    ODPT_user_create : str


class OrganizationDocumentTypeUpdate(BaseModel):
    ODPT_name : str
    ODPT_description : str
    ODPT_date_create : str
    ODPT_user_create : str


class OrganizationDocumentTypeRespose(BaseModel):
    ODPT_PK : int
    ODPT_name : str
    ODPT_description : str
    class Config:
        orm_mode = True 


class OrganizationDocumentTypeOut(BaseModel):
    ODPT_PK : int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationDocumentTypeRespose

    


