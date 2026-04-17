# 📅 Operaciones Diarias

Tareas de rutina diaria para mantener la aplicación en funcionamiento.

## 🌅 Al Iniciar el Turno

### 1. Verificar Estado

```bash
# 1. Revisar que Docker esté corriendo
docker ps

# 2. Ver estado de servicios
docker-compose ps

# 3. Revisar logs de errores
docker-compose logs --tail=50 | grep -i error

# 4. Verificar recursos
docker stats --no-stream
```

### 2. Checklist

- [ ] ¿Todos los contenedores están UP?
- [ ] ¿Hay errores en logs?
- [ ] ¿API responde? (curl http://localhost:8000)
- [ ] ¿BD está accesible?
- [ ] ¿Hay espacio en disco?

## 🔄 Tareas Durante el Día

### Monitoreo Cada Hora

```bash
#!/bin/bash
# monitoreo.sh - Ejecutar cada hora

echo "=== $(date) ==="
docker-compose ps
echo ""
docker stats --no-stream
echo ""
docker-compose logs --tail=20 app | tail -5
```

### Verificar Aplicación

```bash
# Test de salud
curl -s http://localhost:8000/ | head -20

# Docs API disponible
curl -s http://localhost:8000/docs

# Verificar logs
docker-compose logs -f app | head -50
```

### Mantenimiento de BD

```bash
# Ver tamaño de BD
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024,2) FROM information_schema.tables GROUP BY table_schema;"

# Ver transacciones activas
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "SHOW PROCESSLIST;"

# Ver estado de replicación (si aplica)
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "SHOW SLAVE STATUS\G"
```

### Limpiar Logs Viejos

```bash
# Limitar size de logs de Docker
# /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

# O manualmente
docker system prune --filter "until=24h"
```

## 🌙 Al Finalizar el Turno

### 1. Documentar Estado

```bash
# Crear reporte
echo "=== Reporte de Cierre del Turno ===" > reporte.txt
date >> reporte.txt
echo "" >> reporte.txt
echo "Estado de servicios:" >> reporte.txt
docker-compose ps >> reporte.txt
echo "" >> reporte.txt
echo "Últimos logs:" >> reporte.txt
docker-compose logs --tail=20 >> reporte.txt
```

### 2. Hacer Backup (si no es automático)

```bash
# Ver script en BACKUP_Y_RECUPERACION.md
bash backup.sh
```

### 3. Verificar Build/Deploy

```bash
# Si hay nuevos cambios
git log -1 --oneline

# Si se hizo deploy
docker-compose images

# Testear brevemente
curl -s http://localhost:8000/docs
```

### 4. Pasar Información

- [ ] ¿Problemas reportados?
- [ ] ¿Cambios realizados?
- [ ] ¿Próximas tareas?
- [ ] ¿Alertas pendientes?

## 📊 Reportes Comunes

### Reporte Diario

```bash
#!/bin/bash
# reporte_diario.sh

DATE=$(date +%Y-%m-%d)
echo "=== REPORTE DIARIO $DATE ===" >> reporte_$DATE.txt

echo "Uptime de servicios:" >> reporte_$DATE.txt
docker-compose ps >> reporte_$DATE.txt

echo "Uso de recursos:" >> reporte_$DATE.txt
docker stats --no-stream >> reporte_$DATE.txt

echo "Transacciones BD:" >> reporte_$DATE.txt
docker-compose exec -T db mysql -u pmj_user -p${MYSQL_PASSWORD} pmj_db \
  -e "SELECT COUNT(*) FROM users;" >> reporte_$DATE.txt

echo "Reporte guardado en: reporte_$DATE.txt"
```

### Alertas a Revisar

```bash
# Conexiones DB altas
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "SHOW STATUS LIKE 'Max_used_connections';"

# Memoria disponible
free -h

# Espacio en disco
df -h

# Conexiones TCP
netstat -an | grep ESTABLISHED | wc -l
```

## 🛠️ Mantenimiento Preventivo

### Semanal

```bash
# 1. Actualizar imágenes base
docker pull python:3.11-slim
docker pull mysql:8.0

# 2. Limpiar recursos no usados
docker system prune -a --volumes

# 3. Revisar logs de errores
docker-compose logs --tail=1000 app | grep -i error

# 4. Backup de configuración
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env docker-compose.yml nginx.conf
```

### Mensual

```bash
# 1. Actualizar dependencias Python
docker-compose exec app pip install --upgrade -r requirements.txt

# 2. Rebuild de imagen
docker-compose build --no-cache

# 3. Análisis de rendimiento
docker stats --no-stream
docker-compose logs app | grep -i slow

# 4. Documentar cambios
git log --oneline -10 > CAMBIOS_RECIENTE.txt

# 5. Verificar integridad de BD
docker-compose exec db mysql -u pmj_user -p pmj_db \
  -e "CHECK TABLE users;"
```

### Trimestral

```bash
# 1. Backup completo del sistema
tar -czf backup_$(date +%Y%m%d).tar.gz .env .git Services Models Config

# 2. Revisar y actualizar documentación
ls -la Scripts/Documentacion/

# 3. Análisis de seguridad
docker inspect pmj_app | grep -i security

# 4. Planificación de capacidad
docker stats --no-stream
```

## ⚙️ Automatización

### Cron jobs recomendados

```bash
# Backup diario 2 AM
0 2 * * * /path/to/backup.sh

# Monitoreo cada hora
0 * * * * /path/to/monitoreo.sh >> /var/log/pmj_monitor.log

# Limpieza de logs viejos (cada domingo)
0 0 * * 0 docker system prune -a --volumes

# Reporte semanal (lunes 9 AM)
0 9 * * 1 /path/to/reporte_semanal.sh
```

## 📝 Template de Bitácora

```markdown
## [Fecha] - Turno [Número]

### Al Iniciar
- [ ] Servicios UP
- [ ] Sin errores críticos
- [ ] Espacio disponible

### Durante el Turno
- Hora | Evento | Acción

### Al Finalizar
- Backup: ✓
- Cambios: [listar]
- Próximas tareas:

### Observaciones
[Notas relevantes]
```
