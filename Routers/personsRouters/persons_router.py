from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.personsSchemas import persosns_schema
from Schemas.user_schema import UserResponse
from Services.persosnsSevices import persons_service
from Core.security import get_current_user

router = APIRouter(prefix="/persons", tags=["persons"])

@router.get("/listPersons", response_model=list[persosns_schema.personsResponse])

def get_all_persons(db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    persons = persons_service.get_all_persons(db)
    return persons



