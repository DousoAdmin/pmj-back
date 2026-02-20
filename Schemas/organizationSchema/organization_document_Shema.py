from pydantic import BaseModel
from datetime import date


class OrganizationDocumentCreate(BaseModel):
    ORDC_FK_organization : int
    ORDC_FK_document_type : int
    ORDC_original_name : str
    ORDC_observation : str
    ORDC_state : str


class OrganizationDocumentResponse(BaseModel):
    ORDC_PK : int
    ORDC_FK_organization : int
    ORDC_observation : str
    ORDC_user_create : date
    class Config:
        orm_mode = True


class OrganizationDocumentUpdate(BaseModel):
    ORDC_FK_organization : int
    ORDC_FK_document_type : int
    ORDC_original_name : str
    ORDC_observation : str
    ORDC_state : str


class OrganizationDocumentOut(BaseModel):
    ORDC_PK : int


class TokenResponse(BaseModel):
    access_token : str
    token_type: str
    user: OrganizationDocumentResponse









