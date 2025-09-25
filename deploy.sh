#!/bin/bash
# Script de despliegue para Proyecto Pilar en Apache 2
# Ejecutar con: bash deploy.sh

set -e  # Salir si hay algún error

echo "=== SCRIPT DE DESPLIEGUE - PROYECTO PILAR UNCOMA ==="
echo "Configurando aplicación para Apache 2 con basepath /proyecto-pilar"
echo

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "wsgi.py" ]; then
    error "No se encuentra wsgi.py. Asegúrate de ejecutar este script desde el directorio del proyecto."
    exit 1
fi

PROJECT_DIR=$(pwd)
info "Directorio del proyecto: $PROJECT_DIR"

# 1. Verificar dependencias del sistema
info "Verificando dependencias del sistema..."

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    error "Python 3 no está instalado"
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    error "pip3 no está instalado"
    exit 1
fi

# 2. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    info "Creando entorno virtual..."
    python3 -m venv .venv
else
    info "Entorno virtual ya existe"
fi

# 3. Activar entorno virtual e instalar dependencias
info "Activando entorno virtual e instalando dependencias..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Crear directorios necesarios
info "Creando directorios necesarios..."
mkdir -p logs
mkdir -p uploads
mkdir -p instance
mkdir -p static/uploads

# 5. Configurar permisos
info "Configurando permisos..."
chmod +x wsgi.py
chmod 755 logs uploads instance static/uploads
chmod 644 *.py

# 6. Verificar configuración de base de datos
info "Verificando base de datos..."
if [ -f "instance/formularios.db" ]; then
    info "Base de datos ya existe"
else
    warning "Base de datos no existe. Se creará al iniciar la aplicación."
fi

# 7. Configurar archivo de entorno para producción
if [ ! -f ".env" ]; then
    warning "Archivo .env no encontrado"
    echo "¿Deseas crear uno basado en .env.production.example? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        cp .env.production.example .env
        info "Archivo .env creado. ¡IMPORTANTE: Edita .env con tus configuraciones reales!"
    fi
fi

# 8. Probar la aplicación WSGI
info "Probando configuración WSGI..."
if python3 -c "import wsgi; print('WSGI OK')"; then
    info "Configuración WSGI válida"
else
    error "Error en configuración WSGI"
    exit 1
fi

# 9. Mostrar información de configuración de Apache
echo
info "=== CONFIGURACIÓN DE APACHE ==="
echo "Para completar el despliegue, configura Apache con la siguiente información:"
echo
echo "1. Copia la configuración de apache-config.conf a tu sitio de Apache:"
echo "   sudo cp apache-config.conf /etc/apache2/sites-available/proyecto-pilar.conf"
echo
echo "2. Edita la configuración reemplazando '/ruta/al/proyecto/pilar2' con:"
echo "   $PROJECT_DIR"
echo
echo "3. Habilita el sitio:"
echo "   sudo a2ensite proyecto-pilar"
echo
echo "4. Habilita módulos necesarios de Apache:"
echo "   sudo a2enmod wsgi"
echo "   sudo a2enmod rewrite"
echo "   sudo a2enmod headers"
echo "   sudo a2enmod expires"
echo "   sudo a2enmod ssl  # Si usas HTTPS"
echo
echo "5. Reinicia Apache:"
echo "   sudo systemctl restart apache2"
echo
echo "6. Verifica los logs:"
echo "   sudo tail -f /var/log/apache2/pilar_error.log"
echo

# 10. Mostrar URLs de acceso
info "=== URLS DE ACCESO ==="
echo "Una vez configurado Apache, la aplicación estará disponible en:"
echo "- HTTP:  http://tu-dominio.com/proyecto-pilar/"
echo "- HTTPS: https://tu-dominio.com/proyecto-pilar/"
echo

# 11. Verificaciones finales
info "Verificando archivos críticos..."
files_to_check=("wsgi.py" "app.py" "requirements.txt" ".htaccess")
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        info "✓ $file existe"
    else
        error "✗ $file no encontrado"
    fi
done

echo
info "=== DESPLIEGUE COMPLETADO ==="
info "Revisa los pasos de configuración de Apache arriba y edita el archivo .env con tus configuraciones."
warning "¡IMPORTANTE! Cambia la SECRET_KEY en .env antes de usar en producción."
echo

deactivate  # Desactivar entorno virtual