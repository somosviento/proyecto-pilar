@echo off
REM Script para subir archivos actualizados al servidor de producción
REM Ejecutar desde PowerShell o CMD en Windows

echo ============================================
echo   SUBIR ARCHIVOS A PRODUCCIÓN
echo ============================================
echo.

REM Configuración - EDITA ESTOS VALORES
set SERVER_USER=tu_usuario
set SERVER_HOST=tu_servidor.com
set SERVER_PATH=/var/www/proyecto-pilar

echo Configuración:
echo   Usuario: %SERVER_USER%
echo   Servidor: %SERVER_HOST%
echo   Ruta: %SERVER_PATH%
echo.

REM Verificar que existe scp (viene con Git for Windows)
where scp >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: scp no encontrado. Instala Git for Windows.
    echo https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ¿Los valores de configuración son correctos? (S/N)
set /p confirm=
if /i not "%confirm%"=="S" (
    echo.
    echo Edita este archivo batch y actualiza las variables:
    echo   SERVER_USER, SERVER_HOST, SERVER_PATH
    pause
    exit /b 1
)

echo.
echo Subiendo archivos...
echo.

REM Subir archivos principales
echo [1/7] Subiendo models.py...
scp models.py %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo [2/7] Subiendo app.py...
scp app.py %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo [3/7] Subiendo formulario.html...
scp templates\formulario.html %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/templates/

echo [4/7] Subiendo migrate_production.py...
scp migrate_production.py %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo [5/7] Subiendo check_migration_status.py...
scp check_migration_status.py %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo [6/7] Subiendo deploy_production.sh...
scp deploy_production.sh %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo [7/7] Subiendo documentación...
scp QUICKFIX.md MIGRATION_GUIDE.md %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%/

echo.
echo ============================================
echo   ARCHIVOS SUBIDOS EXITOSAMENTE
echo ============================================
echo.
echo Próximos pasos en el SERVIDOR:
echo.
echo   ssh %SERVER_USER%@%SERVER_HOST%
echo   cd %SERVER_PATH%
echo   chmod +x deploy_production.sh
echo   ./deploy_production.sh
echo.
pause
