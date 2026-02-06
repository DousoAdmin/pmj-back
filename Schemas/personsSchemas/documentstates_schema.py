from pydantic import BaseModel, Field
from typing import Optional

class DocumentStateCreate(BaseModel):
    DCST_name: str = Field(..., min_length=1, max_length=45)
    DCST_description: Optional[str] = Field(None, max_length=155)

class DocumentStateUpdate(BaseModel):
    DCST_name: Optional[str] = Field(None, min_length=1, max_length=45)
    DCST_description: Optional[str] = Field(None, max_length=155)

class DocumentStateResponse(BaseModel):
    DCST_PK: int
    DCST_name: str
    DCST_description: Optional[str]
    
    class Config:
        from_attributes = True
