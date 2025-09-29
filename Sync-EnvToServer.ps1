# Script PowerShell para copiar configuración .env al servidor
# Uso: .\Sync-EnvToServer.ps1 -Server "usuario@servidor"

param(
    [Parameter(Mandatory=$true)]
    [string]$Server
)

$RemotePath = "/var/www/proyecto-pilar"

Write-Host "🔧 SINCRONIZACIÓN DE CONFIGURACIÓN AL SERVIDOR" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "Servidor destino: $Server" -ForegroundColor Yellow
Write-Host "Ruta remota: $RemotePath" -ForegroundColor Yellow
Write-Host ""

# Verificar que existe .env local
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: No se encuentra archivo .env local" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Variables configuradas localmente:" -ForegroundColor Green
Write-Host "────────────────────────────────────"
Get-Content .env | Where-Object { $_ -match "GOOGLE_|TEMPLATE_|EMAIL_" } | ForEach-Object {
    $var = $_.Split('=')[0]
    Write-Host "$var=***configurado***" -ForegroundColor DarkGreen
}
Write-Host ""

# Crear backup del .env remoto actual
Write-Host "💾 Creando backup del .env remoto actual..." -ForegroundColor Blue
$backupDate = Get-Date -Format "yyyyMMdd_HHmmss"
ssh $Server "cd $RemotePath && cp .env .env.backup.$backupDate 2>/dev/null || true"

# Copiar .env al servidor
Write-Host "📤 Copiando configuración al servidor..." -ForegroundColor Blue
scp .env "${Server}:${RemotePath}/.env"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Configuración copiada exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error al copiar configuración" -ForegroundColor Red
    exit 1
}

# Verificar permisos
Write-Host "🔐 Configurando permisos..." -ForegroundColor Blue
ssh $Server "cd $RemotePath && sudo chown www-data:www-data .env && sudo chmod 600 .env"

# Validar configuración remota
Write-Host "🔍 Validando configuración remota..." -ForegroundColor Blue
ssh $Server "cd $RemotePath && source .venv/bin/activate && python validate_config.py"

# Reiniciar Apache
Write-Host "🔄 Reiniciando Apache..." -ForegroundColor Blue
ssh $Server "sudo systemctl restart apache2"

Write-Host ""
Write-Host "🎉 ¡Sincronización completada!" -ForegroundColor Green
Write-Host "💡 La aplicación ya debería funcionar con la nueva configuración" -ForegroundColor Yellow
Write-Host ""
Write-Host "🧪 Para probar:" -ForegroundColor Cyan
Write-Host "   1. Ir a https://huayca.crub.uncoma.edu.ar/proyecto-pilar/" -ForegroundColor White
Write-Host "   2. Llenar y enviar el formulario" -ForegroundColor White
Write-Host "   3. Verificar que se crea la carpeta en Google Drive" -ForegroundColor White