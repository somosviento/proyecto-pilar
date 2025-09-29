#!/bin/bash
# Script de diagnóstico completo para resolver el problema de variables de entorno

echo "🔍 DIAGNÓSTICO COMPLETO - PROYECTO PILAR"
echo "=" * 60

SERVER_PATH="/var/www/proyecto-pilar"

# 1. Verificar la existencia del archivo .env
echo "📁 1. VERIFICANDO ARCHIVO .env"
echo "----------------------------------------"
if [ -f "$SERVER_PATH/.env" ]; then
    echo "✅ Archivo .env existe"
    echo "📊 Tamaño: $(wc -c < $SERVER_PATH/.env) bytes"
    echo "🔐 Propietario: $(ls -la $SERVER_PATH/.env | awk '{print $3":"$4}')"
    echo "🔐 Permisos: $(ls -la $SERVER_PATH/.env | awk '{print $1}')"
else
    echo "❌ ARCHIVO .env NO EXISTE"
    echo "📍 Ruta esperada: $SERVER_PATH/.env"
fi
echo

# 2. Verificar contenido del .env (sin mostrar valores sensibles)
echo "📋 2. CONTENIDO DEL .env (VARIABLES CRÍTICAS)"
echo "----------------------------------------"
if [ -f "$SERVER_PATH/.env" ]; then
    echo "Variables de Google encontradas:"
    grep -E "^GOOGLE_|^TEMPLATE_|^EMAIL_" $SERVER_PATH/.env | sed 's/=.*$/=***CONFIGURADO***/' || echo "❌ No se encontraron variables de Google"
    echo
    echo "Variables de Flask encontradas:"
    grep -E "^FLASK_" $SERVER_PATH/.env | sed 's/=.*$/=***CONFIGURADO***/' || echo "⚠️  No se encontraron variables de Flask"
else
    echo "❌ No se puede verificar contenido - archivo no existe"
fi
echo

# 3. Verificar que python-dotenv esté instalado
echo "🐍 3. VERIFICANDO PYTHON-DOTENV"
echo "----------------------------------------"
cd $SERVER_PATH
source .venv/bin/activate
python -c "import dotenv; print('✅ python-dotenv instalado:', dotenv.__version__)" 2>/dev/null || echo "❌ python-dotenv NO instalado"
echo

# 4. Probar carga de variables manualmente
echo "🧪 4. PRUEBA DE CARGA DE VARIABLES"
echo "----------------------------------------"
cat > /tmp/test_env.py << 'EOF'
import os
from dotenv import load_dotenv

print(f"📁 Directorio actual: {os.getcwd()}")
print(f"📁 Archivo .env existe: {os.path.exists('.env')}")

# Cargar variables
load_dotenv()

# Verificar variables críticas
variables = [
    'GOOGLE_APPS_SCRIPT_URL',
    'GOOGLE_APPS_SCRIPT_TOKEN', 
    'GOOGLE_DRIVE_ROOT_FOLDER_ID',
    'TEMPLATE_DOC_ID',
    'EMAIL_SECRETARIA'
]

print("\n🔍 Variables cargadas:")
for var in variables:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {value[:30]}...")
    else:
        print(f"❌ {var}: NO CONFIGURADA")
EOF

python /tmp/test_env.py
rm /tmp/test_env.py
echo

# 5. Verificar logs de WSGI
echo "📝 5. VERIFICANDO LOGS DE WSGI"
echo "----------------------------------------"
echo "Últimas líneas del log de error de Apache:"
tail -n 10 /var/log/apache2/error.log | grep -E "proyecto-pilar|GOOGLE_|ERROR" || echo "⚠️  No se encontraron errores recientes relacionados"
echo

# 6. Verificar configuración de Apache
echo "🌐 6. VERIFICANDO CONFIGURACIÓN DE APACHE"
echo "----------------------------------------"
echo "Procesos WSGI activos:"
ps aux | grep proyecto-pilar | grep -v grep || echo "⚠️  No se encontraron procesos WSGI de proyecto-pilar"
echo

# 7. Sugerencias de solución
echo "💡 7. SUGERENCIAS DE SOLUCIÓN"
echo "----------------------------------------"
if [ ! -f "$SERVER_PATH/.env" ]; then
    echo "🚨 PROBLEMA CRÍTICO: Archivo .env no existe"
    echo "SOLUCIÓN:"
    echo "  1. Copiar .env desde tu máquina local:"
    echo "     scp .env usuario@servidor:$SERVER_PATH/.env"
    echo "  2. Configurar permisos:"
    echo "     sudo chown www-data:www-data $SERVER_PATH/.env"
    echo "     sudo chmod 600 $SERVER_PATH/.env"
else
    echo "✅ Archivo .env existe"
    echo "POSIBLES PROBLEMAS:"
    echo "  1. Variables mal formateadas (espacios, comillas)"
    echo "  2. Problema de codificación de archivo"
    echo "  3. WSGI no reiniciado después de cambios"
fi
echo
echo "PASOS RECOMENDADOS:"
echo "  1. sudo systemctl restart apache2"
echo "  2. Probar formulario nuevamente"
echo "  3. Revisar logs: sudo tail -f /var/log/apache2/error.log"
echo

deactivate