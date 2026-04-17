from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class TypeDocumentsPersonsCreate(BaseModel):
    TPDU_name: str = Field(..., min_length=1, max_length=50)
    TPDU_code: str = Field(..., min_length=1, max_length=10)
    TPDU_description: Optional[str] = None
    TPDU_date_create: Optional[date] = None
    TPDU_user_create: Optional[int] = None


class TypeDocumentsPersonsUpdate(BaseModel):
    TPDU_name: Optional[str] = Field(None, min_length=1, max_length=50)
    TPDU_code: Optional[str] = Field(None, min_length=1, max_length=10)
    TPDU_description: Optional[str] = None
    TPDU_date_create: Optional[date] = None
    TPDU_user_create: Optional[int] = None


class TypeDocumentsPersonsResponse(BaseModel):
    TPDU_PK: int
    TPDU_name: str
    TPDU_code: str
    TPDU_description: Optional[str]
    TPDU_date_create: Optional[date]
    TPDU_user_create: Optional[int]

    class Config:
        from_attributes = True
