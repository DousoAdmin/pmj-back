from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_types_schema import OrganizationTypeCreate, OrganizationTypeUpdate, OrganizationTypeResponse
from Schemas.user_schema import UserResponse
from Services.OrganizationServices import organization_types_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/organization-types", tags=["organization-types"])

@router.get("/", response_model=list[OrganizationTypeResponse])
def get_all_organization_types(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los tipos de organización."""
    try:
        organization_types = organization_types_service.get_all_organization_types(db)
        return organization_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de organización: {str(e)}")

@router.get("/{organization_type_id}", response_model=OrganizationTypeResponse)
def get_organization_type_by_id(
    organization_type_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un tipo de organización por su ID."""
    organization_type = organization_types_service.get_organization_type_by_id(db, organization_type_id)
    if not organization_type:
        raise HTTPException(status_code=404, detail="Tipo de organización no encontrado")
    return organization_type

@router.get("/search/query", response_model=list[OrganizationTypeResponse])
def search_organization_types(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca tipos de organización usando múltiples criterios de búsqueda."""
    try:
        organization_types = organization_types_service.search_organization_types(
            db=db,
            name=name
        )
        return organization_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=OrganizationTypeResponse, status_code=201)
def create_organization_type(
    organization_type_data: OrganizationTypeCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo tipo de organización."""
    try:
        new_organization_type = organization_types_service.create_organization_type(db, organization_type_data)
        return new_organization_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear tipo de organización: {str(e)}")

@router.put("/{organization_type_id}", response_model=OrganizationTypeResponse)
def update_organization_type(
    organization_type_id: int,
    organization_type_data: OrganizationTypeUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un tipo de organización existente."""
    try:
        updated_organization_type = organization_types_service.update_organization_type(db, organization_type_id, organization_type_data)
        if not updated_organization_type:
            raise HTTPException(status_code=404, detail="Tipo de organización no encontrado")
        return updated_organization_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar tipo de organización: {str(e)}")

@router.delete("/{organization_type_id}", status_code=200)
def delete_organization_type(
    organization_type_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un tipo de organización de la base de datos."""
    try:
        deleted_organization_type = organization_types_service.delete_organization_type(db, organization_type_id)
        if not deleted_organization_type:
            raise HTTPException(status_code=404, detail="Tipo de organización no encontrado")
        return {"message": "Tipo de organización eliminado exitosamente", "organization_type_id": organization_type_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar tipo de organización: {str(e)}")
