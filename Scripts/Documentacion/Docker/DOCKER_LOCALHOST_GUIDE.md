# 🐳 Docker + XAMPP - Guía de Validación y Troubleshooting

## ✅ Pre-requisitos

Antes de ejecutar Docker, verifica que tengas:

```bash
1. XAMPP corriendo con MySQL iniciado
2. La BD "prueba" creada en MySQL
3. Docker Desktop instalado y corriendo
4. .env correctamente configurado
```

---

## 🚀 Iniciar Docker (Desarrollo)

### Opción 1: Script Batch (Windows)
```batch
double-click docker-start.bat
```

### Opción 2: Línea de comando
```bash
cd /path/to/pmj-back
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

---

## 🔍 Validar Conexión a BD

### Test 1: Desde tu máquina (sin Docker)
```bash
python test_db_connection.py
```

**Debe mostrar:**
```
✅ CONEXIÓN EXITOSA
📊 Información de la BD:
   Tablas encontradas (N):
     - tabla1
     - tabla2
```

### Test 2: Desde Docker
```bash
# Construye la imagen primero
docker build -t pmj_app .

# Ejecuta el test
docker run --rm -it --network=pmj_network \
  -e DATABASE_URL="mysql+pymysql://root@host.docker.internal:3306/prueba" \
  -v %cd%:/app \
  pmj_app python test_db_connection.py
```

---

## 🔧 Troubleshooting

### ❌ Error: "Access denied for user 'root'@'localhost'"

**Posibles causas:**
1. MySQL en XAMPP no está corriendo
2. El usuario root tiene contraseña (no debe tener)
3. Puerto 3306 está ocupado

**Soluciones:**
```bash
# Verifica que MySQL esté corriendo en XAMPP
# Abre XAMPP Control Panel → Start MySQL

# Verifica conectividad desde Docker
docker run --rm -it ubuntu bash
# Dentro del contenedor:
apt-get update && apt-get install -y mysql-client
mysql -h host.docker.internal -u root -e "SELECT 1"
```

---

### ❌ Error: "host.docker.internal: Nombre o servicio no conocido"

**Este es un problema de Linux/WSL.** En Windows/Mac funciona automáticamente.

**Solución:**
```bash
# En Linux, reemplaza en docker-compose.yml:
# host.docker.internal → tu.ip.local.aqui
# O usa el gateway de Docker:
# host.docker.internal → host-gateway

# Ya está incluido en:
extra_hosts:
  - "host.docker.internal:host-gateway"
```

---

### ❌ Error: "Can't connect to MySQL server"

**Posibles causas:**
1. BD "prueba" no existe
2. Firewall bloqueando puerto 3306
3. MySQL no está en puerto 3306

**Soluciones:**
```bash
# 1. Crea la BD si no existe
mysql -u root -e "CREATE DATABASE IF NOT EXISTS prueba;"

# 2. Verifica que MySQL esté en puerto 3306
mysql -u root -e "SELECT 1;" 

# 3. Si MySQL está en otro puerto, actualiza .env:
DATABASE_URL=mysql+pymysql://root@localhost:3306/prueba  # cambiar puerto si es necesario
```

---

## 📊 Verificar que Docker esté conectado

### Ver logs en vivo
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f app
```

### Buscar errores de BD
```bash
docker-compose logs app | grep -i "database\|connection\|error"
```

### Verificar que el contenedor esté corriendo
```bash
docker ps
# Deberías ver: pmj_app  corriendo en puerto 8000
```

---

## ✨ Acceso a la aplicación

Si todo está corriendo:

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛑 Detener Docker

```bash
# Opción 1: Script
docker-stop.bat

# Opción 2: Línea de comando
docker-compose down

# Opción 3: Preservar volúmenes
docker-compose down --remove-orphans
```

---

## 📝 Configuración del .env para diferentes escenarios

### Desarrollo local (sin Docker)
```env
DATABASE_URL=mysql+pymysql://root@localhost:3306/prueba
```

### Desarrollo con Docker
```env
DATABASE_URL=mysql+pymysql://root@host.docker.internal:3306/prueba
```

### Producción con servidor remoto
```env
DATABASE_URL=mysql+pymysql://root:password@tu.servidor.com:3306/prueba
```

---

## 🔐 Seguridad

⚠️ **IMPORTANTE:**
- En producción, NUNCA usar `root` sin contraseña
- Crear usuario específico para la aplicación
- Usar variables de entorno para credenciales

```sql
-- Crear usuario seguro (MySQL)
CREATE USER 'pmj_user'@'%' IDENTIFIED BY 'contraseña_fuerte';
GRANT ALL PRIVILEGES ON prueba.* TO 'pmj_user'@'%';
FLUSH PRIVILEGES;
```

---

## 📚 Recursos

- [Docker Docs](https://docs.docker.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MySQL](https://dev.mysql.com/doc/)
