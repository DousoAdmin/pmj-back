# PMJ Backend

Backend de la Plataforma Modular para Justicia (PMJ) construida con FastAPI.

## 🚀 Inicio Rápido con Docker

### Requisitos
- Docker Desktop instalado
- Docker Compose 1.29+

### Pasos

**En Windows:**
```bash
docker-start.bat
```

**En Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

**O manualmente:**
```bash
cp .env.docker .env
docker-compose up -d --build
```

La aplicación estará disponible en: http://localhost:8000

## 📚 Documentación

- [Guía completa de Docker](DOCKER_SETUP.md) - Configuración, comandos y troubleshooting
- [API Documentation](http://localhost:8000/docs) - Swagger UI (cuando esté en ejecución)

## 🛠️ Desarrollo Local (Sin Docker)

```bash
# Crear entorno virtual
python -m venv env

# Activar entorno
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload
```

## 🐳 Comandos Docker Comunes

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Acceder a bash en la app
docker-compose exec app bash

# Acceder a MySQL
docker-compose exec db mysql -u pmj_user -p pmj_db
```

## 📊 Servicios

- **API FastAPI**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **MySQL Database**: localhost:3306

## 🔐 Variables de Entorno

Ver archivo [.env.docker](.env.docker) para variables disponibles. Copiar a `.env` y ajustar según necesidad.

## 📁 Estructura del Proyecto

```
├── Config/          - Configuración de app y BD
├── Core/            - Seguridad y lógica central
├── Models/          - Modelos SQLAlchemy
├── Routers/         - Rutas FastAPI
├── Schemas/         - Esquemas Pydantic
├── Services/        - Lógica de negocio
└── main.py          - Punto de entrada
```

## ✅ Características

- ✓ FastAPI con OpenAPI/Swagger
- ✓ SQLAlchemy ORM con MySQL
- ✓ Autenticación JWT
- ✓ Docker & Docker Compose listos
- ✓ Health checks
- ✓ Gestión de roles y permisos

## 📝 Licencia

Todos los derechos reservados.
