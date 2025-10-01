#!/bin/bash
# Script para resolver conflictos en producción

echo "=== Resolviendo conflictos de Git en producción ==="
echo ""

cd /var/www/proyecto-pilar

# 1. Ver qué archivos tienen cambios locales
echo "1. Verificando cambios locales..."
git status

echo ""
echo "2. Opciones para resolver:"
echo ""
echo "OPCIÓN A - Guardar cambios locales y aplicar los nuevos (RECOMENDADO):"
echo "  git stash"
echo "  git pull origin master"
echo "  git stash pop  # Si quieres recuperar los cambios locales después"
echo ""
echo "OPCIÓN B - Descartar cambios locales completamente:"
echo "  git checkout -- deploy_production.sh"
echo "  git pull origin master"
echo ""
echo "OPCIÓN C - Ver qué cambió localmente antes de decidir:"
echo "  git diff deploy_production.sh"
echo ""

# Mostrar el diff del archivo problemático
echo "=== Cambios locales en deploy_production.sh ==="
git diff deploy_production.sh

echo ""
echo "¿Qué hacer?"
echo "Si esos cambios locales no son importantes, ejecuta:"
echo "  git checkout -- deploy_production.sh && git pull origin master"
