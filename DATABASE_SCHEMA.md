# 🗃️ Datos Guardados en formularios.db - Proyecto Pilar

## 📊 **Información General**

La base de datos `formularios.db` utiliza SQLite y contiene una tabla principal llamada `formularios_actividad` que almacena todos los datos de los formularios de actividades educativas enviados.

## 🏗️ **Estructura de la Tabla `formularios_actividad`**

### **🔑 Campos Principales**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | Integer (PK) | ID único autoincremental | 1, 2, 3... |
| `titulo_actividad` | Text | Título de la actividad educativa | "Taller de Ciencias Naturales" |
| `docente_responsable` | String(200) | Nombre completo del docente | "García, María Elena" |
| `fundamentacion` | Text | Fundamentación de la actividad | "Esta actividad busca..." |
| `objetivos` | Text | Objetivos y propósitos | "Lograr que los estudiantes..." |
| `metodologia` | Text | Metodología a utilizar | "Se trabajará mediante..." |

### **🎯 Campos de Destinatarios**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `grados` | Text | Grados destinatarios (separados por comas) | "1er Grado, 2do Grado, 7mo Grado" |
| `requisitos` | Text | Requisitos para participar | "Autorización de padres" |
| `materiales_presupuesto` | Text | Materiales y presupuesto necesario | "Microscopios, lupas, $5000" |

### **📅 Campos Temporales**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `meses` | Text | Meses propuestos (separados por comas) | "Enero, Marzo, Septiembre" |
| `fechas_propuestas` | Text | Fechas específicas en formato JSON | `["2025-09-29", "2025-10-15"]` |

### **👥 Equipo de Trabajo**

| Campo | Tipo | Descripción | Estructura JSON |
|-------|------|-------------|-----------------|
| `equipo_json` | Text | Array JSON con datos del equipo | Ver ejemplo abajo |

**Estructura del equipo JSON:**
```json
[
  {
    "apellido_nombre": "García, Juan Carlos",
    "dni": "12345678",
    "correo": "juan.garcia@email.com"
  },
  {
    "apellido_nombre": "López, Ana María", 
    "dni": "87654321",
    "correo": "ana.lopez@email.com"
  }
]
```

### **📋 Metadatos y Control**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `fecha_creacion` | DateTime | Cuándo se creó el registro | "2025-09-29 13:45:23" |
| `fecha_modificacion` | DateTime | Última modificación | "2025-09-29 13:45:23" |
| `estado` | String(50) | Estado del procesamiento | "pendiente", "procesado", "error" |

### **☁️ Integración Google Drive**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `documento_id` | String(100) | ID del documento en Google Docs | "1GcqJ5uN11iSDOyMzJFVQccO0..." |
| `carpeta_id` | String(100) | ID de la carpeta en Google Drive | "1DLlVYgv2HaXz8WAI2yYE..." |

## 📄 **Ejemplo Completo de Registro**

```json
{
  "id": 1,
  "titulo_actividad": "Taller de Observación Científica",
  "docente_responsable": "García, María Elena",
  "equipo": [
    {
      "apellido_nombre": "López, Carlos Alberto",
      "dni": "12345678",
      "correo": "carlos.lopez@uncoma.edu.ar"
    },
    {
      "apellido_nombre": "Martínez, Ana Isabel",
      "dni": "87654321", 
      "correo": "ana.martinez@uncoma.edu.ar"
    }
  ],
  "fundamentacion": "Esta actividad busca desarrollar habilidades de observación científica en estudiantes de nivel primario, promoviendo el pensamiento crítico y la curiosidad por el mundo natural.",
  "objetivos": "Lograr que los estudiantes desarrollen técnicas de observación, registro y análisis de fenómenos naturales de su entorno inmediato.",
  "metodologia": "Se trabajará mediante talleres prácticos con uso de lupas y microscopios, actividades al aire libre y registro sistemático de observaciones.",
  "grados": "5to Grado, 6to Grado, 7mo Grado",
  "requisitos": "Autorización de padres, ropa cómoda para actividades al aire libre",
  "materiales_presupuesto": "Lupas (10 unidades), microscopios básicos (5 unidades), cuadernos de campo, presupuesto estimado: $15,000",
  "meses": "Octubre, Noviembre, Diciembre",
  "fechas": ["2025-10-15", "2025-11-20", "2025-12-10"],
  "fecha_creacion": "2025-09-29T13:45:23.456789",
  "fecha_modificacion": "2025-09-29T13:45:23.456789",
  "documento_id": "1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M",
  "carpeta_id": "1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI",
  "estado": "procesado"
}
```

## 🔍 **Estados de Procesamiento**

| Estado | Descripción |
|--------|-------------|
| `pendiente` | Formulario guardado pero no procesado aún |
| `procesado` | Formulario procesado exitosamente, documento generado |
| `error` | Error durante el procesamiento, requiere revisión |

## 📊 **Comandos Útiles para Explorar la BD**

```bash
# Explorar contenido completo de la base de datos
python explore_db.py

# Ver esquema detallado
python explore_db.py --schema

# Ver datos de ejemplo
python explore_db.py --sample

# Verificar estado de la base de datos
python init_db.py check

# Contar registros desde SQLite directamente
sqlite3 instance/formularios.db "SELECT COUNT(*) FROM formularios_actividad;"

# Ver últimos 5 formularios
sqlite3 instance/formularios.db "SELECT id, titulo_actividad, docente_responsable, estado, fecha_creacion FROM formularios_actividad ORDER BY fecha_creacion DESC LIMIT 5;"
```

## 🔐 **Privacidad y Seguridad**

### **Datos Sensibles Almacenados:**
- ✅ **Nombres completos** de docentes y equipo
- ✅ **DNIs** de los miembros del equipo
- ✅ **Correos electrónicos** institucionales
- ✅ **Detalles de actividades** educativas

### **Medidas de Seguridad:**
- 🔒 Base de datos SQLite local (no expuesta públicamente)
- 🔒 Permisos restrictivos en archivo de BD
- 🔒 Acceso solo a través de la aplicación Flask
- 🔒 Variables de entorno para credenciales sensibles

## 📈 **Métricas y Análisis Disponibles**

La base de datos permite generar reportes sobre:
- 📊 **Actividades por período** (mensual, anual)
- 📊 **Grados más atendidos**
- 📊 **Docentes más activos**
- 📊 **Meses de mayor actividad**
- 📊 **Estados de procesamiento**
- 📊 **Integración con Google Drive** (éxito/errores)

---

**💡 Esta estructura de datos permite un seguimiento completo del ciclo de vida de las actividades educativas, desde la propuesta inicial hasta la generación de documentos oficiales.**