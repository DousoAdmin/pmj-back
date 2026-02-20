from pydantic import BaseModel
from datetime import date


class OrganizationObsarvationCreate(BaseModel):
    OROB_FK_document : int
    OROB_comment : str
    OROB_status : str


class OrganizationObservationUpdate(BaseModel):
    OROB_FK_document : int
    OROB_comment : str
    OROB_status : str


class OrganizationObservationResponse(BaseModel):
    OROB_PK : int
    OROB_FK_document : int
    OROB_comment : str
    class Config:
        orm_mode = True


class OrganizationObservationOut(BaseModel):
    OROB_PK : int

    
class TokeResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationObservationResponse




