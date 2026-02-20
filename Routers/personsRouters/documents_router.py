from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.documents_schema import DocumentCreate, DocumentUpdate, DocumentResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import documents_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_model=list[DocumentResponse])
def get_all_documents(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los documentos."""
    try:
        documents = documents_service.get_all_documents(db)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {str(e)}")

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_by_id(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un documento por su ID."""
    document = documents_service.get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document

@router.get("/search/query", response_model=list[DocumentResponse])
def search_documents(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca documentos usando múltiples criterios de búsqueda."""
    try:
        documents = documents_service.search_documents(
            db=db,
            name=name
        )
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=DocumentResponse, status_code=201)
def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo documento."""
    try:
        new_document = documents_service.create_document(db, document_data)
        return new_document
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear documento: {str(e)}")

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un documento existente."""
    try:
        updated_document = documents_service.update_document(db, document_id, document_data)
        if not updated_document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return updated_document
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar documento: {str(e)}")

@router.delete("/{document_id}", status_code=200)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un documento de la base de datos."""
    try:
        deleted_document = documents_service.delete_document(db, document_id)
        if not deleted_document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return {"message": "Documento eliminado exitosamente", "document_id": document_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar documento: {str(e)}")
