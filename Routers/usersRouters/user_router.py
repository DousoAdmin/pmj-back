from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.userShemas.user_schema import UserCreate, UserResponse,UserOut
from Services.user_service import get_all_users
from Services.userServices import user_service
from Core.security import get_current_user

router = APIRouter(prefix="/user", tags=["user"])



#---------------------------RUTA USER ---------------------------
#Traer todos 
@router.get("/all", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    user = user_service.get_users(db)
    return user


#Traer por id
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    user = user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

#Crear
@router.post("/", response_model=UserOut)
def create(user: UserCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return user.create_user(db, user)

#Actualizar
@router.put("/{user_id}", response_model=UserOut)
def update(user_id: int, data: UserCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    updated = user_service.update_user(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated

#Eliminar
@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    deleted = user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario Eliminado"}




