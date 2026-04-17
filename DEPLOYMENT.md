# 🚀 Guía de Despliegue a Producción

Este documento describe cómo desplegar PMJ Backend en producción usando Docker.

## Opciones de Despliegue

### 1. Servidor Linux Independiente

#### Preparación del servidor

```bash
# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER
newgrp docker
```

#### Desplegar la aplicación

```bash
# Clonar repositorio
git clone <tu-repo> /opt/pmj-backend
cd /opt/pmj-backend

# Crear .env con valores de producción
cp .env.docker .env
nano .env  # Editar con valores reales

# Iniciar servicios
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verificar estados
docker-compose ps
```

### 2. Con Nginx (Reverse Proxy)

Recomendado para producción pública:

```bash
# Usar configuración con Nginx
docker-compose -f docker-compose.yml \
               -f docker-compose.prod.yml \
               -f docker-compose.nginx.yml \
               up -d

# Nginx estará en puerto 80
# Configurar dominio y SSL según sea necesario
```

### 3. Plataformas en la Nube

#### AWS ECS

1. Crear repositorio ECR
2. Construir y pushear imagen
3. Crear cluster ECS
4. Definir task definition
5. Crear servicio

```bash
# Ejemplo básico
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t pmj-backend:latest .
docker tag pmj-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pmj-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pmj-backend:latest
```

#### Google Cloud Run

```bash
# Configurar gcloud
gcloud config set project <proyecto-id>

# Construir imagen
gcloud builds submit --tag gcr.io/<proyecto-id>/pmj-backend

# Desplegar
gcloud run deploy pmj-backend \
    --image gcr.io/<proyecto-id>/pmj-backend \
    --platform managed \
    --region us-central1 \
    --set-env-vars DATABASE_URL=mysql+pymysql://user:pass@cloud-sql-ip/db
```

#### DigitalOcean App Platform

1. Conectar repositorio GitHub
2. Configurar build y despliegue automático
3. Configurar variables de entorno
4. Agregar base de datos MySQL

#### Heroku

```bash
# Alternativa: usar Procfile con gunicorn
echo "web: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:\$PORT" > Procfile

heroku create pmj-backend
heroku addons:create cleardb:ignite
git push heroku main
```

### 4. Docker Swarm (para múltiples nodos)

```bash
# Inicializar swarm
docker swarm init

# Crear servicio
docker service create \
    --name pmj-backend \
    --replicas 3 \
    --port 8000:8000 \
    pmj-backend:latest
```

### 5. Kubernetes

Crear manifiestos `kubernetes/`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pmj-backend
spec:
  selector:
    app: pmj-backend
  ports:
    - port: 8000
      targetPort: 8000
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pmj-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pmj-backend
  template:
    metadata:
      labels:
        app: pmj-backend
    spec:
      containers:
      - name: pmj-backend
        image: pmj-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: pmj-secrets
              key: database-url
```

Desplegar:
```bash
kubectl apply -f kubernetes/
```

## ✅ Checklist Pre-Producción

- [ ] Cambiar `SECRET_KEY` a valor único y fuerte
- [ ] Actualizar todas las contraseñas de BD
- [ ] Configurar HTTPS/SSL (Let's Encrypt)
- [ ] Usar variables de entorno para secretos
- [ ] Crear backups automáticos de BD
- [ ] Configurar logs centralizados (ELK, Datadog, etc)
- [ ] Configurar monitoreo y alertas
- [ ] Realizar pruebas de carga
- [ ] Documentar proceso de rollback
- [ ] Configurar CI/CD (GitHub Actions, GitLab CI)

## 🔐 Seguridad

### Generar SECRET_KEY seguro

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### Actualizar .env con valores seguros

```bash
# Nunca versionar .env en Git
echo ".env" >> .gitignore

# Usar gestores de secretos:
# - AWS Secrets Manager
# - HashiCorp Vault
# - Azure Key Vault
# - 1Password
```

### Configurar HTTPS

Con certbot (Let's Encrypt):

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Actualizar nginx.conf con rutas del certificado
# Renovación automática:
sudo certbot renew --dry-run
```

## 📊 Monitoreo

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs específicos de la app
docker-compose logs -f app

# Logs persistentes a archivo
docker-compose logs > logs-$(date +%Y%m%d-%H%M%S).txt
```

### Métricas

```bash
# Ver recursos en uso
docker stats

# Instalar Prometheus + Grafana para monitoreo avanzado
docker-compose up -d prometheus grafana
```

## 🔄 Backups Automatizados

```bash
#!/bin/bash
# backup.sh - Script de backup automático

BACKUP_DIR="/backups/pmj"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio
mkdir -p $BACKUP_DIR

# Backup de BD
docker-compose exec -T db mysqldump -u pmj_user -p${MYSQL_PASSWORD} pmj_db | \
    gzip > $BACKUP_DIR/pmj_db_$DATE.sql.gz

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_DIR/pmj_db_$DATE.sql.gz"
```

Programar con cron:
```bash
# Backup diario a las 2 AM
0 2 * * * /opt/pmj-backend/backup.sh
```

## 🚨 Troubleshooting

### La app no inicia

```bash
# Ver logs
docker-compose logs app

# Verificar conexión a BD
docker-compose exec app python -c "from Config.database import engine; print(engine)"
```

### Problemas de memoria

```bash
# Aumentar recursos en docker-compose.prod.yml
deploy:
  resources:
    limits:
      memory: 1G

docker-compose up -d --build
```

### BD no accesible

```bash
# Verificar red
docker network inspect pmj_network

# Reconectar
docker-compose down
docker-compose up -d --build
```

## 📚 Referencias

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🆘 Soporte Técnico

Para asistencia:
1. Revisar logs: `docker-compose logs -f`
2. Consultar [DOCKER_SETUP.md](DOCKER_SETUP.md)
3. Verificar status: `docker-compose ps`
4. Documentar el problema con logs
