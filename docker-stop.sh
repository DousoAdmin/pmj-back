#!/bin/bash
# Script para parar servicios Docker

echo "🛑 Deteniendo servicios Docker..."
docker-compose down

echo "✅ Servicios detenidos"
echo ""
echo "Para remover volúmenes (cuidado: elimina datos):"
echo "  docker-compose down -v"
