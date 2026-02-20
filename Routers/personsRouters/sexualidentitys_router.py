from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.sexualidentitys_schema import SexualIdentityCreate, SexualIdentityUpdate, SexualIdentityResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import sexualidentitys_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/sexualidentitys", tags=["sexualidentitys"])

@router.get("/", response_model=list[SexualIdentityResponse])
def get_all_sexualidentitys(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todas las identidades sexuales."""
    try:
        sexualidentitys = sexualidentitys_service.get_all_sexualidentitys(db)
        return sexualidentitys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener identidades sexuales: {str(e)}")

@router.get("/{sexualidentity_id}", response_model=SexualIdentityResponse)
def get_sexualidentity_by_id(
    sexualidentity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca una identidad sexual por su ID."""
    sexualidentity = sexualidentitys_service.get_sexualidentity_by_id(db, sexualidentity_id)
    if not sexualidentity:
        raise HTTPException(status_code=404, detail="Identidad sexual no encontrada")
    return sexualidentity

@router.get("/search/query", response_model=list[SexualIdentityResponse])
def search_sexualidentitys(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca identidades sexuales usando múltiples criterios de búsqueda."""
    try:
        sexualidentitys = sexualidentitys_service.search_sexualidentitys(
            db=db,
            name=name
        )
        return sexualidentitys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=SexualIdentityResponse, status_code=201)
def create_sexualidentity(
    sexualidentity_data: SexualIdentityCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea una nueva identidad sexual."""
    try:
        new_sexualidentity = sexualidentitys_service.create_sexualidentity(db, sexualidentity_data)
        return new_sexualidentity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear identidad sexual: {str(e)}")

@router.put("/{sexualidentity_id}", response_model=SexualIdentityResponse)
def update_sexualidentity(
    sexualidentity_id: int,
    sexualidentity_data: SexualIdentityUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de una identidad sexual existente."""
    try:
        updated_sexualidentity = sexualidentitys_service.update_sexualidentity(db, sexualidentity_id, sexualidentity_data)
        if not updated_sexualidentity:
            raise HTTPException(status_code=404, detail="Identidad sexual no encontrada")
        return updated_sexualidentity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar identidad sexual: {str(e)}")

@router.delete("/{sexualidentity_id}", status_code=200)
def delete_sexualidentity(
    sexualidentity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente una identidad sexual de la base de datos."""
    try:
        deleted_sexualidentity = sexualidentitys_service.delete_sexualidentity(db, sexualidentity_id)
        if not deleted_sexualidentity:
            raise HTTPException(status_code=404, detail="Identidad sexual no encontrada")
        return {"message": "Identidad sexual eliminada exitosamente", "sexualidentity_id": sexualidentity_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar identidad sexual: {str(e)}")
