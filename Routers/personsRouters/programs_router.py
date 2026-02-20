from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas.programs_schema import ProgramCreate, ProgramUpdate, ProgramResponse
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import programs_service
from Core.security import get_current_user
from typing import Optional

router = APIRouter(prefix="/programs", tags=["programs"])

@router.get("/", response_model=list[ProgramResponse])
def get_all_programs(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Incluir programas inactivos"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtiene todos los programas activos (o todos si include_inactive=True)."""
    try:
        programs = programs_service.get_all_programs(db, include_inactive=include_inactive)
        return programs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener programas: {str(e)}")

@router.get("/{program_id}", response_model=ProgramResponse)
def get_program_by_id(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca un programa por su ID."""
    program = programs_service.get_program_by_id(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return program

@router.get("/search/query", response_model=list[ProgramResponse])
def search_programs(
    name: Optional[str] = Query(None, description="Buscar por nombre"),
    include_inactive: bool = Query(False, description="Incluir programas inactivos en la búsqueda"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Busca programas usando múltiples criterios de búsqueda."""
    try:
        programs = programs_service.search_programs(
            db=db,
            name=name,
            include_inactive=include_inactive
        )
        return programs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.post("/", response_model=ProgramResponse, status_code=201)
def create_program(
    program_data: ProgramCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crea un nuevo programa."""
    try:
        new_program = programs_service.create_program(db, program_data)
        return new_program
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear programa: {str(e)}")

@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    program_data: ProgramUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualiza los datos de un programa existente."""
    try:
        updated_program = programs_service.update_program(db, program_id, program_data)
        if not updated_program:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        return updated_program
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar programa: {str(e)}")

@router.delete("/{program_id}", status_code=200)
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Elimina permanentemente un programa de la base de datos."""
    try:
        deleted_program = programs_service.delete_program(db, program_id)
        if not deleted_program:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        return {"message": "Programa eliminado exitosamente", "program_id": program_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar programa: {str(e)}")

@router.patch("/{program_id}/deactivate", response_model=ProgramResponse)
def deactivate_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Inactiva un programa (soft delete)."""
    try:
        deactivated_program = programs_service.deactivate_program(db, program_id)
        if not deactivated_program:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        return deactivated_program
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar programa: {str(e)}")

@router.patch("/{program_id}/activate", response_model=ProgramResponse)
def activate_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Activa un programa previamente inactivado."""
    try:
        activated_program = programs_service.activate_program(db, program_id)
        if not activated_program:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        return activated_program
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar programa: {str(e)}")
