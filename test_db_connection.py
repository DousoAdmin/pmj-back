#!/usr/bin/env python3
"""
Script para validar conexión a la base de datos
Úsalo para verificar si Docker se conecta correctamente a MySQL en XAMPP

Uso:
  python test_db_connection.py           # Prueba desde localhost
  docker run --rm --network=pmj_network -e DATABASE_URL="mysql+pymysql://root@host.docker.internal:3306/prueba" -v $(pwd):/app pmj_app python test_db_connection.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 70)
print("🔍 VALIDACIÓN DE CONEXIÓN A BASE DE DATOS")
print("=" * 70)
print(f"\n📋 DATABASE_URL: {DATABASE_URL}")
print()

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL no está configurada en .env")
    sys.exit(1)

try:
    from sqlalchemy import create_engine, text
    
    print("⏳ Intentando conectar a la base de datos...")
    
    # Crear engine
    engine = create_engine(DATABASE_URL)
    
    # Intentar conexión
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ CONEXIÓN EXITOSA")
        print(f"\n📊 Información de la BD:")
        
        # Listar tablas
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        
        if tables:
            print(f"   Tablas encontradas ({len(tables)}):")
            for table in tables:
                print(f"     - {table[0]}")
        else:
            print("   ⚠️  No hay tablas en la BD")
        
        print("\n✨ La aplicación puede conectarse a la base de datos")
        sys.exit(0)

except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {str(e)}")
    print(f"\n🔧 Posibles soluciones:")
    print("   1. ¿MySQL está corriendo en XAMPP?")
    print("   2. ¿La BD 'prueba' existe? CREATE DATABASE prueba;")
    print("   3. ¿El usuario root tiene acceso sin contraseña?")
    print("   4. Para Docker: ¿host.docker.internal funciona?")
    print("      (Prueba: docker run -it --rm ubuntu ping host.docker.internal)")
    sys.exit(1)
