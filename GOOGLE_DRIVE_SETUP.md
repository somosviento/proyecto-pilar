# 🔧 Guía de Configuración de Google Drive - Proyecto Pilar

Esta guía te ayuda a configurar correctamente la integración con Google Drive y Google Apps Script.

## 📋 Requisitos Previos

1. **Cuenta de Google** con acceso a:
   - Google Drive
   - Google Apps Script
   - Google Docs

2. **Permisos necesarios**:
   - Crear y gestionar carpetas en Google Drive
   - Crear y ejecutar Google Apps Scripts
   - Crear y editar documentos de Google Docs

## 🚀 Paso 1: Configurar Google Apps Script

### 1.1 Crear el Script
1. Ir a https://script.google.com/
2. Clic en "Nuevo proyecto"
3. Copiar el contenido completo del archivo `app.gs` del proyecto
4. Pegar en el editor de Google Apps Script
5. Guardar el proyecto con un nombre descriptivo (ej: "Proyecto Pilar API")

### 1.2 Configurar Permisos
1. En el editor, ir a "Servicios" (ícono de +)
2. Agregar los siguientes servicios:
   - **Drive API** (si no está ya habilitado)
   - **Docs API** (si no está ya habilitado)
   - **Gmail API** (para envío de emails)

### 1.3 Desplegar como Aplicación Web
1. Clic en "Desplegar" → "Nueva implementación"
2. En "Tipo", seleccionar "Aplicación web"
3. Configurar:
   - **Descripción**: "API para Proyecto Pilar"
   - **Ejecutar como**: "Yo" (tu cuenta)
   - **Quién tiene acceso**: "Cualquier persona"
4. Clic en "Implementar"
5. **IMPORTANTE**: Copiar la URL de implementación que aparece
   - Ejemplo: `https://script.google.com/macros/s/AKfycbx...xyz123/exec`

### 1.4 Configurar Variables en .env
```bash
# Pegar la URL real del paso anterior
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_ID_REAL_AQUI/exec

# Crear un token de seguridad (contraseña fuerte)
GOOGLE_APPS_SCRIPT_TOKEN=mi-token-super-secreto-2024
```

## 📁 Paso 2: Configurar Google Drive

### 2.1 Crear Carpeta Raíz
1. Ir a https://drive.google.com/
2. Crear nueva carpeta para el proyecto (ej: "Formularios Pilar UNCOMA")
3. Abrir la carpeta creada
4. Copiar el ID de la URL:
   - URL completa: `https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123`
   - ID a copiar: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ123`

### 2.2 Configurar Variable en .env
```bash
# Pegar el ID real de la carpeta
GOOGLE_DRIVE_ROOT_FOLDER_ID=1aBcDeFgHiJkLmNoPqRsTuVwXyZ123
```

## 📄 Paso 3: Crear Template de Google Docs

### 3.1 Crear Documento Template
1. Ir a https://docs.google.com/
2. Crear nuevo documento
3. Crear la estructura del formulario con placeholders:

```
FORMULARIO DE ACTIVIDAD EDUCATIVA

Título de la Actividad: {{TITULO_ACTIVIDAD}}
Docente Responsable: {{DOCENTE_RESPONSABLE}}

FUNDAMENTACIÓN:
{{FUNDAMENTACION}}

OBJETIVOS:
{{OBJETIVOS}}

METODOLOGÍA:
{{METODOLOGIA}}

GRADOS DESTINATARIOS:
{{GRADOS}}

REQUISITOS:
{{REQUISITOS}}

MATERIALES Y PRESUPUESTO:
{{MATERIALES_PRESUPUESTO}}

MESES PROPUESTOS:
{{MESES}}

EQUIPO DE TRABAJO:
{{EQUIPO_TABLE}}

FECHAS PROPUESTAS:
{{FECHAS_LIST}}
```

### 3.2 Obtener ID del Template
1. Con el documento abierto, copiar el ID de la URL:
   - URL completa: `https://docs.google.com/document/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ456/edit`
   - ID a copiar: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ456`

### 3.3 Configurar Variable en .env
```bash
# Pegar el ID real del template
TEMPLATE_DOC_ID=1aBcDeFgHiJkLmNoPqRsTuVwXyZ456
```

## ✅ Paso 4: Validar Configuración

### 4.1 Ejecutar Validación
```bash
# En el servidor/local
cd /ruta/proyecto-pilar
source .venv/bin/activate
python validate_config.py
```

### 4.2 Probar Conexión con Google Drive
```bash
# Probar conexión real
python validate_config.py --test-drive
```

### 4.3 Ejemplo de .env Completo
```bash
# Flask
FLASK_ENV=production
FLASK_SECRET_KEY=mi-clave-secreta-produccion-2024

# Google Apps Script (URLs reales)
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbxH7R...real-id.../exec
GOOGLE_APPS_SCRIPT_TOKEN=mi-token-super-secreto-aleatorio-2024

# Google Drive (IDs reales)
GOOGLE_DRIVE_ROOT_FOLDER_ID=1A2B3C4D5E6F7G8H9I0J_real_folder_id
TEMPLATE_DOC_ID=1K2L3M4N5O6P7Q8R9S0T_real_template_id

# Base de datos
DATABASE_URL=sqlite:///instance/formularios.db

# Email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
```

## 🔧 Troubleshooting

### Error: "script_url no configurada"
- Verificar que `GOOGLE_APPS_SCRIPT_URL` esté en el .env
- Verificar que la URL sea del Google Apps Script desplegado

### Error: "token no configurado" 
- Verificar que `GOOGLE_APPS_SCRIPT_TOKEN` esté en el .env
- El token puede ser cualquier string seguro

### Error: "folder not found"
- Verificar que `GOOGLE_DRIVE_ROOT_FOLDER_ID` sea correcto
- Verificar que la carpeta exista y sea accesible
- Verificar permisos de la carpeta

### Error: "Script execution failed"
- Verificar que el Google Apps Script esté desplegado correctamente
- Verificar que los permisos estén concedidos
- Revisar los logs en Google Apps Script console

### Error: "Template not found"
- Verificar que `TEMPLATE_DOC_ID` sea correcto
- Verificar que el documento template exista y sea accesible
- Verificar que el documento tenga los placeholders correctos

## 📞 Comandos Útiles

```bash
# Validar configuración
python validate_config.py

# Probar conexión Google Drive  
python validate_config.py --test-drive

# Verificar base de datos
python init_db.py check

# Ver logs de aplicación
tail -f logs/pilar.log

# Reiniciar aplicación
sudo systemctl restart apache2
```

## 🎯 Resultado Esperado

Una vez configurado correctamente:

1. ✅ La aplicación puede crear carpetas en Google Drive
2. ✅ Los formularios generan documentos desde el template
3. ✅ Los documentos se guardan en las carpetas correctas
4. ✅ Se envían emails con PDFs adjuntos
5. ✅ No hay errores en los logs

---

**¡Configuración completada!** El sistema está listo para procesar formularios. 🚀