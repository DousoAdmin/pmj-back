from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.genders_schema import GenderCreate, GenderUpdate, GenderResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import genders_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/genders", tags=["genders"])

@router.get("/", response_model=list[GenderResponse])
def get_all_genders(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Incluir géneros inactivos"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los géneros activos (o todos si include_inactive=True)."""
    try:
        genders = genders_service.get_all_genders(db, include_inactive=include_inactive)
        return genders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener géneros: {str(e)}")

@router.get("/{gender_id}", response_model=GenderResponse)
def get_gender_by_id(
    gender_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un género por su ID."""
    gender = genders_service.get_gender_by_id(db, gender_id)
    if not gender:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return gender

@router.get("/search/query", response_model=list[GenderResponse])
def search_genders(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    include_inactive: bool = Query(False, description="Incluir géneros inactivos en la búsqueda"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca géneros usando múltiples criterios de búsqueda."""
    try:
        genders = genders_service.search_genders(
            db=db,
            name=name,
            include_inactive=include_inactive
        )
        return genders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=GenderResponse, status_code=201)
def create_gender(
    gender_data: GenderCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo género."""
    try:
        new_gender = genders_service.create_gender(db, gender_data)
        return new_gender
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear género: {str(e)}")

@router.put("/{gender_id}", response_model=GenderResponse)
def update_gender(
    gender_id: int,
    gender_data: GenderUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un género existente."""
    try:
        updated_gender = genders_service.update_gender(db, gender_id, gender_data)
        if not updated_gender:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return updated_gender
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar género: {str(e)}")

@router.delete("/{gender_id}", status_code=200)
def delete_gender(
    gender_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un género de la base de datos."""
    try:
        deleted_gender = genders_service.delete_gender(db, gender_id)
        if not deleted_gender:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return {"message": "Género eliminado exitosamente", "gender_id": gender_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar género: {str(e)}")

@router.patch("/{gender_id}/deactivate", response_model=GenderResponse)
def deactivate_gender(
    gender_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Inactiva un género (soft delete)."""
    try:
        deactivated_gender = genders_service.deactivate_gender(db, gender_id)
        if not deactivated_gender:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return deactivated_gender
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar género: {str(e)}")

@router.patch("/{gender_id}/activate", response_model=GenderResponse)
def activate_gender(
    gender_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Activa un género previamente inactivado."""
    try:
        activated_gender = genders_service.activate_gender(db, gender_id)
        if not activated_gender:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return activated_gender
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar género: {str(e)}")
