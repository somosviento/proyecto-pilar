#!/bin/bash

# Script completo de diagnóstico y corrección para Proyecto Pilar
# Ejecutar como root: sudo bash diagnose_and_fix.sh

set -e  # Terminar en caso de error

PROJECT_PATH="/var/www/proyecto-pilar"
INSTANCE_PATH="$PROJECT_PATH/instance"
DB_FILE="$INSTANCE_PATH/formularios.db"
APACHE_USER="www-data"

echo "================================================================"
echo "          DIAGNÓSTICO Y CORRECCIÓN - PROYECTO PILAR"
echo "================================================================"

# Función para mostrar estado actual
show_status() {
    echo ""
    echo "--- ESTADO ACTUAL DEL SISTEMA ---"
    echo "Usuario actual: $(whoami)"
    echo "Directorio del proyecto: $PROJECT_PATH"
    echo "Directorio instance: $INSTANCE_PATH"
    echo "Archivo de base de datos: $DB_FILE"
    echo ""
}

# Función para verificar permisos
check_permissions() {
    echo "--- VERIFICANDO PERMISOS ---"
    
    if [ -d "$PROJECT_PATH" ]; then
        echo "✅ Directorio del proyecto existe"
        ls -la "$PROJECT_PATH" | head -5
    else
        echo "❌ Directorio del proyecto NO existe: $PROJECT_PATH"
        exit 1
    fi
    
    if [ -d "$INSTANCE_PATH" ]; then
        echo "✅ Directorio instance existe"
        ls -la "$INSTANCE_PATH"
    else
        echo "⚠️  Directorio instance NO existe"
    fi
    
    if [ -f "$DB_FILE" ]; then
        echo "✅ Archivo de base de datos existe"
        ls -la "$DB_FILE"
    else
        echo "⚠️  Archivo de base de datos NO existe"
    fi
    echo ""
}

# Función para corregir permisos
fix_permissions() {
    echo "--- CORRIGIENDO PERMISOS ---"
    
    # Crear directorio instance si no existe
    if [ ! -d "$INSTANCE_PATH" ]; then
        echo "Creando directorio instance..."
        mkdir -p "$INSTANCE_PATH"
    fi
    
    # Establecer propietario correcto
    echo "Estableciendo propietario www-data..."
    chown -R "$APACHE_USER:$APACHE_USER" "$PROJECT_PATH"
    
    # Establecer permisos correctos
    echo "Configurando permisos de directorios..."
    chmod 755 "$PROJECT_PATH"
    chmod 755 "$INSTANCE_PATH"
    
    # Si existe el archivo de BD, configurar permisos
    if [ -f "$DB_FILE" ]; then
        echo "Configurando permisos del archivo de base de datos..."
        chown "$APACHE_USER:$APACHE_USER" "$DB_FILE"
        chmod 664 "$DB_FILE"
    fi
    
    echo "✅ Permisos configurados"
    echo ""
}

# Función para probar permisos
test_permissions() {
    echo "--- PROBANDO PERMISOS ---"
    
    # Probar creación de archivo como www-data
    echo "Probando escritura como $APACHE_USER..."
    sudo -u "$APACHE_USER" touch "$INSTANCE_PATH/test_write.tmp"
    
    if [ $? -eq 0 ]; then
        echo "✅ $APACHE_USER puede escribir en instance/"
        rm -f "$INSTANCE_PATH/test_write.tmp"
    else
        echo "❌ $APACHE_USER NO puede escribir en instance/"
        return 1
    fi
    echo ""
}

# Función para inicializar base de datos
init_database() {
    echo "--- INICIALIZANDO BASE DE DATOS ---"
    
    cd "$PROJECT_PATH"
    
    # Verificar que el script de inicialización existe
    if [ ! -f "init_database.py" ]; then
        echo "❌ Script init_database.py no encontrado"
        return 1
    fi
    
    # Ejecutar inicialización como www-data
    echo "Ejecutando inicialización de base de datos como $APACHE_USER..."
    sudo -u "$APACHE_USER" python3 init_database.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Base de datos inicializada correctamente"
    else
        echo "❌ Error al inicializar la base de datos"
        return 1
    fi
    echo ""
}

# Función para verificar Python y dependencias
check_python_env() {
    echo "--- VERIFICANDO ENTORNO PYTHON ---"
    
    cd "$PROJECT_PATH"
    
    echo "Versión de Python:"
    python3 --version
    
    echo "Verificando dependencias clave..."
    python3 -c "
import sys
modules = ['flask', 'sqlalchemy', 'dotenv', 'requests']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module} instalado')
    except ImportError:
        print(f'❌ {module} NO instalado')
"
    echo ""
}

# Función para verificar configuración Apache
check_apache_config() {
    echo "--- VERIFICANDO CONFIGURACIÓN APACHE ---"
    
    APACHE_SITE="/etc/apache2/sites-available/proyecto-pilar.conf"
    
    if [ -f "$APACHE_SITE" ]; then
        echo "✅ Archivo de configuración Apache existe: $APACHE_SITE"
        echo "Configuración WSGI:"
        grep -n "WSGIScriptAlias\|WSGIDaemonProcess\|DocumentRoot" "$APACHE_SITE" || echo "No se encontraron directivas WSGI"
    else
        echo "❌ Archivo de configuración Apache NO existe: $APACHE_SITE"
    fi
    
    echo "Estado del sitio:"
    a2ensite proyecto-pilar > /dev/null 2>&1 && echo "✅ Sitio habilitado" || echo "⚠️  Sitio no habilitado"
    
    echo "Módulos Apache necesarios:"
    a2enmod wsgi > /dev/null 2>&1 && echo "✅ mod_wsgi habilitado" || echo "❌ mod_wsgi NO habilitado"
    echo ""
}

# Función principal
main() {
    show_status
    check_permissions
    check_python_env
    check_apache_config
    
    echo "--- APLICANDO CORRECCIONES ---"
    fix_permissions
    test_permissions
    
    if [ $? -eq 0 ]; then
        init_database
        
        if [ $? -eq 0 ]; then
            echo "--- REINICIANDO APACHE ---"
            systemctl restart apache2
            
            if [ $? -eq 0 ]; then
                echo "✅ Apache reiniciado correctamente"
            else
                echo "❌ Error al reiniciar Apache"
                exit 1
            fi
            
            echo ""
            echo "================================================================"
            echo "                    ✅ CORRECCIÓN COMPLETADA"
            echo "================================================================"
            echo ""
            echo "Estado final:"
            ls -la "$INSTANCE_PATH"
            echo ""
            echo "Próximos pasos:"
            echo "1. Verificar logs de Apache:"
            echo "   sudo tail -f /var/log/apache2/error.log"
            echo ""
            echo "2. Probar el formulario en el navegador:"
            echo "   http://tu-servidor/proyecto-pilar"
            echo ""
            echo "3. Si hay problemas, verificar logs de la aplicación:"
            echo "   sudo tail -f $PROJECT_PATH/logs/pilar.log"
            
        else
            echo "❌ Error en la inicialización de la base de datos"
            exit 1
        fi
    else
        echo "❌ Error en las pruebas de permisos"
        exit 1
    fi
}

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root"
    echo "Uso: sudo bash diagnose_and_fix.sh"
    exit 1
fi

# Ejecutar función principal
main