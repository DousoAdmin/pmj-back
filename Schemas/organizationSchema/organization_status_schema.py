from pydantic import BaseModel
from datetime import date


class OrganizationStatusCreate(BaseModel):
    ORST_name: str
    ORST_description: str
    ORST_date_create: date = None


class OrganizationStatusUpdate(BaseModel):
    ORST_name: str = None
    ORST_description: str = None
    ORST_date_create: date = None


class OrganizationStatusResponse(BaseModel):
    ORST_PK: int
    ORST_name: str
    ORST_description: str
    ORST_date_create: date = None
    class Config:
        orm_mode = True


class OrganizationStatusOut(BaseModel):
    ORST_PK: int
    ORST_name: str
    ORST_description: str
    ORST_date_create: date = None

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: OrganizationStatusResponse