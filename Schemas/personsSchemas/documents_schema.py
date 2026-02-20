from pydantic import BaseModel, Field
from typing import Optional

class DocumentCreate(BaseModel):
    DCMT_name: str = Field(..., min_length=1, max_length=45)
    DCMT_description: Optional[str] = Field(None, max_length=255)
    DCMT_FK_state: Optional[int] = Field(None, description="ID de estado del documento")

class DocumentUpdate(BaseModel):
    DCMT_name: Optional[str] = Field(None, min_length=1, max_length=45)
    DCMT_description: Optional[str] = Field(None, max_length=255)
    DCMT_FK_state: Optional[int] = Field(None, description="ID de estado del documento")

class DocumentResponse(BaseModel):
    DCMT_PK: int
    DCMT_name: str
    DCMT_description: Optional[str]
    DCMT_FK_state: Optional[int]
    
    class Config:
        from_attributes = True
