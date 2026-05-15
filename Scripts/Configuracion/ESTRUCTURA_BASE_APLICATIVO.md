# 🏗️ Estructura Base del Aplicativo

Documento descriptor de arquitectura de aplicación de backend modular.
Use este documento como **reference** para crear aplicaciones similares.

⚠️ **NOTA DE SEGURIDAD:** Este documento contiene arquitectura y patrones.
Para información de producción, consultar documentación privada.

---

## 📋 Resumen Ejecutivo

| Aspecto | Detalle |
|--------|---------|
| **Nombre Aplicación** | [CONFIGURAR] |
| **Framework** | FastAPI |
| **Lenguaje** | Python 3.11+ |
| **Base de Datos** | [CONFIGURAR - SQL/NoSQL] |
| **ORM** | [CONFIGURAR - SQLAlchemy/etc] |
| **Autenticación** | JWT con tokens |
| **Servidor** | ASGI (desarrollo) + WSGI (producción) |
| **Containerización** | Docker + Orquestación |
| **Despliegue** | Containerizado en nube |

---

## 🏛️ Arquitectura General

```
┌────────────────────────────────────────┐
│   Cliente / Consumidor                 │
│   (Frontend / Mobile / API Client)     │
└─────────────┬──────────────────────────┘
              │ Request HTTPS
              │
┌─────────────▼──────────────────────────┐
│   Capa de Proxy / Gateway              │
│   (Opcional en producción)             │
│   ✓ Terminación TLS/SSL                │
│   ✓ Enrutamiento                       │
│   ✓ Rate limiting                      │
│   ✓ Caché de respuestas                │
└─────────────┬──────────────────────────┘
              │ Request HTTP
              │
┌─────────────▼──────────────────────────┐
│   Capa de Aplicación Backend           │
│   ┌────────────────────────────────┐   │
│   │ Routers & Endpoints            │   │
│   │  ✓ Autenticación/Autorización  │   │
│   │  ✓ Recursos de negocio        │   │
│   │  ✓ Operaciones CRUD            │   │
│   └────────────────────────────────┘   │
│   ┌────────────────────────────────┐   │
│   │ Services (Lógica Negocio)      │   │
│   │  ✓ Validaciones               │   │
│   │  ✓ Reglas de negocio          │   │
│   │  ✓ Orquestación               │   │
│   └────────────────────────────────┘   │
│   ┌────────────────────────────────┐   │
│   │ Schemas/Validadores           │   │
│   │  ✓ Validación entrada         │   │
│   │  ✓ Serialización salida       │   │
│   └────────────────────────────────┘   │
└─────────────┬──────────────────────────┘
              │ SQL Queries
              │
┌─────────────▼──────────────────────────┐
│   Capa ORM (Object-Relational Mapper)  │
│   ✓ Mapeo objeto-relacional            │
│   ✓ Pool de conexiones                 │
│   ✓ Transacciones seguras              │
└─────────────┬──────────────────────────┘
              │
┌─────────────▼──────────────────────────┐
│   Base de Datos (SQL Relacional)       │
│   ✓ Almacenamiento persistente         │
│   ✓ Integridad referencial             │
│   ✓ Respaldos automáticos              │
│   ✓ Recuperación ante fallos           │
└────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas Recomendada

```
backend-app/
│
├── 📄 main.py                          # Punto de entrada
├── 📄 requirements.txt                 # Dependencias
├── .env.template                       # Plantilla configuración
├── 📄 README.md                        # Documentación
│
├── 🗂️ Config/                          # Configuración
│   ├── __init__.py
│   ├── config.py                       # Settings
│   └── database.py                     # BD config
│
├── 🗂️ Core/                            # Lógica central
│   ├── __init__.py
│   └── security.py                     # Seguridad
│
├── 🗂️ Models/                          # Modelos ORM
│   ├── __init__.py
│   ├── [modulo_1]/
│   │   ├── __init__.py
│   │   └── [modelo_name.py]
│   └── ...
│
├── 🗂️ Schemas/                         # Esquemas validación
│   ├── __init__.py
│   ├── [modulo_1]/
│   │   ├── __init__.py
│   │   └── [schema_name.py]
│   └── ...
│
├── 🗂️ Routers/                         # Endpoints
│   ├── __init__.py
│   ├── [modulo_1]/
│   │   ├── __init__.py
│   │   └── [router_name.py]
│   └── ...
│
├── 🗂️ Services/                        # Lógica negocio
│   ├── __init__.py
│   ├── [modulo_1]/
│   │   ├── __init__.py
│   │   └── [service_name.py]
│   └── ...
│
├── 🗂️ Scripts/                         # Utilidades
│   └── ...
│
├── 🐳 Docker/                          # Configuración
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── ...
│
└── 🔧 .github/workflows/               # CI/CD
    └── [workflow_files.yml]
```
│   │
│   └── .gitignore
│
└── env/                                # Virtual environment (local)
    └── ...
```

---

## 🔌 Stack Tecnológico

### Backend
```
- Framework web asincrónico moderno
- Servidor ASGI para desarrollo
- Servidor WSGI para producción
- Validación de datos robusta
- ORM para manejo de BD
- Driver para BD relacional
```

### Autenticación & Seguridad
```
- Tokens JWT para autenticación
- Hash seguro de contraseñas (Bcrypt)
- Validación de emails
- Manejo seguro de variables sensibles
```

### Utilidades
```
- Gestor de variables de entorno
- Migraciones de BD (opcional)
- Validación de esquemas
- Documentación automática
```

### Base de Datos
```
- Base de datos SQL relacional (configurar versión según necesidad)
```

### Containerización
```
- Docker (containerización)
- Orquestación de contenedores
- Reverse proxy (opcional en producción)
```

---

## 🔐 Seguridad

### Autenticación

```
✓ Hash de contraseñas: algoritmo robusto (Bcrypt recomendado)
✓ Tokens JWT con expiración configurable
✓ Sin almacenamiento de passwords en texto plano
✓ Validación en cada request protegido
✓ Algo y llave de JWT en variables de entorno
```

### Base de Datos

```
✓ ORM para prevenir inyección SQL
✓ Pool de conexiones configurado
✓ Credenciales en variables de entorno (NUNCA hardcodeadas)
✓ Encriptación de datos sensibles (implementar según necesidad)
✓ Backups automáticos en producción
```

### Validación

```
✓ Validación de tipos en entrada
✓ Esquemas estrictos de datos
✓ Restricciones de datos
✓ Sanitización de input
✓ Rate limiting en API
```

---

## 🚀 Flujo de Operación

### 1. Inicio de Aplicación

```
1. Cargar configuración desde variables de entorno
2. Validar que DB estén disponibles
3. Crear estructura de datos (migraciones o create_all)
4. Registrar todas las rutas/endpoints
5. Iniciar servidor web
6. Verificar health check
```

### 2. Ciclo de Request - Response

```
Cliente HTTP Request
        ↓
Router (enrutamiento)
        ↓
Validación de Schema (entrada)
        ↓
Service (lógica de negocio)
        ↓
ORM (acceso a datos)
        ↓
Base de Datos (persistencia)
        ↓
Response (serialización salida)
```

### 3. Flujo de Autenticación

```
1. POST /auth/[ENDPOINT]
2. Validar credenciales de usuario
3. Generar token JWT
4. Retornar token al cliente

5. Requests posteriores
6. Header: Authorization: Bearer <token>
7. Validar token (Core/security.py)
8. Extraer identidad del usuario
9. Proceder si token es válido
```

---

## 🗄️ Modelo de Datos Base

### Estructura Recomendada

```
Tablas principales:
- Identidad (usuarios - hash de contraseña, NUNCA texto plano)
- Autorización (roles, permisos)
- Recursos principales del negocio
- Auditoría (trazabilidad)

Relaciones:
- N:M entre usuarios y roles
- N:M entre roles y permisos
- 1:N entre categorías y elementos
```

### Campos Comunes en Todas las Tablas

```
✓ ID único (primary key, auto-incremento)
✓ created_at (timestamp)
✓ updated_at (timestamp)
✓ is_active (boolean, para soft-delete)

IMPORTANTE:
- NUNCA hardcodear ID's de datos
- NUNCA incluir nombres específicos de negocio en templates
- NUNCA almacenar contraseñas en texto plano
- SIEMPRE usar hash para sensible (contraseñas, tokens)
```

---

## ⚙️ Configuración Base

### config.py

```
✓ Usar clase Settings para validación
✓ Cargar variables desde archivo .env
✓ Defaults sensatos para desarrollo
✓ Valores de producción SOLO desde variables de entorno
✓ NUNCA hardcodear credenciales o secretos
✓ Validar que variables requeridas están presentes al inicio
✓ Sin contraseñas, API keys, o datos sensibles en el código
```

### database.py

```
✓ Crear engine con URL desde settings.DATABASE_URL
✓ Configurar pool de conexiones
✓ Crear SessionLocal factory
✓ Base declarativa para modelos
✓ Función get_db() como dependencia FastAPI
✓ Manejo seguro de sesiones (always close en try/finally)
✓ NUNCA hardcodear host, puerto, usuario o contraseña de BD
```

---

## 🔄 Patrones de Código

### Estructura de Modelo

```
1. Definir nombre de tabla
2. Definir columnas con tipos y restricciones
3. Definir relaciones a otros modelos
4. Definir soft-delete si aplica (is_active)
5. Incluir timestamps (created_at, updated_at)
6. NUNCA usar datos hardcodeados
```

### Estructura de Schema (Validación)

```
1. Heredar de BaseModel
2. Definir campos con tipos correctos
3. Agregar validadores si es necesario
4. Separar: Create, Response, Update schemas
5. NO exponer campos sensibles
6. Usar field validators para reglas de negocio
```

### Estructura de Service

```
1. Recibir Session de BD como parámetro
2. Recibir datos pre-validados del Schema
3. Realizar lógica de negocio
4. Usar ORM para persistencia (no SQL directo)
5. Manejo de errores y transacciones
6. Retornar resultado
```

### Estructura de Router

```
1. Definir prefix y tags
2. Crear GET, POST, PUT, DELETE según necesidad
3. Inyectar dependencias (DB, Usuario actual)
4. Validar autorización/permisos
5. Llamar service
6. Retornar response serializado
7. Documentar con docstrings
```

---

## 🐳 Configuración de Containerización

### Dockerfile

```
✓ Usar imagen base oficial slim
✓ Multi-stage build (builder + runtime)
✓ Etapa builder: compilar dependencias
✓ Etapa final: solo lo necesario
✓ Exponer puerto en variable
✓ User no-root por seguridad
✓ Health check incluido
✓ NUNCA incluir credenciales en imagen
```

### docker-compose.yml

```
✓ Servicios claramente definidos
✓ Variables de entorno desde .env
✓ Recursos limitados
✓ NO hardcodear passwords
✓ Health checks en ambos servicios
✓ Volúmenes para persistencia
✓ Red isolada entre servicios
✓ Logs configurados
```

### .env.template

```
Incluir TODAS las variables necesarias con:
✓ [SECTION] comments
✓ Ejemplos de valores (NO credenciales reales)
✓ Descripción de cada variable
✓ Valores por defecto seguros
```

---

## 📈 Escalabilidad

### Horizontal Scaling
```
- Docker Compose → Docker Swarm
- Docker Swarm → Kubernetes
- Contenedor único → Múltiples réplicas
```

### Vertical Scaling
```
- Aumentar CPU/RAM en docker-compose.prod.yml
- Aumentar workers de Gunicorn
- Aumentar pool de conexiones
```

### Base de Datos
```
- MySQL replicación
- Read replicas
- Sharding (si es necesario)
- Caching (Redis)
```

---

## 🧪 Testing

### Estructura Recomendada

```
tests/
├── unit/
│   ├── test_services/
│   │   └── test_[service_name].py
│   └── ...
│
├── integration/
│   ├── test_routes/
│   │   └── test_[route_name].py
│   └── ...
│
├── conftest.py
└── requirements-test.txt
```

### Ejecución

```bash
pytest tests/
pytest tests/ --cov=Services
pytest tests/integration/ -v
```

---

## 📊 Monitoreo

### Métricas a Monitorear
```
- Uptime de aplicación
- Response time promedio
- Errores por minuto
- Conexiones activas a BD
- Uso de CPU/RAM
- Espacio en disco
```

### Herramientas Recomendadas
```
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog
- New Relic
```

---

## 🔗 Referencias

| Aspecto | Enlace |
|--------|--------|
| FastAPI Docs | https://fastapi.tiangolo.com/ |
| SQLAlchemy | https://www.sqlalchemy.org/ |
| Docker | https://docs.docker.com/ |
| MySQL | https://dev.mysql.com/doc/ |
| Pydantic | https://docs.pydantic.dev/ |
| JWT | https://tools.ietf.org/html/rfc7519 |

---

## ✨ Conclusión

Este documento es un template arquitectónico para aplicaciones backend modulares.

### Para crear aplicaciones similares:

1. ✓ Seguir estructura de directorios recomendada
2. ✓ Adaptar modelos según requisitos de negocio
3. ✓ Reutilizar patrones de código
4. ✓ Usar template de Docker
5. ✓ NUNCA hardcodear datos sensibles
6. ✓ Validar seguridad antes de producción
7. ✓ Consultar documentación en `Scripts/Documentacion/`

⚠️ **RECORDATORIO DE SEGURIDAD:**
- Variables sensibles SIEMPRE en .env
- Credenciales NUNCA en código fuente
- Secrets en gestores dedicados (Vault, AWS Secrets, etc.)
- Credenciales de BD NUNCA en documentación pública
- No reutilizar credenciales de producción en desarrollo
- Validar permisos y autorización en cada endpoint
- Sanitizar entrada de usuario siempre
