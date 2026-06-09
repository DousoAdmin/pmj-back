from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.userShemas.user_schema import UserCreate, UserResponse,UserOut
from Schemas.organizationSchema.organization_Shema import OrganizationSimple
from Services.user_service import get_all_users
from Services.userServices import user_service
from Core.security import get_current_user
from Services.userServices.users_roles_organizations_service import get_user_role_organizations_by_user
from Services.OrganizationServices import organization_service
from Services.OrganizationServices.organization_status_service import get_organization_status
from Services.OrganizationServices.organization_type_service import get_organization_type_by_id
from typing import List

router = APIRouter(prefix="/user", tags=["user"])



#---------------------------RUTA USER ---------------------------


@router.get("/meOrganizations", response_model=List[OrganizationSimple])
def get_user_organizations(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
	"""Devuelve las organizaciones a las que pertenece el usuario autenticado (campos sin prefijos DB)."""
	try:
		role_orgs = get_user_role_organizations_by_user(db, current_user.USER_PK)
		if not role_orgs:
			return []

		result = []
		for uro in role_orgs:
			org = organization_service.get_organization_by_id(db, uro.USRL_FK_organization)
			if not org:
				continue
			status = get_organization_status(db, org.ORGZ_FK_statu) if org.ORGZ_FK_statu else None
			type_data = get_organization_type_by_id(db, org.ORGZ_FK_type) if org.ORGZ_FK_type else None
			result.append({
				"id_organizacion": org.ORGZ_PK,
				"nombre": org.ORGZ_name,
				"descripcion": org.ORGZ_descriptions,
				"nit": org.ORGZ_nit,
				"fecha_creacion": org.ORGZ_creation_date,
				"id_estado": status.ORST_PK if status else None,
				"nombre_estado": status.ORST_name if status else None,
				"id_tipo": type_data.ORTP_PK if type_data else None,
				"nombre_tipo": type_data.ORTP_name if type_data else None,
			})

		return result
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


