from pydantic import BaseModel, EmailStr
from datetime import date, datetime
class personsResponse(BaseModel):
    PRSN_PK: int
    PRSN_name: str
    PRSN_lastname: str
    PRSN_phone: str
    PRSN_email: EmailStr
    PRSN_brithday: date
    PRSN_identification: str
    PRSN_location: str

    # ForeingKey
    PRSN_FK_ethnicity:int
    PRSN_FK_disability:int
    PRSN_FK_gender:int
    PRSN_FK_sexualidentity:int
    class Config:
        orm_mode = True
 