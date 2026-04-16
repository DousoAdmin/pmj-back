from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.approaches_schema import ApproachCreate, ApproachUpdate, ApproachResponse
from Schemas.user_schema import UserResponse
from Services.OrganizationServices import approaches_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/approaches", tags=["approaches"])

@router.get("/", response_model=list[ApproachResponse])
def get_all_approaches(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los enfoques."""
    try:
        approaches = approaches_service.get_all_approaches(db)
        return approaches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener enfoques: {str(e)}")

@router.get("/{approach_id}", response_model=ApproachResponse)
def get_approach_by_id(
    approach_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un enfoque por su ID."""
    approach = approaches_service.get_approach_by_id(db, approach_id)
    if not approach:
        raise HTTPException(status_code=404, detail="Enfoque no encontrado")
    return approach

@router.get("/search/query", response_model=list[ApproachResponse])
def search_approaches(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca enfoques usando múltiples criterios de búsqueda."""
    try:
        approaches = approaches_service.search_approaches(
            db=db,
            name=name
        )
        return approaches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=ApproachResponse, status_code=201)
def create_approach(
    approach_data: ApproachCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo enfoque."""
    try:
        new_approach = approaches_service.create_approach(db, approach_data)
        return new_approach
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear enfoque: {str(e)}")

@router.put("/{approach_id}", response_model=ApproachResponse)
def update_approach(
    approach_id: int,
    approach_data: ApproachUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un enfoque existente."""
    try:
        updated_approach = approaches_service.update_approach(db, approach_id, approach_data)
        if not updated_approach:
            raise HTTPException(status_code=404, detail="Enfoque no encontrado")
        return updated_approach
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar enfoque: {str(e)}")

@router.delete("/{approach_id}", status_code=200)
def delete_approach(
    approach_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un enfoque de la base de datos."""
    try:
        deleted_approach = approaches_service.delete_approach(db, approach_id)
        if not deleted_approach:
            raise HTTPException(status_code=404, detail="Enfoque no encontrado")
        return {"message": "Enfoque eliminado exitosamente", "approach_id": approach_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar enfoque: {str(e)}")
