# 📋 Procedimientos Comunes

Procedimientos paso a paso para operaciones habituales.

## 1. Iniciar la Aplicación

### Desarrollo Local
```bash
# Terminal 1: Iniciar servicios Docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# O en Windows
docker-start.bat

# O en Linux/Mac
./docker-start.sh
```

### Acceso
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- BD MySQL: localhost:3306

## 2. Actualizar Dependencias

```bash
# Ver paquetes instalados
pip list

# Instalar nuevos paquetes
pip install <nombre-paquete>

# Actualizar requirements.txt
pip freeze > requirements.txt

# Reconstruir imagen Docker
docker-compose up -d --build
```

## 3. Acceder a la Base de Datos

```bash
# Desde el contenedor
docker-compose exec db mysql -u pmj_user -p pmj_db

# O usar cliente local
mysql -h 127.0.0.1 -u pmj_user -p pmj_db

# Dentro de MySQL
SHOW TABLES;
SELECT * FROM users LIMIT 5;
```

## 4. Ejecutar Comandos en el Contenedor

```bash
# Bash interactivo
docker-compose exec app bash

# Ejecutar comando puntual
docker-compose exec app python -c "print('Hola')"

# Ver versión de Python
docker-compose exec app python --version

# Listar archivos
docker-compose exec app ls -la
```

## 5. Ver y Seguir Logs

```bash
# Últimas 100 líneas
docker-compose logs --tail=100

# Seguir en tiempo real
docker-compose logs -f

# Solo de la app
docker-compose logs -f app

# Solo de BD
docker-compose logs -f db

# Desde hace X minutos
docker-compose logs --since 10m
```

## 6. Restartear Servicios

```bash
# Reiniciar un servicio
docker-compose restart app
docker-compose restart db

# Restart completo
docker-compose down
docker-compose up -d

# Con rebuild
docker-compose up -d --build
```

## 7. Parar y Limpiar

```bash
# Parar servicios (mantiene volúmenes)
docker-compose down

# Parar y borrar datos BD (cuidado)
docker-compose down -v

# Limpiar todo
docker system prune -a --volumes
```

## 8. Inspeccionar Contenedores

```bash
# Ver estado
docker-compose ps

# Información detallada
docker inspect pmj_app

# Ver redes
docker network inspect pmj_network

# Ver volúmenes
docker volume ls
```

## 9. Generar SECRET_KEY

```bash
# Método 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Método 2: OpenSSL
openssl rand -base64 32
```

## 10. Cambiar Configuración

```bash
# 1. Editar .env
nano .env

# 2. Reiniciar servicios
docker-compose restart app

# O reconstruir
docker-compose up -d --build
```

## 11. Hacer Commit de Cambios

```bash
# Ver estado
git status

# Añadir cambios
git add .

# Commit
git commit -m "descripción del cambio"

# Push
git push origin main
```

## 12. Debugging

```bash
# Logs completos
docker-compose logs -f

# Estado de recursos
docker stats

# Conectarse a app
docker-compose exec app bash
python -c "import sys; print(sys.path)"

# Probar conectividad BD
docker-compose exec app python
>>> from Config.database import engine
>>> print(engine)
```

## Comandos Rápidos

| Tarea | Comando |
|-------|---------|
| Iniciar | `docker-compose up -d` |
| Parar | `docker-compose down` |
| Logs | `docker-compose logs -f` |
| Bash en app | `docker-compose exec app bash` |
| Logs de app | `docker-compose logs -f app` |
| Ver BD | `docker-compose exec db mysql -u pmj_user -p pmj_db` |
| Restart | `docker-compose restart app` |
| Rebuild | `docker-compose up -d --build` |
| Estado | `docker-compose ps` |
| Limpiar | `docker system prune -a --volumes` |
