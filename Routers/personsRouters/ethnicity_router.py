from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.ethnicity_schema import EthnicityCreate, EthnicityUpdate, EthnicityResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import ethnicity_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/ethnicities", tags=["ethnicities"])

@router.get("/", response_model=list[EthnicityResponse])
def get_all_ethnicities(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Incluir etnias inactivas"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todas las etnias activas (o todas si include_inactive=True)."""
    try:
        ethnicities = ethnicity_service.get_all_ethnicities(db, include_inactive=include_inactive)
        return ethnicities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener etnias: {str(e)}")

@router.get("/{ethnicity_id}", response_model=EthnicityResponse)
def get_ethnicity_by_id(
    ethnicity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca una etnia por su ID."""
    ethnicity = ethnicity_service.get_ethnicity_by_id(db, ethnicity_id)
    if not ethnicity:
        raise HTTPException(status_code=404, detail="Etnia no encontrada")
    return ethnicity

@router.get("/search/query", response_model=list[EthnicityResponse])
def search_ethnicities(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    include_inactive: bool = Query(False, description="Incluir etnias inactivas en la búsqueda"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca etnias usando múltiples criterios de búsqueda."""
    try:
        ethnicities = ethnicity_service.search_ethnicities(
            db=db,
            name=name,
            include_inactive=include_inactive
        )
        return ethnicities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=EthnicityResponse, status_code=201)
def create_ethnicity(
    ethnicity_data: EthnicityCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea una nueva etnia."""
    try:
        new_ethnicity = ethnicity_service.create_ethnicity(db, ethnicity_data)
        return new_ethnicity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear etnia: {str(e)}")

@router.put("/{ethnicity_id}", response_model=EthnicityResponse)
def update_ethnicity(
    ethnicity_id: int,
    ethnicity_data: EthnicityUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de una etnia existente."""
    try:
        updated_ethnicity = ethnicity_service.update_ethnicity(db, ethnicity_id, ethnicity_data)
        if not updated_ethnicity:
            raise HTTPException(status_code=404, detail="Etnia no encontrada")
        return updated_ethnicity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar etnia: {str(e)}")

@router.delete("/{ethnicity_id}", status_code=200)
def delete_ethnicity(
    ethnicity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente una etnia de la base de datos."""
    try:
        deleted_ethnicity = ethnicity_service.delete_ethnicity(db, ethnicity_id)
        if not deleted_ethnicity:
            raise HTTPException(status_code=404, detail="Etnia no encontrada")
        return {"message": "Etnia eliminada exitosamente", "ethnicity_id": ethnicity_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar etnia: {str(e)}")

@router.patch("/{ethnicity_id}/deactivate", response_model=EthnicityResponse)
def deactivate_ethnicity(
    ethnicity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Inactiva una etnia (soft delete)."""
    try:
        deactivated_ethnicity = ethnicity_service.deactivate_ethnicity(db, ethnicity_id)
        if not deactivated_ethnicity:
            raise HTTPException(status_code=404, detail="Etnia no encontrada")
        return deactivated_ethnicity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar etnia: {str(e)}")

@router.patch("/{ethnicity_id}/activate", response_model=EthnicityResponse)
def activate_ethnicity(
    ethnicity_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Activa una etnia previamente inactivada."""
    try:
        activated_ethnicity = ethnicity_service.activate_ethnicity(db, ethnicity_id)
        if not activated_ethnicity:
            raise HTTPException(status_code=404, detail="Etnia no encontrada")
        return activated_ethnicity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar etnia: {str(e)}")
