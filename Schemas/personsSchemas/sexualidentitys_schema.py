from pydantic import BaseModel, Field
from typing import Optional

class SexualIdentityCreate(BaseModel):
    SXID_name: Optional[str] = Field(None, max_length=45)
    SXID_description: Optional[str] = Field(None, max_length=250)

class SexualIdentityUpdate(BaseModel):
    SXID_name: Optional[str] = Field(None, max_length=45)
    SXID_description: Optional[str] = Field(None, max_length=250)

class SexualIdentityResponse(BaseModel):
    SXID_PK: int
    SXID_name: Optional[str]
    SXID_description: Optional[str]
    
    class Config:
        from_attributes = True
