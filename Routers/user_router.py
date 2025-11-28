from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.user_schema import UserResponse,UserOut
from Services.user_service import get_all_users
from Core.security import get_current_user


router = APIRouter(prefix="/users", tags=["users"])
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.get("/admin")
def admin_route(current_user: UserResponse = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return {"message": f"Bienvenido administrador {current_user.username}"}

@router.get("/all", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users
