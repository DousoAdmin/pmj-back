# 💾 Backup y Recuperación

Procedimientos para backup automático y recuperación de datos.

## 📦 Backup de Base de Datos

### Backup Manual Rápido

```bash
# Dump básico
docker-compose exec db mysqldump -u pmj_user -p pmj_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Con compresión
docker-compose exec db mysqldump -u pmj_user -p pmj_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Todas las bases de datos
docker-compose exec db mysqldump -u pmj_user -p --all-databases | gzip > backup_completo_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Backup con Contraseña en Script

```bash
#!/bin/bash
# backup.sh

MYSQL_USER="pmj_user"
MYSQL_PASSWORD="pmj_password"
MYSQL_DB="pmj_db"
BACKUP_DIR="/backups/pmj"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Hacer backup
docker-compose exec -T db mysqldump \
  -u $MYSQL_USER \
  -p$MYSQL_PASSWORD \
  $MYSQL_DB | gzip > $BACKUP_DIR/pmj_db_$DATE.sql.gz

echo "✓ Backup realizado: $BACKUP_DIR/pmj_db_$DATE.sql.gz"

# Guardar en archivo de log
echo "$(date): Backup realizado en $BACKUP_DIR/pmj_db_$DATE.sql.gz" >> $BACKUP_DIR/backup.log

# Limpiar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "✓ Backups antiguos eliminados"
```

### Ejecutar Script

```bash
# Dar permisos
chmod +x backup.sh

# Ejecutar manualmente
./backup.sh

# Programar con cron
0 2 * * * /opt/pmj-backend/backup.sh
```

### Backup de Volumen (alternativa)

```bash
# Ver volúmenes
docker volume ls | grep pmj

# Backup de volumen
docker run --rm -v pmj_mysql_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql_data_$(date +%Y%m%d).tar.gz -C /data .

# Restaurar
docker run --rm -v pmj_mysql_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/mysql_data_20240416.tar.gz -C /data
```

## 🔄 Recuperación de Base de Datos

### Recuperación Rápida

```bash
# Tipo 1: Archivo sin comprimir
docker-compose exec -T db \
  mysql -u pmj_user -p pmj_db < backup_20240416.sql

# Tipo 2: Archivo comprimido
gunzip < backup_20240416.sql.gz | \
docker-compose exec -T db \
  mysql -u pmj_user -p pmj_db
```

### Recuperación Paso a Paso

```bash
# 1. Verificar que el backup existe
ls -lh backup_20240416.sql.gz

# 2. Ver primeras líneas
head -20 backup_20240416.sql.gz | zcat

# 3. Parar servicios (opcional)
docker-compose down

# 4. Iniciar solo BD
docker-compose up -d db

# 5. Esperar a que BD esté lista
sleep 30

# 6. Restaurar
gunzip < backup_20240416.sql.gz | \
docker-compose exec -T db \
  mysql -u pmj_user -p pmj_db

# 7. Verificar
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "SELECT COUNT(*) FROM users;"

# 8. Reiniciar todo
docker-compose up -d
```

## 📊 Backup de Configuración

### Backup de Archivos

```bash
#!/bin/bash
# backup_config.sh

BACKUP_DIR="/backups/pmj"
DATE=$(date +%Y%m%d_%H%M%S)

# Archivos importantes
tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
  .env \
  docker-compose.yml \
  docker-compose.prod.yml \
  Dockerfile \
  nginx.conf \
  --exclude="*.pyc" \
  --exclude="__pycache__" \
  --exclude=".git"

echo "✓ Configuración backup: $BACKUP_DIR/config_$DATE.tar.gz"

# Código fuente (sin venv)
tar -czf $BACKUP_DIR/codigo_$DATE.tar.gz \
  --exclude="venv" \
  --exclude="env" \
  --exclude=".git" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  .

echo "✓ Código backup: $BACKUP_DIR/codigo_$DATE.tar.gz"
```

### Restaurar Configuración

```bash
# Extraer en directorio nuevo
mkdir /tmp/pmj_restore
cd /tmp/pmj_restore
tar xzf config_20240416.tar.gz

# Copiar archivos importantes
cp .env /opt/pmj-backend/
cp docker-compose.yml /opt/pmj-backend/
```

## 🌐 Backup a Servicios en la Nube

### AWS S3

```bash
#!/bin/bash
# backup_s3.sh

AWS_BUCKET="s3://pmj-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup local
./backup.sh

# Subir a S3
aws s3 cp /backups/pmj/pmj_db_$DATE.sql.gz \
  $AWS_BUCKET/backups/pmj_db_$DATE.sql.gz

echo "✓ Backup subido a S3"

# Ver archivos en S3
aws s3 ls $AWS_BUCKET/backups/
```

### Google Cloud Storage

```bash
#!/bin/bash
# backup_gcs.sh

BUCKET="gs://pmj-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup local
./backup.sh

# Subir a GCS
gsutil cp /backups/pmj/pmj_db_$DATE.sql.gz \
  $BUCKET/backups/pmj_db_$DATE.sql.gz

gsutil ls $BUCKET/backups/
```

### OneDrive/Azure

```bash
#!/bin/bash
# backup_azure.sh

DATE=$(date +%Y%m%d_%H%M%S)

# Backup local
./backup.sh

# Copiar a OneDrive (via rclone)
rclone copy /backups/pmj/pmj_db_$DATE.sql.gz \
  onedrive:/PMJ-Backups/

echo "✓ Backup copiado a OneDrive"
```

## 🔐 Backup Encriptado

```bash
#!/bin/bash
# backup_encrypted.sh

BACKUP_DIR="/backups/pmj"
DATE=$(date +%Y%m%d_%H%M%S)
PASSPHRASE="your-secure-passphrase"

# Backup con encriptación GPG
docker-compose exec db mysqldump -u pmj_user -p pmj_db | \
  gzip | \
  gpg --symmetric --cipher-algo AES256 --passphrase "$PASSPHRASE" \
  > $BACKUP_DIR/pmj_db_$DATE.sql.gz.gpg

echo "✓ Backup encriptado: $BACKUP_DIR/pmj_db_$DATE.sql.gz.gpg"

# Restaurar
gpg --decrypt --passphrase "$PASSPHRASE" \
  $BACKUP_DIR/pmj_db_$DATE.sql.gz.gpg | \
  gunzip | \
  docker-compose exec -T db \
  mysql -u pmj_user -p pmj_db
```

## 📋 Estrategia de Backup Recomendada

### Diario
```bash
# 2 AM: Backup automático
0 2 * * * /opt/pmj-backend/backup.sh
```

### Semanal
```bash
# Domingo 3 AM: Backup completo
0 3 * * 0 /opt/pmj-backend/backup_s3.sh
```

### Mensual
```bash
# Primer día del mes 4 AM: Backup encriptado
0 4 1 * * /opt/pmj-backend/backup_encrypted.sh
```

### Retención
- Diarios: 7 días
- Semanales: 4 semanas
- Mensuales: 12 meses

## ✅ Verificación de Backups

```bash
# Verificar integridad de archivo
gunzip -t backup_20240416.sql.gz

# Ver tamaño
du -h /backups/pmj/

# Contar backups
ls -1 /backups/pmj/pmj_db_*.gz | wc -l

# Backup más antiguo
ls -ltr /backups/pmj/ | head -1

# Backup más reciente
ls -ltr /backups/pmj/ | tail -1
```

## 🚨 Plan de Recuperación ante Desastre

### Si la BD se daña

1. **Detener la aplicación**
   ```bash
   docker-compose down
   ```

2. **Listar backups disponibles**
   ```bash
   ls -lh /backups/pmj/
   ```

3. **Elegir backup más reciente bueno**
   ```bash
   gunzip -t /backups/pmj/pmj_db_20240415.sql.gz
   ```

4. **Iniciar solo BD**
   ```bash
   docker-compose up -d db
   sleep 30
   ```

5. **Restaurar**
   ```bash
   gunzip < /backups/pmj/pmj_db_20240415.sql.gz | \
   docker-compose exec -T db \
   mysql -u pmj_user -p pmj_db
   ```

6. **Verificar**
   ```bash
   docker-compose exec db mysql -u pmj_user -p pmj_db \
     -e "SELECT COUNT(*) FROM users;"
   ```

7. **Reiniciar aplicación**
   ```bash
   docker-compose up -d
   ```

8. **Testear**
   ```bash
   curl http://localhost:8000/docs
   ```

## 📞 Contacto en Emergencia

- **Soporte BD**: [contacto]
- **Backup en Cloud**: [contacto]
- **Responsable IT**: [contacto]
