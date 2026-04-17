# 🐳 Docker Documentation Index

Documentación completa sobre Docker para PMJ Backend.

## 📚 Documentos

### 1. [DOCKER_QUICKSTART.md](../DOCKER_QUICKSTART.md)
**Tiempo:** 2 minutos
**Nivel:** Principiante

- Inicio rápido Windows/Linux
- Verificación básica
- Primer acceso a la app

### 2. [DOCKER_SETUP.md](../../DOCKER_SETUP.md)
**Tiempo:** 30 minutos
**Nivel:** Intermedio

- Información completa de Docker
- Estructura de archivos
- Acceso a servicios
- Comandos útiles
- Troubleshooting

### 3. [DOCKER_CONFIGS.md](DOCKER_CONFIGS.md)
**Tiempo:** 15 minutos
**Nivel:** Técnico

- Variables de entorno
- Estructura Dockerfile
- Servicios Docker Compose
- Configuración de recursos
- Health checks

### 4. [DEPLOYMENT.md](../../DEPLOYMENT.md)
**Tiempo:** 45 minutos
**Nivel:** Avanzado

- Opciones de despliegue
- AWS ECS, Google Cloud, DigitalOcean
- Kubernetes
- HTTPS/SSL
- Monitoreo
- Backups

## 🎯 Flujo de Aprendizaje

```
Principiante
    ↓
[DOCKER_QUICKSTART] - ¿Funciona?
    ├─ Sí  → [PROCEDIMIENTOS] de Guias/
    └─ No  → [TROUBLESHOOTING] de Guias/
    ↓
Intermedio
    ↓
[DOCKER_SETUP] - Entender todo
    ├─ Configuración → [DOCKER_CONFIGS]
    └─ Problemas → [TROUBLESHOOTING]
    ↓
Avanzado
    ↓
[DEPLOYMENT] - Producción
    ├─ Monitoreo → [OPERACIONES_DIARIAS]
    └─ Backups → [BACKUP_Y_RECUPERACION]
```

## 🔗 Enlaces a Otros Documentos

**Guías de Operación:**
- [Procedimientos Comunes](../../Guias/PROCEDIMIENTOS.md)
- [Troubleshooting](../../Guias/TROUBLESHOOTING.md)
- [Operaciones Diarias](../../Guias/OPERACIONES_DIARIAS.md)
- [Backup y Recuperación](../../Guias/BACKUP_Y_RECUPERACION.md)

**Configuración de Aplicativo:**
- [ESTRUCTURA_BASE_APLICATIVO.md](../Configuracion/ESTRUCTURA_BASE_APLICATIVO.md)
- [TEMPLATE_CONFIGURACION.md](../Configuracion/TEMPLATE_CONFIGURACION.md)

## 🚀 Casos de Uso Comunes

| Necesidad | Documento |
|-----------|-----------|
| Ejecutar app | DOCKER_QUICKSTART |
| Error no funciona | TROUBLESHOOTING |
| Entender qué es un volumen | DOCKER_CONFIGS |
| Desplegar en servidor | DEPLOYMENT |
| Hacer backup | BACKUP_Y_RECUPERACION |
| Tarea diaria | OPERACIONES_DIARIAS |

## 💡 Tips Rápidos

```bash
# ⚡ Inicio en 1 línea
docker-compose up -d

# 📊 Ver estado
docker-compose ps

# 📋 Ver logs
docker-compose logs -f

# 🐚 Acceder a shell
docker-compose exec app bash

# 🛑 Parar
docker-compose down

# 🔧 Rebuild
docker-compose up -d --build
```

## 📞 Necesitas Ayuda?

1. **Empezar** → [DOCKER_QUICKSTART](../DOCKER_QUICKSTART.md)
2. **Error** → [TROUBLESHOOTING](../../Guias/TROUBLESHOOTING.md)
3. **Cómo hace...** → [PROCEDIMIENTOS](../../Guias/PROCEDIMIENTOS.md)
4. **Detalles técnicos** → [DOCKER_CONFIGS](DOCKER_CONFIGS.md)

## 📝 Checklist de Setup

- [ ] Docker instalado
- [ ] .env copiado y editado
- [ ] `docker-compose up -d` ejecutado
- [ ] http://localhost:8000 accesible
- [ ] Logs sin errores (`docker-compose logs`)
- [ ] BD conectada (`docker-compose ps`)
