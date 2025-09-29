# 🚀 Guía de Despliegue - Proyecto Pilar UNCOMA

Esta guía detalla cómo desplegar la aplicación **Proyecto Pilar** en un servidor Apache 2 con el basepath `/proyecto-pilar`.

## 📋 Requisitos Previos

### Sistema Operativo
- Ubuntu 20.04+ / CentOS 8+ / Debian 10+
- Acceso root o sudo

### Software Necesario
- **Apache 2.4+** con mod_wsgi
- **Python 3.8+**
- **pip3**
- **Git** (para clonar el repositorio)

### Módulos de Apache Requeridos
```bash
sudo a2enmod wsgi
sudo a2enmod rewrite  
sudo a2enmod headers
sudo a2enmod expires
sudo a2enmod ssl        # Solo si usas HTTPS
```

## 🛠️ Instalación Paso a Paso

### 1. Preparar el Sistema

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y apache2 python3 python3-pip python3-venv libapache2-mod-wsgi-py3 git

# Verificar instalación
python3 --version
apache2 -v
```

### 2. Clonar y Configurar el Proyecto

```bash
# Navegar al directorio web
cd /var/www/

# Clonar el repositorio
sudo git clone <url-del-repositorio> proyecto-pilar
cd proyecto-pilar

# Cambiar propietario
sudo chown -R www-data:www-data /var/www/proyecto-pilar
```

### 3. Ejecutar Script de Despliegue

```bash
# Hacer ejecutable el script
chmod +x deploy.sh

# Ejecutar script de despliegue
sudo -u www-data ./deploy.sh
```

### 4. Configurar Variables de Entorno

```bash
# Copiar y editar archivo de configuración
sudo -u www-data cp .env.production.example .env
sudo -u www-data nano .env
```

**Configurar las siguientes variables en `.env`:**
```bash
# ⚠️ IMPORTANTE: Cambiar estos valores
FLASK_SECRET_KEY=tu-clave-secreta-muy-segura-para-produccion
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_SCRIPT_ID/exec
GOOGLE_APPS_SCRIPT_TOKEN=tu-token-seguro
GOOGLE_DRIVE_ROOT_FOLDER_ID=tu-folder-id
TEMPLATE_DOC_ID=tu-template-doc-id
```

### 5. Configurar Apache Virtual Host

```bash
# Copiar configuración de Apache
sudo cp apache-config.conf /etc/apache2/sites-available/proyecto-pilar.conf

# Editar configuración (reemplazar rutas)
sudo nano /etc/apache2/sites-available/proyecto-pilar.conf
```

**En el archivo, reemplazar todas las instancias de:**
- `/ruta/al/proyecto/pilar2` → `/var/www/proyecto-pilar`
- `tu-dominio.com` → tu dominio real

### 6. Inicializar Base de Datos

```bash
# Cambiar al directorio del proyecto
cd /var/www/proyecto-pilar

# Activar entorno virtual
source .venv/bin/activate

# Inicializar la base de datos
python init_db.py init

# Verificar que las tablas se crearon correctamente
python init_db.py check
```

### 7. Habilitar Sitio y Reiniciar Apache

```bash
# Habilitar sitio  
sudo a2ensite proyecto-pilar

# Deshabilitar sitio por defecto (opcional)
sudo a2dissite 000-default

# Probar configuración
sudo apache2ctl configtest

# Reiniciar Apache
sudo systemctl restart apache2
```

## 🔧 Configuración Detallada

### Estructura de Archivos
```
/var/www/proyecto-pilar/
├── wsgi.py                 # Archivo WSGI principal
├── app.py                  # Aplicación Flask
├── requirements.txt        # Dependencias Python
├── .env                    # Variables de entorno (CREAR)
├── .htaccess              # Configuración adicional Apache
├── apache-config.conf     # Configuración Virtual Host
├── deploy.sh              # Script de despliegue
├── static/                # Archivos estáticos
├── templates/             # Templates HTML
├── instance/              # Base de datos SQLite
├── logs/                  # Logs de aplicación
└── .venv/                 # Entorno virtual Python
```

### URLs de Acceso
- **Desarrollo**: `http://localhost:5000/`
- **Producción**: `http://tu-dominio.com/proyecto-pilar/`

### Configuración de Base de Datos
La aplicación usa SQLite por defecto. La base de datos se crea automáticamente en:
```
/var/www/proyecto-pilar/instance/formularios.db
```

## 🛡️ Configuración de Seguridad

### Permisos de Archivos
```bash
# Configurar permisos correctos
sudo chown -R www-data:www-data /var/www/proyecto-pilar
sudo chmod -R 755 /var/www/proyecto-pilar
sudo chmod -R 644 /var/www/proyecto-pilar/*.py
sudo chmod 600 /var/www/proyecto-pilar/.env
```

### Firewall (UFW)
```bash
sudo ufw allow 'Apache Full'
sudo ufw enable
```

### Headers de Seguridad
Los headers de seguridad están configurados en `apache-config.conf`:
- X-Content-Type-Options
- X-Frame-Options  
- X-XSS-Protection
- Strict-Transport-Security (HTTPS)
- Content-Security-Policy

## 📊 Monitoreo y Logs

### Ubicación de Logs
```bash
# Logs de Apache
sudo tail -f /var/log/apache2/pilar_error.log
sudo tail -f /var/log/apache2/pilar_access.log

# Logs de aplicación
sudo tail -f /var/www/proyecto-pilar/logs/pilar.log
```

### Comandos Útiles
```bash
# Estado de Apache
sudo systemctl status apache2

# Reiniciar Apache
sudo systemctl restart apache2

# Verificar configuración
sudo apache2ctl configtest

# Verificar sitios habilitados
sudo a2ensite
```

## 🔄 Actualización de la Aplicación

```bash
cd /var/www/proyecto-pilar

# Hacer backup de .env
sudo cp .env .env.backup

# Actualizar código
sudo -u www-data git pull origin main

# Actualizar dependencias
sudo -u www-data .venv/bin/pip install -r requirements.txt

# Reiniciar Apache
sudo systemctl restart apache2
```

## 🚨 Troubleshooting

### Error: "No module named 'app'"
```bash
# Verificar permisos y propietario
ls -la /var/www/proyecto-pilar/
sudo chown -R www-data:www-data /var/www/proyecto-pilar/
```

### Error: "Permission denied"
```bash
# Verificar permisos de directorios
sudo chmod 755 /var/www/proyecto-pilar/logs
sudo chmod 755 /var/www/proyecto-pilar/instance
```

### Error: "no such table: formularios_actividad"
```bash
# La base de datos no está inicializada
cd /var/www/proyecto-pilar
source .venv/bin/activate
python init_db.py init

# Verificar que se crearon las tablas
python init_db.py check

# Asegurar permisos correctos
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/formularios.db
sudo chmod 755 /var/www/proyecto-pilar/instance/
sudo chmod 644 /var/www/proyecto-pilar/instance/formularios.db
```

### Error: "Database is locked"
```bash
# Verificar permisos de base de datos
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/formularios.db
sudo chmod 644 /var/www/proyecto-pilar/instance/formularios.db
```

### Error: "Static files not loading"
```bash
# Verificar configuración de archivos estáticos en Apache
sudo nano /etc/apache2/sites-available/proyecto-pilar.conf
# Verificar línea: Alias /proyecto-pilar/static
```

## 📞 Soporte

Para problemas específicos:
1. Revisar logs de Apache y aplicación
2. Verificar configuración de `.env`
3. Confirmar que todos los módulos de Apache estén habilitados
4. Verificar permisos de archivos y directorios

## 🔐 Configuración HTTPS (Recomendado)

Para habilitar HTTPS:
1. Obtener certificado SSL (Let's Encrypt recomendado)
2. Descomentar sección HTTPS en `apache-config.conf`
3. Configurar rutas de certificados
4. Reiniciar Apache

```bash
# Instalar Certbot para Let's Encrypt
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d tu-dominio.com
```

---

**✅ ¡Aplicación desplegada exitosamente!**

La aplicación estará disponible en: `http://tu-dominio.com/proyecto-pilar/`