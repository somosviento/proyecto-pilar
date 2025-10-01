#!/bin/bash
# Script de despliegue rápido para producción
# Ejecuta todos los pasos necesarios para aplicar la migración

set -e  # Detener si hay errores

echo "=========================================="
echo "  DESPLIEGUE Y MIGRACIÓN - PROYECTO PILAR"
echo "=========================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra app.py${NC}"
    echo "   Asegúrate de estar en el directorio /var/www/proyecto-pilar"
    exit 1
fi

echo -e "${GREEN}✅ Directorio correcto${NC}"
echo ""

# 1. Activar entorno virtual
echo "📦 Activando entorno virtual..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
else
    echo -e "${RED}❌ No se encuentra el entorno virtual en .venv${NC}"
    exit 1
fi
echo ""

# 2. Verificar archivos actualizados
echo "🔍 Verificando archivos actualizados..."
python3 check_migration_status.py
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Advertencia: Algunos archivos pueden no estar actualizados${NC}"
    read -p "¿Continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
        exit 1
    fi
fi
echo ""

# 3. Ejecutar migración
echo "🚀 Ejecutando migración de base de datos..."
python3 migrate_production.py /var/www/proyecto-pilar/instance/formularios.db

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ La migración falló${NC}"
    exit 1
fi
echo ""

# 4. Verificar permisos
echo "🔐 Verificando permisos de la base de datos..."
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/formularios.db
sudo chmod 664 /var/www/proyecto-pilar/instance/formularios.db
echo -e "${GREEN}✅ Permisos actualizados${NC}"
echo ""

# 5. Reiniciar Apache
echo "🔄 Reiniciando Apache..."
sudo systemctl restart apache2

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Apache reiniciado exitosamente${NC}"
else
    echo -e "${RED}❌ Error al reiniciar Apache${NC}"
    exit 1
fi
echo ""

# 6. Verificar estado de Apache
echo "📊 Verificando estado de Apache..."
sudo systemctl status apache2 --no-pager -l | head -n 10
echo ""

echo "=========================================="
echo -e "${GREEN}✅ DESPLIEGUE COMPLETADO${NC}"
echo "=========================================="
echo ""
echo "📝 Próximos pasos:"
echo "   1. Probar el formulario en el navegador"
echo "   2. Monitorear logs si hay errores:"
echo "      sudo tail -f /var/log/apache2/error.log"
echo ""
echo "🔙 Si algo sale mal, restaurar backup:"
echo "   cd /var/www/proyecto-pilar/instance"
echo "   ls -lh *.backup.*"
echo "   cp formularios.db.backup.YYYYMMDD_HHMMSS formularios.db"
echo "   sudo systemctl restart apache2"
echo ""
