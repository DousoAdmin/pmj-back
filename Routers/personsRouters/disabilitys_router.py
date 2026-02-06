from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.disabilitys_schema import DisabilityCreate, DisabilityUpdate, DisabilityResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import disabilitys_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/disabilitys", tags=["disabilitys"])

@router.get("/", response_model=list[DisabilityResponse])
def get_all_disabilitys(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Incluir discapacidades inactivas"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todas las discapacidades activas (o todas si include_inactive=True)."""
    try:
        disabilitys = disabilitys_service.get_all_disabilitys(db, include_inactive=include_inactive)
        return disabilitys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener discapacidades: {str(e)}")

@router.get("/{disability_id}", response_model=DisabilityResponse)
def get_disability_by_id(
    disability_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca una discapacidad por su ID."""
    disability = disabilitys_service.get_disability_by_id(db, disability_id)
    if not disability:
        raise HTTPException(status_code=404, detail="Discapacidad no encontrada")
    return disability

@router.get("/search/query", response_model=list[DisabilityResponse])
def search_disabilitys(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    include_inactive: bool = Query(False, description="Incluir discapacidades inactivas en la búsqueda"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca discapacidades usando múltiples criterios de búsqueda."""
    try:
        disabilitys = disabilitys_service.search_disabilitys(
            db=db,
            name=name,
            include_inactive=include_inactive
        )
        return disabilitys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=DisabilityResponse, status_code=201)
def create_disability(
    disability_data: DisabilityCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea una nueva discapacidad."""
    try:
        new_disability = disabilitys_service.create_disability(db, disability_data)
        return new_disability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear discapacidad: {str(e)}")

@router.put("/{disability_id}", response_model=DisabilityResponse)
def update_disability(
    disability_id: int,
    disability_data: DisabilityUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de una discapacidad existente."""
    try:
        updated_disability = disabilitys_service.update_disability(db, disability_id, disability_data)
        if not updated_disability:
            raise HTTPException(status_code=404, detail="Discapacidad no encontrada")
        return updated_disability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar discapacidad: {str(e)}")

@router.delete("/{disability_id}", status_code=200)
def delete_disability(
    disability_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente una discapacidad de la base de datos."""
    try:
        deleted_disability = disabilitys_service.delete_disability(db, disability_id)
        if not deleted_disability:
            raise HTTPException(status_code=404, detail="Discapacidad no encontrada")
        return {"message": "Discapacidad eliminada exitosamente", "disability_id": disability_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar discapacidad: {str(e)}")

@router.patch("/{disability_id}/deactivate", response_model=DisabilityResponse)
def deactivate_disability(
    disability_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Inactiva una discapacidad (soft delete)."""
    try:
        deactivated_disability = disabilitys_service.deactivate_disability(db, disability_id)
        if not deactivated_disability:
            raise HTTPException(status_code=404, detail="Discapacidad no encontrada")
        return deactivated_disability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar discapacidad: {str(e)}")

@router.patch("/{disability_id}/activate", response_model=DisabilityResponse)
def activate_disability(
    disability_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Activa una discapacidad previamente inactivada."""
    try:
        activated_disability = disabilitys_service.activate_disability(db, disability_id)
        if not activated_disability:
            raise HTTPException(status_code=404, detail="Discapacidad no encontrada")
        return activated_disability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar discapacidad: {str(e)}")
