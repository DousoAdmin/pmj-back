# 🏗️ Estructura Base del Aplicativo - PMJ Backend

Documento descriptor de la estructura, configuración y componentes base de la aplicación PMJ Backend.
Use este documento como **template** para crear aplicaciones similares.

---

## 📋 Resumen Ejecutivo

| Aspecto | Detalle |
|--------|---------|
| **Nombre Aplicación** | Plataforma Modular para Justicia (PMJ) Backend |
| **Framework** | FastAPI 0.116.1 |
| **Lenguaje** | Python 3.11 |
| **Base de Datos** | MySQL 8.0 |
| **ORM** | SQLAlchemy 2.0.43 |
| **Autenticación** | JWT (python-jose) |
| **Servidor** | Uvicorn + Gunicorn (producción) |
| **Containerización** | Docker + Docker Compose |
| **Despliegue** | Docker, Kubernetes, Cloud (AWS/GCP) |

---

## 🏛️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                         Cliente (Frontend)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                    │
│              (Opcional - Producción)                         │
├─────────────────────────────────────────────────────────────┤
│ - SSL/TLS Termination                                       │
│ - Load Balancing                                            │
│ - Static Files                                              │
│ - Security Headers                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Application                        │
│                      (Uvicorn)                              │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────┐   │
│ │             Routers & Endpoints                      │   │
│ │  ├─ Auth Router       (/auth)                        │   │
│ │  ├─ User Router       (/users)                       │   │
│ │  ├─ Org Router        (/organizations)              │   │
│ │  └─ Persons Router    (/persons)                    │   │
│ └──────────────────────────────────────────────────────┘   │
│ ┌──────────────────────────────────────────────────────┐   │
│ │             Services (Business Logic)                │   │
│ │  ├─ Auth Service                                     │   │
│ │  ├─ User Service                                     │   │
│ │  ├─ Organization Services                           │   │
│ │  └─ Persons Services                                │   │
│ └──────────────────────────────────────────────────────┘   │
│ ┌──────────────────────────────────────────────────────┐   │
│ │             Schemas (Validation)                     │   │
│ │  └─ Pydantic Models                                  │   │
│ └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  SQLAlchemy ORM                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Models (declarative_base)                          │  │
│  │  ├─ Users, Roles, Permissions                       │  │
│  │  ├─ Organizations, Document Types                   │  │
│  │  └─ Persons, Documents, Status                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   MySQL Database                           │
│  ├─ User Management                                        │
│  ├─ Organization Data                                      │
│  ├─ Person Information                                     │
│  └─ Business Data                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
pmj-back/
│
├── 📄 main.py                          # Punto de entrada
├── 📄 requirements.txt                 # Dependencias Python
├── .env.docker                         # Template de variables
├── 📄 README.md                        # Documentación principal
│
├── 🗂️ Config/                          # Configuración
│   ├── __init__.py
│   ├── config.py                       # Settings (dotenv)
│   └── database.py                     # Conexión SQLAlchemy
│
├── 🗂️ Core/                            # Lógica central
│   ├── __init__.py
│   └── security.py                     # JWT, hashing, etc
│
├── 🗂️ Models/                          # Modelos SQLAlchemy
│   ├── users/                          # Modelos de usuarios
│   │   ├── userModel.py
│   │   ├── rolesModel.py
│   │   ├── permissionsModel.py
│   │   └── ...
│   │
│   ├── organizations/                 # Modelos de organizaciones
│   │   ├── organizations_model.py
│   │   ├── organization_type_model.py
│   │   └── ...
│   │
│   └── persons/                        # Modelos de personas
│       ├── personsModel.py
│       ├── documentsModel.py
│       └── ...
│
├── 🗂️ Schemas/                         # Esquemas Pydantic
│   ├── user_schema.py
│   ├── userShemas/
│   │   └── ...
│   ├── organizationSchema/
│   │   └── ...
│   └── personsSchemas/
│       └── ...
│
├── 🗂️ Routers/                         # Endpoints FastAPI
│   ├── auth_router.py
│   ├── user_router.py
│   │
│   ├── organizationsRouters/
│   │   ├── organization_router.py
│   │   ├── organization_type_router.py
│   │   └── ...
│   │
│   ├── personsRouters/
│   │   ├── persons_router.py
│   │   ├── documents_router.py
│   │   └── ...
│   │
│   └── usersRouters/
│       └── user_router.py
│
├── 🗂️ Services/                        # Lógica de negocio
│   ├── auth_service.py
│   ├── user_service.py
│   │
│   ├── OrganizationServices/
│   │   ├── organization_service.py
│   │   ├── approaches_service.py
│   │   └── ...
│   │
│   ├── personsServices/
│   │   ├── persons_service.py
│   │   ├── documents_service.py
│   │   └── ...
│   │
│   └── userServices/
│       └── ...
│
├── 🗂️ Scripts/                         # Scripts y documentación
│   ├── Documentacion/
│   │   ├── Docker/
│   │   │   ├── DOCKER_CONFIGS.md
│   │   │   └── README.md
│   │   │
│   │   ├── Guias/
│   │   │   ├── PROCEDIMIENTOS.md
│   │   │   ├── TROUBLESHOOTING.md
│   │   │   ├── OPERACIONES_DIARIAS.md
│   │   │   └── BACKUP_Y_RECUPERACION.md
│   │   │
│   │   └── README.md
│   │
│   ├── Configuracion/
│   │   ├── ESTRUCTURA_BASE_APLICATIVO.md (este archivo)
│   │   └── TEMPLATE_CONFIGURACION.md
│   │
│   ├── docker-start.bat
│   ├── docker-start.sh
│   ├── docker-stop.bat
│   └── docker-stop.sh
│
├── 🐳 Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── docker-compose.nginx.yml
│   ├── .dockerignore
│   └── nginx.conf
│
├── 🔧 CI/CD
│   ├── .github/
│   │   └── workflows/
│   │       └── docker-ci-cd.yml
│   │
│   └── .gitignore
│
└── env/                                # Virtual environment (local)
    └── ...
```

---

## 🔌 Stack Tecnológico

### Backend
```python
# main.py
- FastAPI 0.116.1          → Framework web
- Uvicorn 0.35.0           → Servidor ASGI
- Gunicorn 21.2.0          → WSGI HTTP Server (producción)
- Pydantic 2.11.7          → Validación de datos
- SQLAlchemy 2.0.43        → ORM para BD
- PyMySQL 1.1.2            → Driver MySQL
```

### Autenticación & Seguridad
```python
- python-jose 3.5.0        → JWT tokens
- passlib 1.7.4            → Hashing de contraseñas
- bcrypt 4.3.0             → Algoritmo de hash
- python-multipart 0.0.20  → Form parsing
```

### Utilidades
```python
- python-dotenv 1.1.1      → Manejo de variables .env
- Alembic 1.16.5           → Migraciones de BD (opcional)
- email-validator 2.3.0    → Validación de email
- Mako 1.3.10              → Template engine
```

### Database
```
- MySQL 8.0                → Base de datos relacional
```

### Containerización
```
- Docker                   → Containerización
- Docker Compose           → Orquestación multi-contenedor
- Nginx                    → Reverse proxy (opcional)
```

---

## 🔐 Seguridad

### Autenticación
```python
# Core/security.py
- Hash de contraseñas: bcrypt (passlib)
- Tokens JWT: python-jose (HS256)
- Expiración de tokens: configurable
```

### Base de Datos
```python
# Config/database.py
- Engine: SQLAlchemy
- URL: MySQL+PyMySQL
- Pool de conexiones: automático
- Echo (SQL logging): configurable
```

### Validación
```python
# Schemas/
- Modelos Pydantic
- Validación de tipos
- Restricciones de datos
```

---

## 🚀 Flujo de Operación

### 1. Inicio de Aplicación

```python
# main.py
1. Carga variables de .env (Config.py)
2. Importa todos los modelos (para relaciones SQLAlchemy)
3. Crea tablas en BD (Base.metadata.create_all)
4. Inicializa rutas (routers)
5. Inicia servidor Uvicorn en puerto 8000
```

### 2. Request Lifecycle

```
Cliente HTTP Request
        ↓
   Nginx (si existe)
        ↓
   Uvicorn Router
        ↓
   Endpoint (FastAPI)
        ↓
   Validación (Pydantic Schema)
        ↓
   Service (Lógica de negocio)
        ↓
   Repository (Model + SQLAlchemy)
        ↓
   MySQL Query
        ↓
   Response JSON
```

### 3. Autenticación

```
1. POST /auth/login
2. Verificar usuario + contraseña
3. Generar JWT token
4. Retornar token

5. Subsecuentes requests
6. Header: Authorization: Bearer <token>
7. Validar token (Core/security.py)
8. Obtener usuario actual
9. Proceder si es válido
```

---

## 🗄️ Modelo de Base de Datos Base

### Tablas Principales

```sql
-- Users
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    state_id INT,
    created_at TIMESTAMP
);

-- Roles
CREATE TABLE roles (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(100),
    description TEXT
);

-- Permissions
CREATE TABLE permissions (
    permissions_id INT PRIMARY KEY,
    permissions_name VARCHAR(100),
    description TEXT
);

-- Organizations
CREATE TABLE organizations (
    organization_id INT PRIMARY KEY,
    organization_name VARCHAR(200),
    organization_type_id INT,
    created_at TIMESTAMP
);

-- Persons
CREATE TABLE persons (
    person_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    identity_document VARCHAR(50),
    created_at TIMESTAMP
);

-- Relaciones (N:M)
CREATE TABLE users_roles_organizations (
    user_id INT,
    role_id INT,
    organization_id INT,
    PRIMARY KEY (user_id, role_id, organization_id)
);
```

---

## ⚙️ Configuración Base

### Config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME = os.getenv("APP_NAME", "FastAPI App")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
```

### Database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from Config.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🔄 Patrones de Código

### Modelo SQLAlchemy

```python
# Models/users/userModel.py
from sqlalchemy import Column, Integer, String, DateTime
from Config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Schema Pydantic

```python
# Schemas/user_schema.py
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
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### Service

```python
# Services/user_service.py
from sqlalchemy.orm import Session
from Models.users.userModel import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, user_data):
    user_dict = user_data.dict()
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### Router

```python
# Routers/user_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.database import get_db
from Services.user_service import get_user_by_id
from Schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    return user
```

---

## 🐳 Configuración Docker

### Dockerfile (Multi-stage)

```dockerfile
FROM python:3.11-slim as builder
# ... instalar dependencias

FROM python:3.11-slim
# ... runtime
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: mysql+pymysql://user:pass@db:3306/pmj_db
  
  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: pmj_db
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---

## 📈 Escalabilidad

### Horizontal Scaling
```
- Docker Compose → Docker Swarm
- Docker Swarm → Kubernetes
- Contenedor único → Múltiples réplicas
```

### Vertical Scaling
```
- Aumentar CPU/RAM en docker-compose.prod.yml
- Aumentar workers de Gunicorn
- Aumentar pool de conexiones
```

### Base de Datos
```
- MySQL replicación
- Read replicas
- Sharding (si es necesario)
- Caching (Redis)
```

---

## 🧪 Testing

### Struktur Recomendada

```
tests/
├── unit/
│   ├── test_user_service.py
│   ├── test_organization_service.py
│   └── ...
│
├── integration/
│   ├── test_user_routes.py
│   ├── test_auth.py
│   └── ...
│
├── conftest.py
└── requirements-test.txt
```

### Ejecución

```bash
pytest tests/
pytest tests/ --cov=Services
pytest tests/integration/test_auth.py -v
```

---

## 📊 Monitoreo

### Métricas a Monitorear
```
- Uptime de aplicación
- Response time promedio
- Errores por minuto
- Conexiones activas a BD
- Uso de CPU/RAM
- Espacio en disco
```

### Herramientas Recomendadas
```
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog
- New Relic
```

---

## 🔗 Referencias

| Aspecto | Enlace |
|--------|--------|
| FastAPI Docs | https://fastapi.tiangolo.com/ |
| SQLAlchemy | https://www.sqlalchemy.org/ |
| Docker | https://docs.docker.com/ |
| MySQL | https://dev.mysql.com/doc/ |
| Pydantic | https://docs.pydantic.dev/ |
| JWT | https://tools.ietf.org/html/rfc7519 |

---

## ✨ Conclusión

Este documento describe la estructura base y patrones de la aplicación PMJ Backend.
Para crear aplicaciones similares:

1. Seguir la misma estructura de directorios
2. Adaptar modelos según necesidad
3. Reutilizar patrones de código
4. Usar template de Docker
5. Consultar la documentación en `Scripts/Documentacion/`
