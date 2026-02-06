from pydantic import BaseModel, Field
from typing import Optional

class ProgramCreate(BaseModel):
    PRGM_name: str = Field(..., min_length=1, max_length=45)
    PRGM_description: Optional[str] = Field(None, max_length=255)
    PRGM_state: Optional[int] = None

class ProgramUpdate(BaseModel):
    PRGM_name: Optional[str] = Field(None, min_length=1, max_length=45)
    PRGM_description: Optional[str] = Field(None, max_length=255)
    PRGM_state: Optional[int] = None

class ProgramResponse(BaseModel):
    PRGM_PK: int
    PRGM_name: str
    PRGM_description: Optional[str]
    PRGM_state: Optional[int]
    
    class Config:
        from_attributes = True
