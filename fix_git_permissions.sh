#!/bin/bash
# Script para corregir permisos de Git en el servidor de producción

echo "=== Corrigiendo permisos de Git ==="

# Ir al directorio del proyecto
cd /var/www/proyecto-pilar

# Verificar el propietario actual
echo "Propietario actual del proyecto:"
ls -la | head -5

# Opción 1: Cambiar propietario a huayca (recomendado)
echo ""
echo "Ejecutar como root o con sudo:"
echo "sudo chown -R huayca:huayca /var/www/proyecto-pilar"
echo ""

# Opción 2: Cambiar propietario a www-data y agregar huayca al grupo
echo "O alternativamente (para compartir entre usuarios):"
echo "sudo chown -R www-data:www-data /var/www/proyecto-pilar"
echo "sudo usermod -a -G www-data huayca"
echo "sudo chmod -R g+w /var/www/proyecto-pilar"
echo ""

# Después de cambiar permisos, intentar el pull de nuevo
echo "Después de cambiar permisos, ejecutar:"
echo "git pull origin master"
