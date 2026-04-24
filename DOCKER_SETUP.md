# 🐳 Guía de Docker para PMJ Backend

Este documento describe cómo usar Docker para desplegar la aplicación PMJ Backend.

## Requisitos Previos

- [Docker](https://www.docker.com/products/docker-desktop) instalado (versión 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (versión 1.29+)

## Estructura de Archivos Docker

```
├── Dockerfile                 # Imagen de la aplicación FastAPI
├── docker-compose.yml         # Orquestación de servicios (producción)
├── docker-compose.dev.yml     # Configuración adicional para desarrollo
├── .dockerignore               # Archivos excluidos de la imagen
├── .env.docker                # Variables de entorno de ejemplo
└── DOCKER_SETUP.md            # Este archivo
```

## Configuración Rápida

### 1. Preparar Variables de Entorno

Copia el archivo `.env.docker` a `.env`:

```bash
cp .env.docker .env
```

Edita `.env` y ajusta la configuración según tu entorno (especialmente `SECRET_KEY` y contraseñas en producción).

### 2. Construcción de la Imagen (Opcional)

Docker Compose construye automáticamente la imagen, pero puedes hacerlo manualmente:

```bash
docker build -t pmj-backend:latest .
```

## Uso

### Iniciar Servicios (Producción)

```bash
# Descarga imágenes y crea servicios en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver solo logs de la app
docker-compose logs -f app

# Ver solo logs de la base de datos
docker-compose logs -f db
```

### Iniciar Servicios (Desarrollo con Hot-Reload)

```bash
# Usar configuración de desarrollo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Con logs en tiempo real
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
docker-compose logs -f app
```

### Detener Servicios

```bash
docker-compose down

# Detener y remover volúmenes (cuidado: pierde datos de la BD)
docker-compose down -v
```

### Recrear Servicios

```bash
# Reconstruir imagen y reiniciar
docker-compose up -d --build
```

## Acceso a los Servicios

### Aplicación FastAPI
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base de Datos MySQL
- **Host**: `localhost` o `db` (desde dentro del contenedor)
- **Puerto**: `3306`
- **Usuario**: `pmj_user` (configurado en `.env`)
- **Contraseña**: `pmj_password` (configurado en `.env`)
- **Base de Datos**: `pmj_db`

Conexión desde host local:
```bash
mysql -h 127.0.0.1 -u pmj_user -p pmj_db
```

Conexión desde dentro de Docker:
```bash
docker-compose exec db mysql -u pmj_user -p pmj_db
```

## Comandos Útiles

### Ejecutar Comandos en Contenedores

```bash
# Acceder a la shell de la aplicación
docker-compose exec app bash

# Ejecutar comando Python
docker-compose exec app python -c "import sys; print(sys.version)"

# Acceder a MySQL CLI
docker-compose exec db mysql -u pmj_user -p pmj_db

# Ver procesos en contenedor
docker-compose exec app ps aux
```

### Gestión de Base de Datos

```bash
# Ejecutar script SQL
docker-compose exec db mysql -u pmj_user -p pmj_db < database_update_typedocumentspersons.sql

# Hacer dump de la base de datos
docker-compose exec db mysqldump -u pmj_user -p pmj_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker-compose exec -T db mysql -u pmj_user -p pmj_db < backup_20240416.sql
```

### Limpieza

```bash
# Ver imágenes Docker
docker images | grep pmj

# Remover imagen
docker rmi pmj-backend:latest

# Limpiar volúmenes no usados
docker volume prune

# Limpiar todo (contenedores, redes, volumes no usados)
docker system prune -a --volumes
```

## Monitoreo y Debugging

### Ver Estado de Servicios

```bash
# Estado de contenedores
docker-compose ps

# Estadísticas en tiempo real
docker stats
```

### Inspeccionar Contenedores

```bash
# Ver configuración del contenedor
docker inspect pmj_app

# Ver redes del contenedor
docker network inspect pmj_network
```

### Logs de Aplicación

```bash
# Últimas 100 líneas
docker-compose logs --tail=100 app

# Seguir logs en tiempo real
docker-compose logs -f app

# Logs desde hace 10 minutos
docker-compose logs --since 10m app
```

## Variables de Entorno Importantes

| Variable | Descripción | Valor Por Defecto |
|----------|-------------|-------------------|
| `MYSQL_ROOT_PASSWORD` | Contraseña root de MySQL | `rootpassword` |
| `MYSQL_DATABASE` | Nombre de la base de datos | `pmj_db` |
| `MYSQL_USER` | Usuario de MySQL | `pmj_user` |
| `MYSQL_PASSWORD` | Contraseña del usuario | `pmj_password` |
| `DATABASE_URL` | URL de conexión | `mysql+pymysql://pmj_user:pmj_password@db:3306/pmj_db` |
| `APP_ENV` | Entorno (development/production) | `production` |
| `SECRET_KEY` | Clave secreta JWT | Generar nueva en producción |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token | `30` |

## Seguridad en Producción

Antes de desplegar a producción:

1. **Cambiar todas las contraseñas y claves**:
   ```bash
   # Generar SECRET_KEY seguro
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Usar variables de entorno seguras**:
   - No versionar `.env` en Git
   - Usar gestores de secretos (AWS Secrets Manager, Azure Key Vault, etc.)

3. **Configurar HTTPS/TLS**:
   - Usar reverse proxy (Nginx, Traefik)
   - Obtener certificados SSL (Let's Encrypt)

4. **Limitar acceso a puertos**:
   - No exponer puerto 3306 de MySQL en producción
   - Usar firewall para restringir acceso a 8000

5. **Actualizar imagen base**:
   ```bash
   docker pull python:3.11-slim
   ```

## Troubleshooting

### "Connection refused" en la app

```bash
# Verificar que la BD está lista
docker-compose logs db

# Verificar conectividad entre contenedores
docker-compose exec app ping db
```

### Puerto ya en uso

```bash
# Cambiar puertos en docker-compose.yml
# O liberar el puerto:
lsof -i :8000  # En Linux/Mac
netstat -ano | findstr :8000  # En Windows
```

### Perdida de datos de la BD

```bash
# Crear volumen permanente (ya está en docker-compose.yml)
volumes:
  mysql_data:
```

### Errores de permisos en volúmenes

```bash
# Cambiar propiedad en Linux
sudo chown -R 1000:1000 .

# O usar volumen anónimo en docker-compose.yml
```

## Referencias

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MySQL Docker Hub](https://hub.docker.com/_/mysql)

## Soporte

Para problemas o preguntas, revisa los logs:

```bash
docker-compose logs -f
```

O consulta la documentación oficial de Docker y FastAPI.
