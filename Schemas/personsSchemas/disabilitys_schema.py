from pydantic import BaseModel, Field
from typing import Optional

class DisabilityCreate(BaseModel):
    DSBT_name: Optional[str] = Field(None, max_length=45)
    DSBT_description: Optional[str] = Field(None, max_length=150)
    DSBT_state: Optional[bytes] = None

class DisabilityUpdate(BaseModel):
    DSBT_name: Optional[str] = Field(None, max_length=45)
    DSBT_description: Optional[str] = Field(None, max_length=150)
    DSBT_state: Optional[bytes] = None

class DisabilityResponse(BaseModel):
    DSBT_PY: int
    DSBT_name: Optional[str]
    DSBT_description: Optional[str]
    DSBT_state: Optional[bytes]
    
    class Config:
        from_attributes = True
