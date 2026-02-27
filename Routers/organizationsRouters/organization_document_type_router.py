from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.organizationSchema.organization_document_type_schema import OrganizationDocumentTypeCreate, OrganizationDocumentTypeUpdate, OrganizationDocumentTypeResponse
from Schemas.user_schema import UserResponse
from Services.organizationServices import organization_document_type_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/organization-document-types", tags=["organization-document-types"])

@router.get("/", response_model=list[OrganizationDocumentTypeResponse])
def get_all_organization_document_types(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los tipos de documentos de organización."""
    try:
        organization_document_types = organization_document_type_service.get_all_organization_document_types(db)
        return organization_document_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de documentos de organización: {str(e)}")

@router.get("/{organization_document_type_id}", response_model=OrganizationDocumentTypeResponse)
def get_organization_document_type_by_id(
    organization_document_type_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un tipo de documento de organización por su ID."""
    organization_document_type = organization_document_type_service.get_organization_document_type_by_id(db, organization_document_type_id)
    if not organization_document_type:
        raise HTTPException(status_code=404, detail="Tipo de documento de organización no encontrado")
    return organization_document_type

@router.get("/search/query", response_model=list[OrganizationDocumentTypeResponse])
def search_organization_document_types(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca tipos de documentos de organización usando múltiples criterios de búsqueda."""
    try:
        organization_document_types = organization_document_type_service.search_organization_document_types(
            db=db,
            name=name
        )
        return organization_document_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=OrganizationDocumentTypeResponse, status_code=201)
def create_organization_document_type(
    organization_document_type_data: OrganizationDocumentTypeCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo tipo de documento de organización."""
    try:
        new_organization_document_type = organization_document_type_service.create_organization_document_type(db, organization_document_type_data)
        return new_organization_document_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear tipo de documento de organización: {str(e)}")

@router.put("/{organization_document_type_id}", response_model=OrganizationDocumentTypeResponse)
def update_organization_document_type(
    organization_document_type_id: int,
    organization_document_type_data: OrganizationDocumentTypeUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un tipo de documento de organización existente."""
    try:
        updated_organization_document_type = organization_document_type_service.update_organization_document_type(db, organization_document_type_id, organization_document_type_data)
        if not updated_organization_document_type:
            raise HTTPException(status_code=404, detail="Tipo de documento de organización no encontrado")
        return updated_organization_document_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar tipo de documento de organización: {str(e)}")

@router.delete("/{organization_document_type_id}", status_code=200)
def delete_organization_document_type(
    organization_document_type_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un tipo de documento de organización de la base de datos."""
    try:
        deleted_organization_document_type = organization_document_type_service.delete_organization_document_type(db, organization_document_type_id)
        if not deleted_organization_document_type:
            raise HTTPException(status_code=404, detail="Tipo de documento de organización no encontrado")
        return {"message": "Tipo de documento de organización eliminado exitosamente", "organization_document_type_id": organization_document_type_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar tipo de documento de organización: {str(e)}")
