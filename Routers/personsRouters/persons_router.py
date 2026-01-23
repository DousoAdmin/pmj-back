from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas import persosns_schema
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import persons_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/persons", tags=["persons"])

# -------------------------
# GET ALL - Listar todas las personas
# -------------------------
@router.get("/", response_model=list[persosns_schema.personsResponse])
def get_all_persons(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Incluir personas inactivas"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todas las personas activas (o todas si include_inactive=True)."""
    try:
        persons = persons_service.get_all_persons(db, include_inactive=include_inactive)
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener personas: {str(e)}")

# -------------------------
# GET BY ID - Buscar persona por ID
# -------------------------
@router.get("/{person_id}", response_model=persosns_schema.personsResponse)
def get_person_by_id(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca una persona por su ID."""
    person = persons_service.get_person_by_id(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return person

# -------------------------
# SEARCH - Buscar personas con filtros
# -------------------------
@router.get("/search/query", response_model=list[persosns_schema.personsResponse])
def search_persons(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    lastname: Optional[str] = Query(None, description="Buscar por apellido"),
    identification: Optional[str] = Query(None, description="Buscar por número de identificación"),
    email: Optional[str] = Query(None, description="Buscar por email"),
    phone: Optional[str] = Query(None, description="Buscar por teléfono"),
    include_inactive: bool = Query(False, description="Incluir personas inactivas en la búsqueda"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca personas usando múltiples criterios de búsqueda."""
    try:
        persons = persons_service.search_persons(
            db=db,
            name=name,
            lastname=lastname,
            identification=identification,
            email=email,
            phone=phone,
            include_inactive=include_inactive
        )
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

# -------------------------
# CREATE - Crear nueva persona
# -------------------------
@router.post("/", response_model=persosns_schema.personsResponse, status_code=201)
def create_person(
    person_data: persosns_schema.PersonCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea una nueva persona."""
    try:
        new_person = persons_service.create_person(db, person_data)
        return new_person
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear persona: {str(e)}")

# -------------------------
# UPDATE - Actualizar persona
# -------------------------
@router.put("/{person_id}", response_model=persosns_schema.personsResponse)
def update_person(
    person_id: int,
    person_data: persosns_schema.PersonUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de una persona existente."""
    try:
        updated_person = persons_service.update_person(db, person_id, person_data)
        if not updated_person:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return updated_person
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar persona: {str(e)}")

# -------------------------
# DELETE - Eliminar persona permanentemente
# -------------------------
@router.delete("/{person_id}", status_code=200)
def delete_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente una persona de la base de datos."""
    try:
        deleted_person = persons_service.delete_person(db, person_id)
        if not deleted_person:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return {"message": "Persona eliminada exitosamente", "person_id": person_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar persona: {str(e)}")

# -------------------------
# DEACTIVATE - Inactivar persona
# -------------------------
@router.patch("/{person_id}/deactivate", response_model=persosns_schema.personsResponse)
def deactivate_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Inactiva una persona (soft delete)."""
    try:
        deactivated_person = persons_service.deactivate_person(db, person_id)
        if not deactivated_person:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return deactivated_person
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar persona: {str(e)}")

# -------------------------
# ACTIVATE - Activar persona
# -------------------------
@router.patch("/{person_id}/activate", response_model=persosns_schema.personsResponse)
def activate_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Activa una persona previamente inactivada."""
    try:
        activated_person = persons_service.activate_person(db, person_id)
        if not activated_person:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return activated_person
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar persona: {str(e)}")

