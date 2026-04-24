@echo off
REM Script para ejecutar Docker con MySQL en XAMPP
REM Requiere que XAMPP MySQL esté corriendo

title PMJ Backend - Docker Development
cls

echo.
echo ================================
echo  PMJ Backend - Docker Development
echo ================================
echo.

REM Verificar que Docker esté corriendo
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no está instalado o no está corriendo
    echo Abre Docker Desktop y vuelve a intentar
    pause
    exit /b 1
)

echo [1/3] Verificando que XAMPP MySQL esté disponible en puerto 3306...
echo.

echo [2/3] Limpiando contenedores anteriores...
docker-compose down --remove-orphans

echo.
echo [3/3] Construyendo e iniciando servicios...
echo.
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

echo.
echo La aplicación debería estar disponible en: http://localhost:8000
echo Documentación en: http://localhost:8000/docs
echo.

pause

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
