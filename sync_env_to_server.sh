#!/bin/bash
# Script para copiar configuración local al servidor
# Uso: bash sync_env_to_server.sh usuario@servidor

if [ $# -eq 0 ]; then
    echo "❌ Error: Debes proporcionar el usuario y servidor"
    echo "Uso: bash sync_env_to_server.sh usuario@servidor"
    echo "Ejemplo: bash sync_env_to_server.sh ubuntu@huayca.crub.uncoma.edu.ar"
    exit 1
fi

SERVER=$1
REMOTE_PATH="/var/www/proyecto-pilar"

echo "🔧 SINCRONIZACIÓN DE CONFIGURACIÓN AL SERVIDOR"
echo "=" * 50
echo "Servidor destino: $SERVER"
echo "Ruta remota: $REMOTE_PATH"
echo

# Verificar que existe .env local
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encuentra archivo .env local"
    exit 1
fi

echo "📋 Variables configuradas localmente:"
echo "────────────────────────────────────"
grep -E "GOOGLE_|TEMPLATE_|EMAIL_" .env | sed 's/=.*$/=***configurado***/'
echo

# Crear backup del .env remoto actual
echo "💾 Creando backup del .env remoto actual..."
ssh $SERVER "cd $REMOTE_PATH && cp .env .env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true"

# Copiar .env al servidor
echo "📤 Copiando configuración al servidor..."
scp .env $SERVER:$REMOTE_PATH/.env

if [ $? -eq 0 ]; then
    echo "✅ Configuración copiada exitosamente"
else
    echo "❌ Error al copiar configuración"
    exit 1
fi

# Verificar permisos
echo "🔐 Configurando permisos..."
ssh $SERVER "cd $REMOTE_PATH && chown www-data:www-data .env && chmod 600 .env"

# Validar configuración remota
echo "🔍 Validando configuración remota..."
ssh $SERVER "cd $REMOTE_PATH && source .venv/bin/activate && python validate_config.py"

# Reiniciar Apache
echo "🔄 Reiniciando Apache..."
ssh $SERVER "sudo systemctl restart apache2"

echo
echo "🎉 ¡Sincronización completada!"
echo "💡 La aplicación ya debería funcionar con la nueva configuración"
echo
echo "🧪 Para probar:"
echo "   1. Ir a https://huayca.crub.uncoma.edu.ar/proyecto-pilar/"
echo "   2. Llenar y enviar el formulario"
echo "   3. Verificar que se crea la carpeta en Google Drive"