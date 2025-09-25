# Formulario de Actividades Educativas UNCOMA

## Descripción
Aplicación web desarrollada con Flask que permite a los docentes de la Universidad Nacional del Comahue completar formularios de actividades educativas. La aplicación genera automáticamente documentos PDF, los almacena en Google Drive y envía notificaciones por email.

## Características
- ✅ Formulario web completo con todos los campos requeridos
- ✅ Manejo de equipos dinámicos de trabajo
- ✅ Captura de firma digital
- ✅ Generación automática de PDF
- ✅ Integración con Google Drive para almacenamiento
- ✅ Envío automático de notificaciones por email
- ✅ Base de datos SQLAlchemy para persistencia
- ✅ Interfaz responsive y moderna

## Estructura del Proyecto
```
proyecto/
├── app.py                    # Aplicación Flask principal
├── app.gs                    # Script Google Apps Script (NO MODIFICAR)
├── models.py                 # Modelos SQLAlchemy
├── requirements.txt          # Dependencias Python
├── .env                      # Variables de entorno (configurar)
├── static/
│   └── doc/
│       └── Grilla Pilar.txt  # Template de referencia
├── templates/
│   └── formulario.html       # Formulario web
└── utils/
    ├── __init__.py
    ├── pdf_generator.py      # Generación de PDFs
    ├── google_drive.py       # Integración con Google Drive
    └── email_sender.py       # Envío de emails
```

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Editar el archivo `.env` con los valores correctos:

```env
# Configuración de Flask
FLASK_SECRET_KEY=tu_clave_secreta_muy_segura_aqui

# Configuración de Base de Datos
DATABASE_URL=sqlite:///formularios.db

# Google Apps Script API
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_SCRIPT_ID/exec
GOOGLE_APPS_SCRIPT_TOKEN=tu_token_de_seguridad_aqui

# Google Drive
GOOGLE_DRIVE_ROOT_FOLDER_ID=tu_id_de_carpeta_raiz

# Configuración de Email
EMAIL_SECRETARIA=secretaria.extension@uncobariloche.com

# Configuración del template (opcional)
TEMPLATE_DOC_ID=id_del_template_en_google_drive
```

### 3. Configurar Google Apps Script
1. El archivo `app.gs` ya está configurado y NO debe modificarse
2. Desplegar el script en Google Apps Script
3. Obtener la URL del script desplegado
4. Configurar un token de seguridad en las propiedades del script
5. Asegurar que las APIs de Google Drive y Gmail estén habilitadas

## Uso

### Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Endpoints disponibles
- `GET /` - Formulario principal
- `POST /enviar_formulario` - Procesar envío del formulario
- `GET /formularios` - Listar todos los formularios (admin)
- `GET /formulario/<id>` - Ver formulario específico
- `GET /health` - Verificación de estado

## Integración con Google Apps Script

La aplicación utiliza las siguientes acciones de la API `app.gs`:

### createFolders
Crea carpetas en Google Drive para organizar los documentos.

### generateDocuments (opcional)
Si se configura `TEMPLATE_DOC_ID`, genera documentos a partir de un template de Google Docs.

### uploadFiles
Sube archivos PDF generados localmente a Google Drive.

### sendEmail
Envía notificaciones por email con el documento adjunto.

## Campos del Formulario

### Campos Obligatorios (*)
- **Título de la Actividad**: Descripción de la actividad educativa
- **Docente Responsable**: Nombre completo del docente a cargo
- **Fundamentación**: Base teórica de la actividad
- **Objetivos o Propósitos**: Metas a alcanzar
- **Metodología**: Enfoque pedagógico a utilizar

### Campos Opcionales
- **Firma del Docente**: Captura digital de firma
- **Equipo**: Lista dinámica de colaboradores (nombre, DNI, email)
- **Grados/Requisitos**: Niveles educativos incluidos
- **Materiales/Presupuesto**: Recursos necesarios
- **Fechas Propuestas**: Múltiples fechas posibles para la actividad

## Flujo de Procesamiento

1. **Captura**: Usuario completa el formulario web
2. **Validación**: Se verifican campos obligatorios
3. **Persistencia**: Datos se guardan en base de datos SQLAlchemy
4. **Carpeta**: Se crea carpeta específica en Google Drive
5. **Documento**: Se genera PDF (local) o documento (template Google Docs)
6. **Almacenamiento**: Archivo se sube a la carpeta de Google Drive
7. **Notificación**: Email automático a secretaría con adjunto
8. **Confirmación**: Usuario recibe confirmación de éxito

## Personalización

### Estilos
Los estilos están incluidos en `templates/formulario.html` y pueden modificarse según necesidades institucionales.

### Template PDF
El generador de PDF en `utils/pdf_generator.py` puede personalizarse para cambiar formato, colores, fuentes, etc.

### Campos del Formulario
Nuevos campos pueden agregarse modificando:
1. `models.py` - Agregar columnas a la base de datos
2. `templates/formulario.html` - Agregar inputs al formulario
3. `app.py` - Incluir en `extraer_datos_formulario()`
4. `utils/pdf_generator.py` - Agregar al template PDF

## Seguridad

- ✅ Token de seguridad para API de Google Apps Script
- ✅ Validación de datos del lado del servidor
- ✅ Manejo seguro de archivos y uploads
- ✅ Variables de entorno para credenciales sensibles

## Limitaciones Actuales

- No hay autenticación de usuarios (se puede agregar)
- No hay panel de administración visual (solo endpoints JSON)
- La firma digital se guarda como imagen base64 (funcional pero básico)

## Contribución

Para contribuir al proyecto:
1. No modificar `app.gs`
2. Mantener la estructura de archivos existente
3. Documentar cambios en este README
4. Probar integración completa antes de desplegar

## Licencia

Proyecto interno de la Universidad Nacional del Comahue.