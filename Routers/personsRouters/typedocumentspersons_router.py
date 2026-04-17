from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Core.security import get_current_user
from Schemas.user_schema import UserResponse
from Schemas.personsSchemas.typedocumentspersons_schema import (
    TypeDocumentsPersonsCreate,
    TypeDocumentsPersonsResponse,
    TypeDocumentsPersonsUpdate,
)
from Services.persosnsSevices import typedocumentspersons_service


router = APIRouter(prefix="/type-documents-persons", tags=["type-documents-persons"])


@router.get("/", response_model=list[TypeDocumentsPersonsResponse])
def get_all_type_documents_persons(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        return typedocumentspersons_service.get_all_type_documents_persons(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de documento: {str(e)}")


@router.get("/{tpdu_id}", response_model=TypeDocumentsPersonsResponse)
def get_type_document_person_by_id(
    tpdu_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    item = typedocumentspersons_service.get_type_document_person_by_id(db, tpdu_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return item


@router.get("/search/query", response_model=list[TypeDocumentsPersonsResponse])
def search_type_documents_persons(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    code: Optional[str] = Query(None, description="Buscar por código"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        return typedocumentspersons_service.search_type_documents_persons(db=db, name=name, code=code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")


@router.post("/", response_model=TypeDocumentsPersonsResponse, status_code=201)
def create_type_document_person(
    data: TypeDocumentsPersonsCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        return typedocumentspersons_service.create_type_document_person(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear tipo de documento: {str(e)}")


@router.put("/{tpdu_id}", response_model=TypeDocumentsPersonsResponse)
def update_type_document_person(
    tpdu_id: int,
    data: TypeDocumentsPersonsUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        item = typedocumentspersons_service.update_type_document_person(db, tpdu_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar tipo de documento: {str(e)}")


@router.delete("/{tpdu_id}", status_code=200)
def delete_type_document_person(
    tpdu_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        deleted = typedocumentspersons_service.delete_type_document_person(db, tpdu_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
        return {"message": "Tipo de documento eliminado exitosamente", "tpdu_id": tpdu_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar tipo de documento: {str(e)}")
