from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    USER_username: str
    USER_email: EmailStr
    USER_password: str
    USER_full_name: str

class UserLogin(BaseModel):
    USER_username: str
    USER_password: str

class UserResponse(BaseModel):
    USER_id: int
    USER_username: str
    USER_email: EmailStr
    class Config:
        orm_mode = True
        
class UserOut(BaseModel):
    USER_id: int
    USER_username: str
    USER_email: str
    USER_full_name: str

    class Config:
        orm_mode = True