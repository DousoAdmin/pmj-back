from pathlib import Path
import sys

# Asegura que la raíz del proyecto esté en PYTHONPATH (robusto en Azure)
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from Config.database import Base, engine

# 1) Importa TODOS los modelos (para que SQLAlchemy resuelva relaciones)
from Models.users import (
    userModel, statesuserModel, logsModel, rolesModel,
    permissionsModel, rolesPermissionModel,usersRolesOrganizationsModel
)
from Models.persons import (
    personsModel, userpersonalModel, beneficiarysModel, disabilitysModel,
    documentsModel, documentstatesModel, ethnicityModel, gendersModel,
    personsdocumentModel, programsModel, sexualidentitysModel,
    statepersondocumentModel
)
#from Models.organizations import (
#   approachesModel, organizationStatusesModel, organizationapproachesModel,
 #   organizationDocumentModel, organizationDocumentTypeModel,
#    organizationObservationsModel, organizationsModel, organizationTypeModel
#)
from Models.organizations import approachesModel
from Models.organizations import organizationStatusesModel
from Models.organizations import organizationapproachesModel
from Models.organizations import organizationDocumentModel
from Models.organizations import organizationDocumentTypeModel
from Models.organizations import organizationObservationsModel
from Models.organizations import organizationsModel
from Models.organizations import organizationTypeModel

# 2) Crea tablas
Base.metadata.create_all(bind=engine)

# 3) App
app = FastAPI(title="Plataforma Modular con FastAPI")

# 4) Descubrimiento recursivo de routers en Routers/ y subcarpetas
import importlib
import pkgutil
from typing import Iterable
from fastapi import APIRouter

def _iter_module_routers(module) -> Iterable[APIRouter]:
    """Devuelve todos los APIRouter que un módulo exponga de forma común."""
    # a) variable "router" (convención típica)
    if hasattr(module, "router") and isinstance(getattr(module, "router"), APIRouter):
        yield getattr(module, "router")
    # b) lista/tupla "routers" (varios routers por módulo)
    if hasattr(module, "routers"):
        val = getattr(module, "routers")
        if isinstance(val, (list, tuple)):
            for r in val:
                if isinstance(r, APIRouter):
                    yield r
    # c) función "get_router()" (algunos proyectos lo usan)
    if hasattr(module, "get_router"):
        try:
            r = module.get_router()
            if isinstance(r, APIRouter):
                yield r
        except Exception:
            pass

def include_all_routers(app: FastAPI, package_name: str = "Routers"):
    """
    Importa recursivamente todos los módulos bajo `package_name`
    e incluye cualquier APIRouter expuesto.
    """
    try:
        pkg = importlib.import_module(package_name)
    except ModuleNotFoundError:
        print(f"[routers] Paquete '{package_name}' no encontrado")
        return

    # IMPORTANTÍSIMO: cada carpeta dentro de Routers debe tener __init__.py
    discovered = set()

    for finder, name, ispkg in pkgutil.walk_packages(pkg.__path__, prefix=package_name + "."):
        # Evita módulos "privados" o duplicados
        short = name.rsplit(".", 1)[-1]
        if short.startswith("_"):
            continue
        if name in discovered:
            continue
        discovered.add(name)

        try:
            module = importlib.import_module(name)
        except Exception as e:
            print(f"[routers] Error importando {name}: {e}")
            continue

        found_any = False
        for r in _iter_module_routers(module):
            app.include_router(r)
            found_any = True

        if found_any:
            print(f"[routers] Registrado(s) en: {name}")

# 5) Incluir todos los routers recursivamente
include_all_routers(app, "Routers")