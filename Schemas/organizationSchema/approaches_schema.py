from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ApproachCreate(BaseModel):
    APCH_name: str = Field(..., min_length=1, max_length=100)
    APCH_description: str = Field(..., min_length=1, max_length=100)
    APCH_date_create: Optional[date] = None

class ApproachUpdate(BaseModel):
    APCH_name: Optional[str] = Field(None, min_length=1, max_length=100)
    APCH_description: Optional[str] = Field(None, min_length=1, max_length=100)
    APCH_date_create: Optional[date] = None

class ApproachResponse(BaseModel):
    APCH_PK: int
    APCH_name: str
    APCH_description: str
    APCH_date_create: Optional[date]
    
    class Config:
        from_attributes = True
