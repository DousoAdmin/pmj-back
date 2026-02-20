from pydantic import BaseModel
from datetime import date


class OrganizationTypeCreate(BaseModel):
    ORTP_name : str
    ORTP_description : str
    ORTP_date_create : str


class OrganizationTypeUpdate(BaseModel):
    ORTP_name : str
    ORTP_description : str
    ORTP_date_create : str


class OrganizationTypeResponse(BaseModel):
    ORTP_PK : int
    ORTP_name : str
    ORTP_description : str
    class Config:
        orm_mode = True


class OrganizationTypeOut(BaseModel):
    ORTP_PK = int


class TokeResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationTypeResponse