@echo off
REM Script de inicio rápido para Docker en Windows

echo 🐳 PMJ Backend - Docker Setup
echo ==============================

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado. Por favor instálalo desde https://www.docker.com
    exit /b 1
)

REM Verificar si Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose no está instalado.
    exit /b 1
)

echo ✓ Docker y Docker Compose detectados

REM Crear .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env...
    copy .env.docker .env
    echo ⚠️  Edita .env y configura las variables de entorno
) else (
    echo ✓ Archivo .env ya existe
)

REM Construir y levantar servicios
echo.
echo 🏗️  Construyendo imagen y levantando servicios...
docker-compose up -d --build

echo.
echo ⏳ Esperando a que la base de datos esté lista...
timeout /t 10 /nobreak

echo.
echo ✅ Servicios iniciados:
echo    - Aplicación: http://localhost:8000
echo    - Docs API: http://localhost:8000/docs
echo    - Base de datos: localhost:3306
echo.
echo 📋 Comandos útiles:
echo    - Ver logs: docker-compose logs -f
echo    - Parar servicios: docker-compose down
echo    - Acceder a la app: docker-compose exec app bash
echo.
docker-compose ps
