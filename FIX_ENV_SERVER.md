# 🚀 Solución Inmediata: Configurar .env en el Servidor

## ❌ **Problema Identificado:**
El archivo `.env` en el servidor **NO tiene** las variables de Google configuradas.

## ✅ **Tu configuración local está CORRECTA:**
```bash
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbyOCTQyZdowgCEPr3yJyz7c-ppRsDJFsQoiplAswZv6Cun7URbvr1V1Tsv4O89tdc-Z/exec
GOOGLE_APPS_SCRIPT_TOKEN=quintral1250
GOOGLE_DRIVE_ROOT_FOLDER_ID=1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI
TEMPLATE_DOC_ID=1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M
EMAIL_SECRETARIA=secretaria.extension@uncobariloche.com
```

## 🔧 **Solución Manual:**

### **Opción 1: Copiar archivo completo**
```bash
# Desde tu máquina local
scp .env usuario@huayca.crub.uncoma.edu.ar:/var/www/proyecto-pilar/.env

# En el servidor
ssh usuario@huayca.crub.uncoma.edu.ar
cd /var/www/proyecto-pilar
sudo chown www-data:www-data .env
sudo chmod 600 .env
sudo systemctl restart apache2
```

### **Opción 2: Editar manualmente en el servidor**
```bash
# Conectar al servidor
ssh usuario@huayca.crub.uncoma.edu.ar

# Editar .env
cd /var/www/proyecto-pilar
sudo nano .env
```

**Agregar/actualizar estas líneas:**
```bash
# Google Apps Script API
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbyOCTQyZdowgCEPr3yJyz7c-ppRsDJFsQoiplAswZv6Cun7URbvr1V1Tsv4O89tdc-Z/exec
GOOGLE_APPS_SCRIPT_TOKEN=quintral1250

# Google Drive
GOOGLE_DRIVE_ROOT_FOLDER_ID=1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI

# Configuración del template
TEMPLATE_DOC_ID=1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M

# Email
EMAIL_SECRETARIA=secretaria.extension@uncobariloche.com

# Flask para producción
FLASK_ENV=production
FLASK_DEBUG=False
```

**Guardar** (Ctrl+X, Y, Enter en nano)

```bash
# Configurar permisos
sudo chown www-data:www-data .env
sudo chmod 600 .env

# Reiniciar Apache
sudo systemctl restart apache2
```

### **Opción 3: Usar scripts automatizados**

**En PowerShell (Windows):**
```powershell
.\Sync-EnvToServer.ps1 -Server "usuario@huayca.crub.uncoma.edu.ar"
```

**En Bash (Linux/Mac):**
```bash
bash sync_env_to_server.sh usuario@huayca.crub.uncoma.edu.ar
```

## 🧪 **Validar que funciona:**

```bash
# En el servidor, validar configuración
cd /var/www/proyecto-pilar
source .venv/bin/activate
python validate_config.py

# Debería mostrar:
# ✅ GOOGLE_APPS_SCRIPT_URL: https://script.google.com/macros/s/AKfyc...
# ✅ GOOGLE_APPS_SCRIPT_TOKEN: quintral1250
# ✅ GOOGLE_DRIVE_ROOT_FOLDER_ID: 1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI
# ✅ TEMPLATE_DOC_ID: 1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M

# Probar conexión con Google Drive
python validate_config.py --test-drive
```

## 🎯 **Resultado Esperado:**

Después de configurar el `.env` en el servidor:
1. ✅ El formulario se enviará correctamente
2. ✅ Se creará una carpeta en Google Drive
3. ✅ Se generará un documento desde el template
4. ✅ Se enviará el email con el PDF
5. ✅ Aparecerá la página de confirmación

---

**¡Esta es la causa raíz del problema!** Una vez que copies la configuración al servidor, todo debería funcionar perfectamente. 🚀