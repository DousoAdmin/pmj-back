from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class OrganizationTypeCreate(BaseModel):
    ORTP_name: str = Field(..., min_length=1, max_length=100)
    ORTP_description: str = Field(..., min_length=1, max_length=100)
    ORTP_date_create: Optional[date] = None

class OrganizationTypeUpdate(BaseModel):
    ORTP_name: Optional[str] = Field(None, min_length=1, max_length=100)
    ORTP_description: Optional[str] = Field(None, min_length=1, max_length=100)
    ORTP_date_create: Optional[date] = None

class OrganizationTypeResponse(BaseModel):
    ORTP_PK: int
    ORTP_name: str
    ORTP_description: str
    ORTP_date_create: Optional[date]
    
    class Config:
        from_attributes = True
