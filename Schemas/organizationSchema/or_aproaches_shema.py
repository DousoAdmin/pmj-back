from pydantic import BaseModel
from datetime import date 


class AorpachesOrganizationCreate(BaseModel):
    APCH_name : str
    APCH_description : str


class AproachesOrganizationUpdate(BaseModel):
    APCH_name : str
    APCH_description : str


class AproacheOrganizationOut(BaseModel):
    APCH_PK: int


class AproachesOrganizationResponse(BaseModel):
    APCH_PK : int
    APCH_name : str
    APCH_description : str
    class Config:
        orm_mode = True


class TokeResponse(BaseModel):
    acces_Token : str
    token_type : str
    user : AproachesOrganizationResponse
