from pydantic import BaseModel
from datetime import date


class OrganizationAproachesCreate(BaseModel):
    ORAP_user_create : str
    ORAP_FK_organization : int
    ORAP_FK_approach : int


class OrganizatioAprochesUpdate(BaseModel):
    ORAP_user_create : str
    ORAP_FK_organization : int
    ORAP_FK_approach : int


class OrganizationAproachesResponse(BaseModel):
    ORAP_PK : int
    ORAP_user_create : str
    ORAP_FK_organization : int
    ORAP_FK_approach : int
    class Config:
        orm_mode = True


class OrganizatioAproachesOut(BaseModel):
    ORAP_PK : int

class TokeResponse(BaseModel):
    acces_Token : str
    token_type : str
    user : OrganizationAproachesResponse