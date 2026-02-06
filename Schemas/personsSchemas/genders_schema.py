from pydantic import BaseModel, Field
from typing import Optional

class GenderCreate(BaseModel):
    GNDR_name: str = Field(..., min_length=1, max_length=45)
    GNDR_description: Optional[str] = Field(None, max_length=155)
    GNDR_state: Optional[int] = None

class GenderUpdate(BaseModel):
    GNDR_name: Optional[str] = Field(None, min_length=1, max_length=45)
    GNDR_description: Optional[str] = Field(None, max_length=155)
    GNDR_state: Optional[int] = None

class GenderResponse(BaseModel):
    GNDR_PK: int
    GNDR_name: str
    GNDR_description: Optional[str]
    GNDR_state: Optional[int]
    
    class Config:
        from_attributes = True
