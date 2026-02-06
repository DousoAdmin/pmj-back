from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class OrganizationDocumentTypeCreate(BaseModel):
    ODPT_name: str = Field(..., min_length=1, max_length=100)
    ODPT_description: str = Field(..., min_length=1, max_length=100)
    ODPT_date_create: Optional[date] = None
    ODPT_user_create: Optional[date] = None
    ODPT_user_update: Optional[date] = None

class OrganizationDocumentTypeUpdate(BaseModel):
    ODPT_name: Optional[str] = Field(None, min_length=1, max_length=100)
    ODPT_description: Optional[str] = Field(None, min_length=1, max_length=100)
    ODPT_date_create: Optional[date] = None
    ODPT_user_create: Optional[date] = None
    ODPT_user_update: Optional[date] = None

class OrganizationDocumentTypeResponse(BaseModel):
    ODPT_PK: int
    ODPT_name: str
    ODPT_description: str
    ODPT_date_create: Optional[date]
    ODPT_user_create: Optional[date]
    ODPT_user_update: Optional[date]
    
    class Config:
        from_attributes = True
