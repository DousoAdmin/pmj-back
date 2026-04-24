# 📋 TEMPLATE - Configuración Base para Nueva Aplicación

Use este template como base para crear nuevas aplicaciones similares a PMJ Backend.

---

## 📋 Checklist Inicial

- [ ] Nombre de aplicación definido
- [ ] Stack tecnológico elegido
- [ ] Base de datos planeada
- [ ] Modelos principales diseñados
- [ ] Endpoints requeridos listados

---

## 1. Información General

```yaml
# COMPLETAR

Nombre Aplicación: [TU_APP_NAME]
Descripción: [DESCRIPCION_CORTA]
Versión Inicial: 1.0.0
Framework: FastAPI
Lenguaje: Python 3.11+
Base de Datos: MySQL 8.0+
Autor/Equipo: [NOMBRE]
Fecha Inicio: [FECHA]
```

---

## 2. Stack Tecnológico

### Backend Base

```python
# Copiar estos en requirements.txt
fastapi==0.116.1
uvicorn==0.35.0
gunicorn==21.2.0
pydantic==2.11.7
pydantic-settings==2.10.1
sqlalchemy==2.0.43
pymysql==1.1.2
python-dotenv==1.1.1
python-jose==3.5.0
passlib==1.7.4
bcrypt==4.3.0
python-multipart==0.0.20
email-validator==2.3.0
```

### Opcional según necesidad

```python
# API Documentation
swagger-ui-bundle==3.52.3

# Testing
pytest==7.4.0
pytest-cov==4.1.0
httpx==0.24.0

# Database Migrations
alembic==1.16.5

# Caching
redis==5.0.0

# Async
aioredis==2.0.1
starlette==0.47.3
```

### Docker

```
- Docker Desktop (latest)
- Docker Compose (1.29+)
- Nginx (opcional)
```

---

## 3. Estructura de Directorios

```
tu-app-back/
│
├── main.py
├── requirements.txt
├── .env.template
├── README.md
│
├── Config/
│   ├── __init__.py
│   ├── config.py               # Settings
│   └── database.py             # SQLAlchemy setup
│
├── Core/
│   ├── __init__.py
│   └── security.py             # JWT, hashing
│
├── Models/
│   ├── __init__.py
│   └── [MODULO_1]/
│       ├── __init__.py
│       └── [modelo_name.py]    # Modelos SQLAlchemy
│
├── Schemas/
│   ├── __init__.py
│   └── [MODULO_1]/
│       ├── __init__.py
│       └── [schema_name.py]    # Schemas Pydantic
│
├── Routers/
│   ├── __init__.py
│   ├── auth_router.py
│   └── [MODULO_1]/
│       ├── __init__.py
│       └── [router_name.py]    # Endpoints
│
├── Services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── [MODULO_1]/
│       ├── __init__.py
│       └── [service_name.py]   # Lógica negocio
│
├── Scripts/
│   ├── Documentacion/
│   │   ├── Docker/
│   │   ├── Guias/
│   │   └── README.md
│   └── Configuracion/
│       ├── ESTRUCTURA_BASE_APLICATIVO.md
│       └── TEMPLATE_CONFIGURACION.md
│
├── Docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── .dockerignore
│   └── nginx.conf (opcional)
│
├── .github/
│   └── workflows/
│       └── docker-ci-cd.yml
│
└── tests/
    ├── unit/
    ├── integration/
    └── conftest.py
```

---

## 4. Archivos Base a Crear

### 4.1 Config/config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = os.getenv("APP_NAME", "[TU_APP_NAME]")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
```

### 4.2 Config/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from Config.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development"
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.3 Core/security.py

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from Config.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

### 4.4 main.py

```python
from fastapi import FastAPI
from Config.database import Base, engine
from Routers import auth_router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="[TU_APP_NAME]",
    version="1.0.0"
)

# Incluir routers
app.include_router(auth_router.router)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "API is running"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
```

### 4.5 .env.template

```env
# App
APP_NAME=[TU_APP_NAME]
APP_VERSION=1.0.0
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

# Database
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=tu_app_db
MYSQL_USER=tu_app_user
MYSQL_PASSWORD=tu_app_password
DATABASE_URL=mysql+pymysql://tu_app_user:tu_app_password@db:3306/tu_app_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4.6 Dockerfile

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.7 docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: tu_app_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-rootpassword}
      MYSQL_DATABASE: ${MYSQL_DATABASE:-tu_app_db}
      MYSQL_USER: ${MYSQL_USER:-tu_app_user}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-tu_app_password}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - tu_app_network

  app:
    build: .
    container_name: tu_app
    restart: always
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: ${DATABASE_URL:-mysql+pymysql://tu_app_user:tu_app_password@db:3306/tu_app_db}
      SECRET_KEY: ${SECRET_KEY:-your-secret-key}
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    networks:
      - tu_app_network

volumes:
  mysql_data:
    driver: local

networks:
  tu_app_network:
    driver: bridge
```

---

## 5. Modelos Base

### Ejemplo: Usuario

```python
# Models/users/user_model.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from Config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 6. Esquemas Base

### Ejemplo: Usuario

```python
# Schemas/users/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
```

---

## 7. Rutas Base

### Ejemplo: Autenticación

```python
# Routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Schemas.users.user_schema import UserCreate, UserResponse
from Services.user_service import create_user, get_user_by_username

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario existe")
    return create_user(db, user)
```

---

## 8. Servicios Base

### Ejemplo: Usuario

```python
# Services/user_service.py
from sqlalchemy.orm import Session
from Models.users.user_model import User
from Core.security import get_password_hash

def create_user(db: Session, user):
    hashed = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
```

---

## 9. Variables de Entorno

Crear archivo `.env`:

```bash
cp .env.template .env
# Editar .env con valores locales
```

Generar SECRET_KEY seguro:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 10. Ejecución

### Desarrollo

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con reload
uvicorn main:app --reload

# O con Docker
docker-compose up
```

### Producción

```bash
# Con Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# O con Docker
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## 11. Testing

### Estructura

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── test_user_service.py
│   └── test_auth.py
└── integration/
    ├── test_user_routes.py
    └── test_auth_routes.py
```

### conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)
```

### Ejecutar

```bash
pytest
pytest -v
pytest --cov=Services
```

---

## 12. Documentación

Crear estructura similar:

```
Scripts/
├── Documentacion/
│   ├── Docker/
│   │   ├── DOCKER_QUICKSTART.md
│   │   ├── DOCKER_SETUP.md
│   │   ├── DOCKER_CONFIGS.md
│   │   └── README.md
│   │
│   ├── Guias/
│   │   ├── PROCEDIMIENTOS.md
│   │   ├── TROUBLESHOOTING.md
│   │   ├── OPERACIONES_DIARIAS.md
│   │   └── BACKUP_Y_RECUPERACION.md
│   │
│   └── README.md
│
└── Configuracion/
    ├── ESTRUCTURA_BASE_APLICATIVO.md
    └── TEMPLATE_CONFIGURACION.md
```

---

## 13. Git Setup

```bash
# Inicializar repo
git init
echo ".env" >> .gitignore
echo "env/" >> .gitignore
echo "__pycache__/" >> .gitignore

git add .
git commit -m "Initial commit: FastAPI application setup"
```

---

## 14. Checklist Final

- [ ] Estructura de directorios creada
- [ ] Archivos base creados
- [ ] .env configurado
- [ ] requirements.txt actualizado
- [ ] Docker funcionando
- [ ] `http://localhost:8000/docs` accesible
- [ ] Health check en `/health` respondiendo
- [ ] Código en git
- [ ] Documentación base en Scripts/
- [ ] Primeros modelos y rutas implementados

---

## 📞 Próximos Pasos

1. **Añadir Modelos:** Crear modelos específicos según negocio
2. **Crear Servicios:** Lógica de negocio para cada módulo
3. **Definir Routers:** Endpoints según requerimientos
4. **Testing:** Escribir tests unitarios e integración
5. **Documentación:** Completar documentación técnica
6. **Despliegue:** Configurar para producción

---

**Última actualización:** 2024-04-16
**Versión Template:** 1.0
