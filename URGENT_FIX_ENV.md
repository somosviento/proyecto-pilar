# 🚨 SOLUCIÓN URGENTE: Variables de entorno no se cargan en producción

## ❌ **Problema identificado en los logs:**
```
[DEBUG] Root folder ID: None
[ERROR] script_url no configurada
```

**Diagnóstico**: Las variables de entorno **NO se están cargando** en el servidor.

## 🔧 **SOLUCIÓN INMEDIATA (Ejecutar en el servidor):**

### **Paso 1: Verificar si existe .env**
```bash
cd /var/www/proyecto-pilar
ls -la .env
```

Si **NO EXISTE**, ejecutar:
```bash
# Crear .env con la configuración correcta
cat > .env << 'EOF'
# Configuración de Flask
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_SECRET_KEY=tu-clave-secreta-muy-segura-para-produccion

# Google Apps Script API
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbyOCTQyZdowgCEPr3yJyz7c-ppRsDJFsQoiplAswZv6Cun7URbvr1V1Tsv4O89tdc-Z/exec
GOOGLE_APPS_SCRIPT_TOKEN=quintral1250

# Google Drive
GOOGLE_DRIVE_ROOT_FOLDER_ID=1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI

# Configuración del template
TEMPLATE_DOC_ID=1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M

# Email
EMAIL_SECRETARIA=secretaria.extension@uncobariloche.com

# Base de datos
DATABASE_URL=sqlite:///instance/formularios.db
EOF

# Configurar permisos
sudo chown www-data:www-data .env
sudo chmod 600 .env
```

### **Paso 2: Verificar que python-dotenv esté instalado**
```bash
cd /var/www/proyecto-pilar
source .venv/bin/activate
pip install python-dotenv
```

### **Paso 3: Probar carga de variables**
```bash
cd /var/www/proyecto-pilar
source .venv/bin/activate
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('GOOGLE_APPS_SCRIPT_URL:', os.getenv('GOOGLE_APPS_SCRIPT_URL'))
print('GOOGLE_DRIVE_ROOT_FOLDER_ID:', os.getenv('GOOGLE_DRIVE_ROOT_FOLDER_ID'))
print('TEMPLATE_DOC_ID:', os.getenv('TEMPLATE_DOC_ID'))
"
```

**Resultado esperado:**
```
GOOGLE_APPS_SCRIPT_URL: https://script.google.com/macros/s/AKfyc...
GOOGLE_DRIVE_ROOT_FOLDER_ID: 1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI
TEMPLATE_DOC_ID: 1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M
```

### **Paso 4: Validar configuración**
```bash
python validate_config.py
```

### **Paso 5: Reiniciar Apache**
```bash
sudo systemctl restart apache2
```

### **Paso 6: Probar el formulario**
Ir a: `https://huayca.crub.uncoma.edu.ar/proyecto-pilar/`

## 🔍 **Si el problema persiste:**

### **Opción A: Forzar recarga de variables en wsgi.py**
Agregar al inicio de `wsgi.py`:
```python
# Forzar carga de variables de entorno
from dotenv import load_dotenv
load_dotenv(override=True)
```

### **Opción B: Variables directas en wsgi.py**
Como solución temporal, agregar directamente en `wsgi.py`:
```python
# Variables temporales hasta resolver problema de .env
os.environ.setdefault('GOOGLE_APPS_SCRIPT_URL', 'https://script.google.com/macros/s/AKfycbyOCTQyZdowgCEPr3yJyz7c-ppRsDJFsQoiplAswZv6Cun7URbvr1V1Tsv4O89tdc-Z/exec')
os.environ.setdefault('GOOGLE_APPS_SCRIPT_TOKEN', 'quintral1250')
os.environ.setdefault('GOOGLE_DRIVE_ROOT_FOLDER_ID', '1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI')
os.environ.setdefault('TEMPLATE_DOC_ID', '1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M')
os.environ.setdefault('EMAIL_SECRETARIA', 'secretaria.extension@uncobariloche.com')
```

## 🎯 **Comandos de diagnóstico rápido:**

```bash
# Ver contenido del .env
cat /var/www/proyecto-pilar/.env

# Ver permisos
ls -la /var/www/proyecto-pilar/.env

# Ver logs en tiempo real
sudo tail -f /var/log/apache2/error.log

# Reiniciar Apache
sudo systemctl restart apache2

# Probar variables desde Python
cd /var/www/proyecto-pilar && source .venv/bin/activate && python -c "
import os
from dotenv import load_dotenv
print('Antes de load_dotenv:', os.getenv('GOOGLE_APPS_SCRIPT_URL'))
load_dotenv()
print('Después de load_dotenv:', os.getenv('GOOGLE_APPS_SCRIPT_URL'))
"
```

---

**🚀 Esta solución debería resolver el problema inmediatamente. El formulario funcionará correctamente una vez que las variables se carguen en producción.**