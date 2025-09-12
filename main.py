from fastapi import FastAPI
from Config.database import Base, engine
import importlib
import pkgutil

app = FastAPI(title="Plataforma Modular con FastAPI")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Importar TODOS los routers dentro de app.Routers (con mayúscula)
from Routers import __path__ as routers_path

for module_info in pkgutil.iter_modules(routers_path):
    module_name = f"Routers.{module_info.name}"
    module = importlib.import_module(module_name)
    
    router = getattr(module, "router", None)
    if router:
        app.include_router(router)

# Endpoint por defecto
@app.get("/")
def root():
    return {"message": "API trabajando correctamente 😎"}