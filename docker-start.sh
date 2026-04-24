#!/bin/bash
# Script de inicio rápido para Docker

set -e

echo "🐳 PMJ Backend - Docker Setup"
echo "=============================="

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instálalo desde https://www.docker.com"
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado."
    exit 1
fi

echo "✓ Docker y Docker Compose detectados"

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.docker .env
    echo "⚠️  Edita .env y configura las variables de entorno"
else
    echo "✓ Archivo .env ya existe"
fi

# Construir y levantar servicios
echo ""
echo "🏗️  Construyendo imagen y levantando servicios..."
docker-compose up -d --build

echo ""
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

echo ""
echo "✅ Servicios iniciados:"
echo "   - Aplicación: http://localhost:8000"
echo "   - Docs API: http://localhost:8000/docs"
echo "   - Base de datos: localhost:3306"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Parar servicios: docker-compose down"
echo "   - Acceder a la app: docker-compose exec app bash"
echo ""
docker-compose ps
