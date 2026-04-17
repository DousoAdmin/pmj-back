# 📚 Scripts - Documentación y Configuración

Carpeta central con documentación completa de la aplicación y templates para nuevos proyectos.

## 📂 Estructura

```
Scripts/
│
├── 📖 Documentacion/
│   ├── Docker/          # Docker y despliegue
│   ├── Guias/           # Guías prácticas
│   └── README.md        # Índice de documentación
│
├── 📋 Configuracion/
│   ├── ESTRUCTURA_BASE_APLICATIVO.md
│   ├── TEMPLATE_CONFIGURACION.md
│   └── README.md        # Cómo usar estos documentos
│
├── 🏃‍♂️ Scripts de Operación
│   ├── scripts/         # Scripts útiles (próximamente)
│   └── backups/         # Backups (próximamente)
│
└── 📄 Este archivo (README.md)
```

## 🎯 Acceso Rápido

### 🚀 Quiero iniciar la aplicación

→ [Documentacion/Docker/DOCKER_QUICKSTART.md](Documentacion/DOCKER_QUICKSTART.md)
**Tiempo:** 2 minutos

### 🆘 Tengo un problema

→ [Documentacion/Guias/TROUBLESHOOTING.md](Documentacion/Guias/TROUBLESHOOTING.md)
**Tiempo:** 5-15 minutos

### 📋 Necesito hacer una tarea

→ [Documentacion/Guias/PROCEDIMIENTOS.md](Documentacion/Guias/PROCEDIMIENTOS.md)
**Tiempo:** Varía según tarea

### 🐳 Quiero entender Docker

→ [Documentacion/Docker/DOCKER_SETUP.md](Documentacion/DOCKER_SETUP.md)
**Tiempo:** 30 minutos

### 🚀 Voy a desplegar a producción

→ [Documentacion/../DEPLOYMENT.md](../DEPLOYMENT.md)
**Tiempo:** 45 minutos

### 🏗️ Voy a crear una nueva aplicación

→ [Configuracion/TEMPLATE_CONFIGURACION.md](Configuracion/TEMPLATE_CONFIGURACION.md)
**Tiempo:** 1-2 horas

### 📖 Quiero entender la arquitectura

→ [Configuracion/ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md)
**Tiempo:** 1 hora

---

## 📚 Documentación Organizadas por Carpeta

### 📖 [Documentacion/](Documentacion/)

Documentación de operación y mantenimiento de la aplicación.

**Subcarpetas:**

#### 🐳 [Docker/](Documentacion/Docker/)
- **DOCKER_CONFIGS.md** - Referencia de configuraciones Docker
- **README.md** - Índice de documentación Docker
- **Referencias cruzadas:**
  - DOCKER_QUICKSTART.md (en raíz)
  - DOCKER_SETUP.md (en raíz)
  - DEPLOYMENT.md (en raíz)

#### 📖 [Guias/](Documentacion/Guias/)
- **PROCEDIMIENTOS.md** - Tareas comunes paso a paso
- **TROUBLESHOOTING.md** - Solución de problemas
- **OPERACIONES_DIARIAS.md** - Tareas de rutina diaria
- **BACKUP_Y_RECUPERACION.md** - Backup automático y recuperación

#### 📋 [README.md](Documentacion/README.md)
- Índice de documentación
- Tabla de contenidos rápida
- Búsqueda de documentos

### 📋 [Configuracion/](Configuracion/)

Documentos para entender y replicar la estructura del aplicativo.

**Archivos:**

- **ESTRUCTURA_BASE_APLICATIVO.md** - Arquitectura completa de PMJ Backend
  - Cómo está estructurada la aplicación
  - Patrones de código
  - Stack tecnológico
  - Modelos base

- **TEMPLATE_CONFIGURACION.md** - Template para crear nuevas aplicaciones
  - Pasos para iniciar un nuevo proyecto
  - Código base a copiar
  - Configuración mínima requerida
  - Checklist final

- **README.md** - Guía sobre cómo usar estos documentos
  - Cuándo usar cada documento
  - Mapa de contenidos
  - Ejemplos de uso

---

## 🗺️ Mapa de Navegación

```
Necesito...                          → Documento
────────────────────────────────────────────────────────────
Iniciar rápido                       → Docker/QUICKSTART
Resolver error                       → Guias/TROUBLESHOOTING
Hacer tarea diaria                   → Guias/OPERACIONES_DIARIAS
Hacer backup                         → Guias/BACKUP_Y_RECUPERACION
Ver estado de servicios              → Guias/PROCEDIMIENTOS
Hacer deploy                         → ../DEPLOYMENT.md
Configurar variables                 → Docker/DOCKER_CONFIGS.md
Entender arquitectura                → Configuracion/ESTRUCTURA_BASE_APLICATIVO.md
Crear nueva aplicación               → Configuracion/TEMPLATE_CONFIGURACION.md
Encontrar documento                  → Documentacion/README.md
```

---

## 📊 Estadísticas de Documentación

| Carpeta | Documentos | Páginas | Secciones |
|---------|-----------|---------|-----------|
| Documentacion/Docker | 4 | ~60 | 50+ |
| Documentacion/Guias | 4 | ~80 | 60+ |
| Configuracion | 3 | ~100 | 80+ |
| **TOTAL** | **11** | **~240** | **190+** |

---

## 🎯 Nuevos Desarrolladores - Empezar Aquí

### Semana 1

**Día 1:**
1. Leer [Documentacion/README.md](Documentacion/README.md)
2. Ejecutar [Documentacion/Docker/DOCKER_QUICKSTART.md](Documentacion/Docker/DOCKER_QUICKSTART.md)
3. Verificar que app esté corriendo en http://localhost:8000

**Día 2-3:**
1. Leer [Configuracion/ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md)  
2. Explorar archivos reales en el proyecto
3. Entender las 4 capas: Model → Schema → Service → Router

**Día 4-5:**
1. Leer [Documentacion/Guias/PROCEDIMIENTOS.md](Documentacion/Guias/PROCEDIMIENTOS.md)
2. Practicar comandos Docker comunes
3. Familiarizarse con estructura

**Fin de semana:**
1. Revisar [Documentacion/Docker/DOCKER_SETUP.md](Documentacion/Docker/DOCKER_SETUP.md) si es necesario
2. Resolver dudas con [Documentacion/Guias/TROUBLESHOOTING.md](Documentacion/Guias/TROUBLESHOOTING.md)

### Semana 2

1. Comenzar a hacer cambios / crear nuevos endpoints
2. Consultar patrones en [Configuracion/ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md)
3. Crear PR con cambios

---

## 💡 Tips de Uso

### Búsqueda Rápida

**VS Code:**
```
Ctrl+Shift+F → Buscar en Scripts/
```

**Línea de comandos:**
```bash
grep -r "tu-busqueda" Scripts/
```

### Favoritos para Pinear

- [Procedimientos.md](Documentacion/Guias/PROCEDIMIENTOS.md) - Comandos más usados
- [Troubleshooting.md](Documentacion/Guias/TROUBLESHOOTING.md) - Errores comunes
- [Docker/Configs.md](Documentacion/Docker/DOCKER_CONFIGS.md) - Variables y config

### Documentos para Imprimir/PDF

- [ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md)
- [TEMPLATE_CONFIGURACION.md](Configuracion/TEMPLATE_CONFIGURACION.md)

---

## 🔗 Enlaces Globales

| Tipo | Ubicación |
|------|-----------|
| Inicio Rápido | [Documentacion/Docker/DOCKER_QUICKSTART.md](Documentacion/Docker/DOCKER_QUICKSTART.md) |
| Documentación Completa | [Documentacion/](Documentacion/) |
| Solución de Problemas | [Documentacion/Guias/TROUBLESHOOTING.md](Documentacion/Guias/TROUBLESHOOTING.md) |
| Configuración | [Configuracion/](Configuracion/) |
| Diseño de Arquitectura | [Configuracion/ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md) |
| Template Nueva App | [Configuracion/TEMPLATE_CONFIGURACION.md](Configuracion/TEMPLATE_CONFIGURACION.md) |

---

## 🚀 Flujos de Trabajo Comunes

### Trabajar en Feature Nueva

```
1. Leer ESTRUCTURA_BASE_APLICATIVO.md
   ↓
2. Consultar patrones similares en proyecto
   ↓
3. Crear Model (ver ejemplo en ESTRUCTURA_BASE_APLICATIVO.md)
   ↓
4. Crear Schema (ver ejemplo)
   ↓
5. Crear Service (ver ejemplo)
   ↓
6. Crear Router (ver ejemplo)
   ↓
7. Testear localmente
   ↓
8. Commit y push
```

### Resolver Un Bug

```
1. Ver logs: docker-compose logs -f
   ↓
2. No entiendo el error → Consultar TROUBLESHOOTING.md
   ↓
3. Necesito ejecutar comando → Consultar PROCEDIMIENTOS.md
   ↓
4. Revisar el código usando patrones
   ↓
5. Fix y testear
   ↓
6. Commit y push
```

### Desplegar a Producción

```
1. Leer DEPLOYMENT.md
   ↓
2. Seguir checklist pre-producción
   ↓
3. Configurar variables de entorno
   ↓
4. Hacer build Docker
   ↓
5. Testing en ambiente staging
   ↓
6. Deploy a producción
```

---

## 📞 Ayuda Rápida

**¿No encuentras lo que necesitas?**

1. Busca en [Documentacion/README.md](Documentacion/README.md) - Tabla de contenidos
2. Busca en [Configuracion/README.md](Configuracion/README.md) - Cómo usar documentos
3. Usa Ctrl+Shift+F en VS Code dentro de Scripts/
4. Consulta el archivo más específico (ej: TROUBLESHOOTING para errores)

**¿Encontraste un error en la documentación?**

1. Edita el archivo .md
2. Haz commit con mensaje: `docs: fix [descripción]`
3. Push para que otros vean la corrección

---

## 📈 Continuidad y Mantenimiento

### Cómo mantener esta documentación

- ✓ Actualizar cuando cambios mayores en arquitectura
- ✓ Corregir errores cuando se encuentren
- ✓ Agregar nuevos procedimientos cuando se usen frecuentemente
- ✓ Mantener templates sincronizados con código real

### Checklist de Actualización

- [ ] ¿Cambió la estructura de carpetas? → Actualizar ESTRUCTURA_BASE_APLICATIVO.md
- [ ] ¿Cambió el stack? → Actualizar TEMPLATE_CONFIGURACION.md
- [ ] ¿Hay nuevo procedimiento? → Agregar a PROCEDIMIENTOS.md
- [ ] ¿Nuevo problema conocido? → Agregar a TROUBLESHOOTING.md

---

## ✨ Destacados

### Mejor para Principiantes
🌟 [Docker/DOCKER_QUICKSTART.md](Documentacion/Docker/DOCKER_QUICKSTART.md) - 2 minutos para funcionar

### Más Completo
📖 [ESTRUCTURA_BASE_APLICATIVO.md](Configuracion/ESTRUCTURA_BASE_APLICATIVO.md) - Toda la arquitectura

### Más Útil
🔧 [Procedimientos.md](Documentacion/Guias/PROCEDIMIENTOS.md) - Comandos diarios

### Para Crear Nueva App
🏗️ [TEMPLATE_CONFIGURACION.md](Configuracion/TEMPLATE_CONFIGURACION.md) - Copy-paste ready

---

**Última actualización:** 2024-04-16
**Documentação Completa:** ✓
**Última revisión:** 2024-04-16
