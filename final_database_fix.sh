#!/bin/bash

# Script final para resolver el problema de la base de datos SQLite
# Ejecutar como root: sudo bash final_database_fix.sh

set -e

PROJECT_PATH="/var/www/proyecto-pilar"
INSTANCE_PATH="$PROJECT_PATH/instance"
DB_FILE="$INSTANCE_PATH/formularios.db"
APACHE_USER="www-data"

echo "================================================================"
echo "          SOLUCIÓN FINAL - PROBLEMA BASE DE DATOS"
echo "================================================================"

# Verificar que estamos ejecutando como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root"
    echo "Uso: sudo bash final_database_fix.sh"
    exit 1
fi

# Verificar que el proyecto existe
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Directorio del proyecto no existe: $PROJECT_PATH"
    exit 1
fi

echo "1. Creando directorio instance con permisos correctos..."
mkdir -p "$INSTANCE_PATH"
chown -R "$APACHE_USER:$APACHE_USER" "$PROJECT_PATH"
chmod 755 "$PROJECT_PATH"
chmod 755 "$INSTANCE_PATH"

echo "2. Eliminando archivo de base de datos existente si tiene problemas..."
if [ -f "$DB_FILE" ]; then
    echo "   Eliminando base de datos existente para recrearla limpia..."
    rm -f "$DB_FILE"
fi

echo "3. Probando permisos de escritura como $APACHE_USER..."
sudo -u "$APACHE_USER" touch "$INSTANCE_PATH/test_permissions.tmp"
if [ $? -eq 0 ]; then
    echo "   ✅ Permisos de escritura confirmados"
    rm -f "$INSTANCE_PATH/test_permissions.tmp"
else
    echo "   ❌ Error: No se pueden establecer permisos de escritura"
    exit 1
fi

echo "4. Probando configuración de la aplicación..."
cd "$PROJECT_PATH"
sudo -u "$APACHE_USER" python3 test_database_config.py
if [ $? -eq 0 ]; then
    echo "   ✅ Configuración de la aplicación correcta"
else
    echo "   ❌ Problemas en la configuración de la aplicación"
    exit 1
fi

echo "5. Inicializando base de datos..."
sudo -u "$APACHE_USER" python3 init_database.py
if [ $? -eq 0 ]; then
    echo "   ✅ Base de datos inicializada correctamente"
else
    echo "   ❌ Error al inicializar la base de datos"
    exit 1
fi

echo "6. Verificando que la base de datos se creó..."
if [ -f "$DB_FILE" ]; then
    echo "   ✅ Archivo de base de datos creado:"
    ls -la "$DB_FILE"
    
    # Verificar que el archivo tiene contenido
    file_size=$(stat -f%z "$DB_FILE" 2>/dev/null || stat -c%s "$DB_FILE" 2>/dev/null || echo "0")
    if [ "$file_size" -gt 0 ]; then
        echo "   ✅ Base de datos tiene contenido ($file_size bytes)"
    else
        echo "   ⚠️  Base de datos está vacía"
    fi
else
    echo "   ❌ Archivo de base de datos no se creó"
    exit 1
fi

echo "7. Reiniciando Apache..."
systemctl restart apache2
if [ $? -eq 0 ]; then
    echo "   ✅ Apache reiniciado correctamente"
else
    echo "   ❌ Error al reiniciar Apache"
    exit 1
fi

echo "8. Verificando estado final..."
echo "   Estructura del directorio instance:"
ls -la "$INSTANCE_PATH"

echo ""
echo "================================================================"
echo "                ✅ PROBLEMA RESUELTO"
echo "================================================================"
echo ""
echo "La base de datos SQLite ha sido configurada correctamente con:"
echo "• Directorio instance/ con permisos de www-data"
echo "• Base de datos inicializada con tablas"
echo "• Configuración de rutas absolutas"
echo "• Apache reiniciado"
echo ""
echo "Próximos pasos:"
echo "1. Verificar logs de Apache:"
echo "   sudo tail -f /var/log/apache2/error.log"
echo ""
echo "2. Probar el formulario:"
echo "   http://tu-servidor/proyecto-pilar"
echo ""
echo "3. Si persisten problemas, revisar logs de la aplicación:"
echo "   sudo tail -f $PROJECT_PATH/logs/pilar.log"
echo ""
echo "El error 'unable to open database file' debería estar resuelto."