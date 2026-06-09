from datetime import date

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    USER_FK_user_create : int 
    USER_FK_user_update : int
    USER_username : str
    USER_password : str
    USER_FK_state_user : int
    USER_reset_password : int
    USER_address_ip : str


class UserRegister(BaseModel):
    full_name: str
    identification: str
    type_document: int
    birthday: date
    email: str
    phone: str
    location: str
    etnia: int
    discapacidad: int
    genero: int
    identidad_sexual: int
    password: str


class UserLogin(BaseModel):
    USER_username: str
    USER_password: str

class UserResponse(BaseModel):
    USER_PK: int
    USER_username: str
    class Config:
        from_attributes = True
        
class UserOut(BaseModel):
    USER_FK_user_create : int 
    USER_FK_user_update : int
    USER_username : str
    USER_password : str
    USER_FK_state_user : int
    USER_reset_password : int
    USER_address_ip : str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse  # Incluir datos del usuario para mostrar en UI