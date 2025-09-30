#!/bin/bash

# Script para corregir permisos de la base de datos SQLite en producción
# Ejecutar como root en el servidor: sudo bash fix_database_permissions.sh

echo "=== Corrigiendo permisos de la base de datos SQLite ==="

PROJECT_PATH="/var/www/proyecto-pilar"
INSTANCE_PATH="$PROJECT_PATH/instance"
DB_FILE="$INSTANCE_PATH/formularios.db"

echo "1. Creando directorio instance/ si no existe..."
mkdir -p "$INSTANCE_PATH"

echo "2. Estableciendo propietario www-data para el directorio del proyecto..."
chown -R www-data:www-data "$PROJECT_PATH"

echo "3. Estableciendo permisos correctos..."
# Directorio del proyecto: lectura y ejecución para todos
chmod 755 "$PROJECT_PATH"

# Directorio instance: lectura, escritura y ejecución para www-data
chmod 755 "$INSTANCE_PATH"

# Si existe el archivo de base de datos, establecer permisos
if [ -f "$DB_FILE" ]; then
    echo "4. Configurando permisos del archivo de base de datos existente..."
    chown www-data:www-data "$DB_FILE"
    chmod 664 "$DB_FILE"
else
    echo "4. El archivo de base de datos no existe aún, se creará automáticamente."
fi

echo "5. Verificando permisos actuales..."
echo "Directorio del proyecto:"
ls -la "$PROJECT_PATH" | grep -E "(instance|wsgi.py|app.py)"

echo "Directorio instance:"
ls -la "$INSTANCE_PATH"

echo "6. Probando creación de archivo de prueba como www-data..."
sudo -u www-data touch "$INSTANCE_PATH/test_permissions.tmp"
if [ $? -eq 0 ]; then
    echo "✅ www-data puede escribir en el directorio instance"
    rm "$INSTANCE_PATH/test_permissions.tmp"
else
    echo "❌ Error: www-data NO puede escribir en el directorio instance"
    exit 1
fi

echo "7. Inicializando la base de datos como www-data..."
cd "$PROJECT_PATH"
sudo -u www-data python3 -c "
import sys
sys.path.insert(0, '/var/www/proyecto-pilar')
from app import app, db
with app.app_context():
    try:
        db.create_all()
        print('✅ Base de datos inicializada correctamente')
    except Exception as e:
        print(f'❌ Error al inicializar base de datos: {e}')
        sys.exit(1)
"

echo "8. Verificando que la base de datos se creó correctamente..."
if [ -f "$DB_FILE" ]; then
    ls -la "$DB_FILE"
    echo "✅ Base de datos creada exitosamente"
else
    echo "❌ Error: No se pudo crear la base de datos"
    exit 1
fi

echo "=== Corrección de permisos completada ==="
echo ""
echo "Próximos pasos:"
echo "1. Reiniciar Apache: sudo systemctl restart apache2"
echo "2. Verificar logs: sudo tail -f /var/log/apache2/error.log"
echo "3. Probar el formulario en el navegador"