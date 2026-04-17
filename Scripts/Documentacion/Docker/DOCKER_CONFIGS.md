# 🐳 Referencia de Configuración Docker

Referencia rápida de variables y configuraciones de Docker.

## 🔧 Variables de Entorno (.env)

```env
# App Info
APP_NAME=Plataforma Modular con FastAPI
APP_VERSION=1.0.0
APP_ENV=production                          # development | production

# Database
MYSQL_ROOT_PASSWORD=rootpassword123
MYSQL_DATABASE=pmj_db
MYSQL_USER=pmj_user
MYSQL_PASSWORD=pmj_password_secure
DATABASE_URL=mysql+pymysql://pmj_user:pmj_password_secure@db:3306/pmj_db

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ports
APP_PORT=8000
MYSQL_PORT=3306
```

## 📋 Dockerfile - Capas

```dockerfile
# Etapa 1: Builder
FROM python:3.11-slim as builder
├─ Instala dependencias sistema
├─ Copia requirements.txt
└─ Instala paquetes Python

# Etapa 2: Runtime
FROM python:3.11-slim
├─ Instala dependencias runtime solo
├─ Copia paquetes desde builder
└─ Copia aplicación
```

**Ventajas:**
- ✓ Imagen más pequeña (~200MB vs 600MB)
- ✓ Menos vulnerabilidades
- ✓ Startup más rápido

## 🐳 docker-compose.yml - Servicios

### Servicio: db (MySQL)

```yaml
db:
  image: mysql:8.0
  ports:
    - "3306:3306"
  environment:
    MYSQL_ROOT_PASSWORD: ...
    MYSQL_DATABASE: pmj_db
  volumes:
    - mysql_data:/var/lib/mysql
  healthcheck:
    test: ["CMD", "mysqladmin", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**Puertos:**
- Interno: `3306`
- Externo: `3306`

**Volúmenes:**
- `mysql_data` → Persiste datos de BD

**Health Check:**
- Verifica cada 10s
- Timeout: 5s
- Reintentos: 5

### Servicio: app (FastAPI)

```yaml
app:
  build: .
  ports:
    - "8000:8000"
  depends_on:
    db:
      condition: service_healthy
  volumes:
    - .:/app
  environment:
    DATABASE_URL: mysql+pymysql://pmj_user:...@db:3306/pmj_db
```

**Puertos:**
- Interno: `8000`
- Externo: `8000`

**Volúmenes:**
- `.:/app` → Desarrollo (hot-reload)
- Vacío en producción

**Dependencias:**
- Espera a que `db` esté healthy

## 🔗 Red de Contenedores

```
pmj_network (bridge)
├── pmj_app (puerto 8000)
├── pmj_mysql (puerto 3306)
└── pmj_nginx (puerto 80, 443) [opcional]
```

**Resolución de DNS:**
- Dentro de red: `db:3306`
- Desde host: `localhost:3306`

## 💾 Volúmenes

```
mysql_data/
├─ Datos de MySQL
├─ Persistor entre reincios
└─ Ubicación física: /var/lib/docker/volumes/pmj_mysql_data/_data/
```

## 📊 Archivos de Configuración

### docker-compose.yml
```yaml
# Configuración base
# Servicios: app, db
# Red: pmj_network
# Volúmenes: mysql_data
```

### docker-compose.dev.yml
```yaml
# Sobrescribe docker-compose.yml
# Hot-reload activo
# Volumen mount en desarrollo
# Logging verboso
```

### docker-compose.prod.yml
```yaml
# Sobrescribe docker-compose.yml
# Gunicorn (4 workers) en lugar de uvicorn
# Sin volúmenes
# Límites de recursos
# Reinicio automático
```

### docker-compose.nginx.yml
```yaml
# Opcional
# Agrega servicio nginx
# Reverse proxy
# Mapeo de puertos 80/443
```

## 🔐 Variables de Seguridad

| Variable | Valor | Notas |
|----------|-------|-------|
| `SECRET_KEY` | 32+ caracteres aleatorios | CAMBIAR en producción |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Duración de token |
| `MYSQL_PASSWORD` | Contraseña fuerte | CAMBIAR en producción |

**Generar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Comandos Rápidos

| Acción | Comando |
|--------|---------|
| Iniciar | `docker-compose up -d` |
| Parar | `docker-compose down` |
| Rebuild | `docker-compose up -d --build` |
| Logs | `docker-compose logs -f` |
| Estado | `docker-compose ps` |
| Desarrollo | `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up` |
| Producción | `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d` |

## 📈 Límites de Recursos

### Producción

```yaml
app:
  deploy:
    resources:
      limits:
        cpus: '1'          # 1 core máximo
        memory: 512M       # 512 MB máximo
      reservations:
        cpus: '0.5'        # 0.5 cores reservados
        memory: 256M       # 256 MB reservados
```

### Ajustar según tipo de servidor:

| Servidor | CPU | RAM |
|----------|-----|-----|
| Pequeño | 0.5-1 cores | 256-512 MB |
| Mediano | 2-4 cores | 1-2 GB |
| Grande | 4+ cores | 4+ GB |

## 🔄 Health Checks

### app

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 5s
```

### db

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
```

## 🌐 Nginx Reverse Proxy

```nginx
upstream app {
    server app:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📦 Imagen Docker

**Base:** `python:3.11-slim`
**Tamaño:** ~200 MB (multi-stage)
**Entrypoint:** `uvicorn main:app --host 0.0.0.0 --port 8000`
**Working Dir:** `/app`

## ✅ Pre-Producción Checklist

- [ ] `.env` creado y configurado
- [ ] `SECRET_KEY` único y fuerte
- [ ] Contraseñas de BD CAMBIADAS
- [ ] `APP_ENV=production`
- [ ] Volúmenes configurados
- [ ] Health checks funcionan
- [ ] Nginx configurado (si aplica)
- [ ] Backup automatizado
- [ ] Monitoreo activo
- [ ] Logs centralizados
