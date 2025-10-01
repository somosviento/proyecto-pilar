# Script PowerShell para subir archivos actualizados al servidor de producción
# Ejecutar: .\upload_to_server.ps1

# ============================================
#   CONFIGURACIÓN - EDITA ESTOS VALORES
# ============================================

$SERVER_USER = "tu_usuario"
$SERVER_HOST = "tu_servidor.com"
$SERVER_PATH = "/var/www/proyecto-pilar"

# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SUBIR ARCHIVOS A PRODUCCIÓN" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuración:" -ForegroundColor Yellow
Write-Host "  Usuario: $SERVER_USER"
Write-Host "  Servidor: $SERVER_HOST"
Write-Host "  Ruta: $SERVER_PATH"
Write-Host ""

# Verificar que existe scp
$scpExists = Get-Command scp -ErrorAction SilentlyContinue
if (-not $scpExists) {
    Write-Host "❌ ERROR: scp no encontrado." -ForegroundColor Red
    Write-Host "   Instala Git for Windows: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar archivos locales
Write-Host "Verificando archivos locales..." -ForegroundColor Cyan
$archivos = @(
    "models.py",
    "app.py",
    "templates\formulario.html",
    "migrate_production.py",
    "check_migration_status.py",
    "deploy_production.sh",
    "QUICKFIX.md",
    "MIGRATION_GUIDE.md"
)

$faltantes = @()
foreach ($archivo in $archivos) {
    if (-not (Test-Path $archivo)) {
        $faltantes += $archivo
        Write-Host "  ❌ $archivo - NO EXISTE" -ForegroundColor Red
    } else {
        Write-Host "  ✅ $archivo" -ForegroundColor Green
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Faltan archivos. No se puede continuar." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
$confirm = Read-Host "¿Deseas subir estos archivos al servidor? (S/N)"

if ($confirm -ne "S" -and $confirm -ne "s") {
    Write-Host "Operación cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Subiendo archivos..." -ForegroundColor Cyan
Write-Host ""

$remote = "$SERVER_USER@${SERVER_HOST}:$SERVER_PATH"

try {
    Write-Host "[1/7] Subiendo models.py..." -ForegroundColor Yellow
    scp models.py "$remote/"
    
    Write-Host "[2/7] Subiendo app.py..." -ForegroundColor Yellow
    scp app.py "$remote/"
    
    Write-Host "[3/7] Subiendo formulario.html..." -ForegroundColor Yellow
    scp templates\formulario.html "$remote/templates/"
    
    Write-Host "[4/7] Subiendo migrate_production.py..." -ForegroundColor Yellow
    scp migrate_production.py "$remote/"
    
    Write-Host "[5/7] Subiendo check_migration_status.py..." -ForegroundColor Yellow
    scp check_migration_status.py "$remote/"
    
    Write-Host "[6/7] Subiendo deploy_production.sh..." -ForegroundColor Yellow
    scp deploy_production.sh "$remote/"
    
    Write-Host "[7/7] Subiendo documentación..." -ForegroundColor Yellow
    scp QUICKFIX.md "$remote/"
    scp MIGRATION_GUIDE.md "$remote/"
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  ✅ ARCHIVOS SUBIDOS EXITOSAMENTE" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Próximos pasos en el SERVIDOR:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ssh $SERVER_USER@$SERVER_HOST" -ForegroundColor White
    Write-Host "  cd $SERVER_PATH" -ForegroundColor White
    Write-Host "  chmod +x deploy_production.sh" -ForegroundColor White
    Write-Host "  ./deploy_production.sh" -ForegroundColor White
    Write-Host ""
    
    # Opcional: Conectar automáticamente al servidor
    $conectar = Read-Host "¿Conectar al servidor ahora? (S/N)"
    if ($conectar -eq "S" -or $conectar -eq "s") {
        Write-Host ""
        Write-Host "Conectando al servidor..." -ForegroundColor Cyan
        ssh "$SERVER_USER@$SERVER_HOST" -t "cd $SERVER_PATH && bash"
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR al subir archivos: $_" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Read-Host "Presiona Enter para salir"
