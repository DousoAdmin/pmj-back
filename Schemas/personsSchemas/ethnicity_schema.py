from pydantic import BaseModel, Field
from typing import Optional

class EthnicityCreate(BaseModel):
    ETNC_name: str = Field(..., min_length=1, max_length=45)
    ETNC_description: Optional[str] = Field(None, max_length=155)
    ETNC_state: Optional[bytes] = None

class EthnicityUpdate(BaseModel):
    ETNC_name: Optional[str] = Field(None, min_length=1, max_length=45)
    ETNC_description: Optional[str] = Field(None, max_length=155)
    ETNC_state: Optional[bytes] = None

class EthnicityResponse(BaseModel):
    ETNC_PK: int
    ETNC_name: str
    ETNC_description: Optional[str]
    ETNC_state: Optional[bytes]
    
    class Config:
        from_attributes = True
