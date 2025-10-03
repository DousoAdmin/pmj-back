from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    USER_FK_user_create : int 
    USER_FK_user_update : int
    USER_username : str
    USER_password : str
    USER_FK_state_user : int
    USER_reset_password : int
    USER_address_ip : str

class UserLogin(BaseModel):
    USER_username: str
    USER_password: str

class UserResponse(BaseModel):
    USER_PK: int
    USER_username: str
    class Config:
        orm_mode = True
        
class UserOut(BaseModel):
    USER_PK: int
    USER_username: str
    USER_email: str
    USER_full_name: str

    class Config:
        orm_mode = True