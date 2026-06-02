from pydantic import BaseModel, Field
from typing import Optional

class DisabilityCreate(BaseModel):
    DSBT_name: Optional[str] = Field(None, max_length=45)
    DSBT_description: Optional[str] = Field(None, max_length=150)
    DSBT_state: Optional[bool] = None

class DisabilityUpdate(BaseModel):
    DSBT_name: Optional[str] = Field(None, max_length=45)
    DSBT_description: Optional[str] = Field(None, max_length=150)
    DSBT_state: Optional[bool] = None


class DisabilityResponse(BaseModel):
    id: int
    nombre: Optional[str]
    descripcion: Optional[str]
    estado: Optional[bool]
    
    class Config:
        from_attributes = True
