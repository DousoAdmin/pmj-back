# 🔧 Troubleshooting - Solución de Problemas

Soluciones a problemas comunes en Docker y la aplicación.

## 🚫 Errores Comunes

### 1. "Connection refused" a la BD

**Síntoma:** Error de conexión a MySQL desde la app

**Causa:** BD no está lista o no hay conectividad

**Solución:**
```bash
# Ver logs de BD
docker-compose logs db

# Verificar que BD está healthy
docker-compose ps

# Reconectar
docker-compose down
docker-compose up -d

# Esperar 30 segundos
# Verificar
docker-compose logs app
```

### 2. "Port already in use"

**Síntoma:** Error "port 8000 already in use"

**Causa:** Otro proceso usa el puerto

**Solución - Windows:**
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar proceso (reemplazar PID)
taskkill /PID <PID> /F

# O cambiar puerto en docker-compose.yml
# ports:
#   - "8001:8000"  # cambiar 8000 a 8001
```

**Solución - Linux/Mac:**
```bash
# Ver qué usa el puerto
lsof -i :8000

# Matar proceso
kill -9 <PID>
```

### 3. "No space left on device"

**Síntoma:** Error de espacio disco

**Causa:** Disco lleno o volúmenes grandes

**Solución:**
```bash
# Ver uso de Docker
docker system df

# Limpiar imágenes no usadas
docker image prune -a

# Limpiar contenedores no usados
docker container prune

# Limpiar volúmenes no usados
docker volume prune

# Limpiar todo
docker system prune -a --volumes
```

### 4. "Permission denied"

**Síntoma:** Error de permisos en arch Linux/Mac

**Causa:** Problemas de propiedad de archivos

**Solución - Linux:**
```bash
# Cambiar propiedad
sudo chown -R 1000:1000 .

# O usar volumen anónimo
docker-compose down -v
docker-compose up -d
```

### 5. La app no inicia

**Síntoma:** El contenedor se crea pero se detiene

**Causa:** Error en el código o variables de entorno

**Solución:**
```bash
# Ver logs detallados
docker-compose logs app

# Buscar "Traceback" o "Error"
docker-compose logs app | grep -i error

# Ejecutar imagen manualmente
docker run -it pmj-backend:latest bash

# Dentro del contenedor
python main.py
```

### 6. "SQLALCHEMY_DATABASE_URL not found"

**Síntoma:** Error de variable de entorno

**Causa:** `.env` no existe o no está configurada

**Solución:**
```bash
# Crear .env
cp .env.docker .env

# Editar .env
nano .env

# Verificar
cat .env

# Reiniciar
docker-compose up -d --build
```

### 7. MySQL no persiste datos

**Síntoma:** Los datos desaparecen al reiniciar

**Causa:** Volumen no configurado

**Solución:**
```bash
# Verificar docker-compose.yml tiene:
# volumes:
#   mysql_data:
#     driver: local

# Ver volúmenes
docker volume ls

# Verificar volumen
docker volume inspect pmj_mysql_data

# NO hacer:
docker-compose down -v
```

### 8. Imágenes muy grandes

**Síntoma:** Imagen Docker > 500MB

**Causa:** Dockerfile ineficiente

**Solución:**
```bash
# Ver tamaño
docker images | grep pmj

# Analizar capas
docker history pmj-backend:latest

# Usar multi-stage build (ya está en Dockerfile)
docker build -t pmj-backend:latest .
```

## 📊 Comandos de Diagnóstico

```bash
# Verificar estado completo
docker-compose ps
docker-compose logs

# Recursos en uso
docker stats

# Información de imagen
docker inspect pmj_app

# Verificar red
docker network inspect pmj_network

# Verificar volúmenes
docker volume inspect pmj_mysql_data
```

## 🔍 Debug Avanzado

### Conectar debugger

```bash
# 1. Instalar debugpy
pip install debugpy

# 2. Agregar a main.py después de imports:
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()

# 3. Mapear puerto
# docker-compose.yml:
# ports:
#   - "5678:5678"

# 4. Iniciar VS Code debugger
```

### Ver requests/responses

```bash
# Activar logging en main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# O usar middleware
from fastapi import Request
from fastapi.middleware import Middleware
```

### Verificar BD directamente

```bash
# Acceder a MySQL
docker-compose exec db mysql -u pmj_user -p pmj_db

# Comandos útiles
SHOW TABLES;
DESC users;
SELECT COUNT(*) FROM users;
SHOW CREATE TABLE users;
```

## 🆘 Cuando Nada Funcione

```bash
# 1. Backup de datos (si es importante)
docker-compose exec db mysqldump -u pmj_user -p pmj_db > backup.sql

# 2. Reset total
docker-compose down -v

# 3. Limpiar sistema
docker system prune -a --volumes

# 4. Empezar de nuevo
docker-compose up -d --build

# 5. Verificar logs
docker-compose logs -f
```

## 📋 Checklist de Troubleshooting

- [ ] ¿Docker está corriendo? (`docker stats`)
- [ ] ¿Datos .env existen? (`ls -la .env`)
- [ ] ¿Puertos están libres? (`netstat` o `lsof`)
- [ ] ¿BD está healthy? (`docker-compose ps`)
- [ ] ¿Hay logs de error? (`docker-compose logs`)
- [ ] ¿Es problema de código? (`git status`, `git diff`)
- [ ] ¿Espacio en disco? (`docker system df`)
