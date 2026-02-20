from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.documentstates_schema import DocumentStateCreate, DocumentStateUpdate, DocumentStateResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import documentstates_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/documentstates", tags=["documentstates"])

@router.get("/", response_model=list[DocumentStateResponse])
def get_all_documentstates(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los estados de documentos."""
    try:
        documentstates = documentstates_service.get_all_documentstates(db)
        return documentstates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estados de documentos: {str(e)}")

@router.get("/{documentstate_id}", response_model=DocumentStateResponse)
def get_documentstate_by_id(
    documentstate_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un estado de documento por su ID."""
    documentstate = documentstates_service.get_documentstate_by_id(db, documentstate_id)
    if not documentstate:
        raise HTTPException(status_code=404, detail="Estado de documento no encontrado")
    return documentstate

@router.get("/search/query", response_model=list[DocumentStateResponse])
def search_documentstates(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca estados de documentos usando múltiples criterios de búsqueda."""
    try:
        documentstates = documentstates_service.search_documentstates(
            db=db,
            name=name
        )
        return documentstates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=DocumentStateResponse, status_code=201)
def create_documentstate(
    documentstate_data: DocumentStateCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo estado de documento."""
    try:
        new_documentstate = documentstates_service.create_documentstate(db, documentstate_data)
        return new_documentstate
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear estado de documento: {str(e)}")

@router.put("/{documentstate_id}", response_model=DocumentStateResponse)
def update_documentstate(
    documentstate_id: int,
    documentstate_data: DocumentStateUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un estado de documento existente."""
    try:
        updated_documentstate = documentstates_service.update_documentstate(db, documentstate_id, documentstate_data)
        if not updated_documentstate:
            raise HTTPException(status_code=404, detail="Estado de documento no encontrado")
        return updated_documentstate
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar estado de documento: {str(e)}")

@router.delete("/{documentstate_id}", status_code=200)
def delete_documentstate(
    documentstate_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un estado de documento de la base de datos."""
    try:
        deleted_documentstate = documentstates_service.delete_documentstate(db, documentstate_id)
        if not deleted_documentstate:
            raise HTTPException(status_code=404, detail="Estado de documento no encontrado")
        return {"message": "Estado de documento eliminado exitosamente", "documentstate_id": documentstate_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar estado de documento: {str(e)}")
