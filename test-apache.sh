#!/bin/bash
# Script para probar las configuraciones de Apache después de los cambios

echo "=== PROBANDO CONFIGURACIÓN DE PROYECTO PILAR ==="
echo

# Verificar que el servicio esté corriendo
echo "1. Verificando estado de Apache..."
sudo systemctl status apache2 --no-pager -l

echo
echo "2. Probando URLs principales..."

# Probar la aplicación principal
echo "  - Probando aplicación principal:"
curl -I https://huayca.crub.uncoma.edu.ar/proyecto-pilar/ 2>/dev/null | head -1

# Probar archivos estáticos
echo "  - Probando archivos estáticos CSS:"
curl -I https://huayca.crub.uncoma.edu.ar/proyecto-pilar/static/css/formulario-pilar.css 2>/dev/null | head -1

echo "  - Probando archivos estáticos IMG:"
curl -I https://huayca.crub.uncoma.edu.ar/proyecto-pilar/static/img/logo_pilar.jpg 2>/dev/null | head -1

echo
echo "3. Verificando logs de Apache..."
echo "  - Errores recientes:"
sudo tail -n 5 /var/log/apache2/error.log

echo "  - Accesos recientes:"
sudo tail -n 5 /var/log/apache2/access.log | grep proyecto-pilar

echo
echo "4. Verificando configuración Apache..."
sudo apache2ctl configtest

echo
echo "=== COMANDOS ÚTILES ==="
echo "- Reiniciar Apache: sudo systemctl restart apache2"
echo "- Ver logs en tiempo real: sudo tail -f /var/log/apache2/error.log"
echo "- Verificar sintaxis: sudo apache2ctl configtest"