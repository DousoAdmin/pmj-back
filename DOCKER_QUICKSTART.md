# ⚡ Docker Quick Start

## Inicio en 2 minutos

### Windows
```bash
docker-start.bat
```

### Linux / Mac
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Manual
```bash
cp .env.docker .env
docker-compose up -d
```

## ✅ Listo

Aplicación: http://localhost:8000
Documentación API: http://localhost:8000/docs

## 📋 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Acceder a bash
docker-compose exec app bash

# Acceder a MySQL
docker-compose exec db mysql -u pmj_user -p pmj_db

# Parar
docker-compose down
```

## 🧑‍💻 Desarrollo con hot-reload

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 📚 Documentación Completa

- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Guía detallada
- [DEPLOYMENT.md](DEPLOYMENT.md) - Despliegue a producción
- [README.md](README.md) - Información general

## ⚠️ Importante

1. Edita `.env` antes de producción
2. Cambia `SECRET_KEY` a un valor seguro
3. Usa contraseñas fuertes para MySQL

```bash
# Generar SECRET_KEY seguro
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🆘 Problemas?

Ver logs:
```bash
docker-compose logs -f
```

Ver guía completa: [DOCKER_SETUP.md](DOCKER_SETUP.md#troubleshooting)
