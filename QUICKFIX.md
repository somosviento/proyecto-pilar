# 🚨 SOLUCIÓN RÁPIDA - Error en Producción

## Error Actual
```
table formularios_actividad has no column named periodos_json
```

## ✅ Solución en 3 Pasos

### Opción A: Automática (Recomendada)

```bash
# 1. Conectar al servidor
ssh usuario@tu-servidor

# 2. Ir al directorio del proyecto
cd /var/www/proyecto-pilar

# 3. Subir archivos actualizados (desde tu máquina local)
# En tu máquina Windows:
scp models.py app.py migrate_production.py check_migration_status.py deploy_production.sh usuario@servidor:/var/www/proyecto-pilar/
scp templates/formulario.html usuario@servidor:/var/www/proyecto-pilar/templates/

# 4. En el servidor, dar permisos de ejecución
chmod +x deploy_production.sh

# 5. Ejecutar script automático
./deploy_production.sh
```

El script `deploy_production.sh` hará automáticamente:
- ✅ Activar entorno virtual
- ✅ Verificar archivos
- ✅ Crear backup de la base de datos
- ✅ Ejecutar migración
- ✅ Actualizar permisos
- ✅ Reiniciar Apache

### Opción B: Manual (Si la opción A falla)

```bash
# 1. Conectar al servidor
ssh usuario@tu-servidor
cd /var/www/proyecto-pilar

# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Verificar estado actual
python3 check_migration_status.py

# 4. Crear backup manual (por seguridad)
cp instance/formularios.db instance/formularios.db.backup_manual

# 5. Ejecutar migración
python3 migrate_production.py instance/formularios.db

# 6. Cuando te pregunte, escribir: s

# 7. Actualizar permisos
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db

# 8. Reiniciar Apache
sudo systemctl restart apache2
```

## ✅ Verificación

Después de aplicar la migración:

1. **Probar el formulario**:
   - Ir a: `https://tu-dominio/proyecto-pilar/`
   - Completar y enviar un formulario de prueba
   - Verificar que no hay errores

2. **Revisar logs** (si hay problemas):
   ```bash
   sudo tail -f /var/log/apache2/error.log
   ```

## 🔙 Rollback (Si algo sale mal)

El script crea automáticamente un backup. Para restaurar:

```bash
# Ver backups disponibles
ls -lh /var/www/proyecto-pilar/instance/*.backup.*

# Restaurar (reemplaza YYYYMMDD_HHMMSS con la fecha del backup)
cp /var/www/proyecto-pilar/instance/formularios.db.backup.20251001_HHMMSS \
   /var/www/proyecto-pilar/instance/formularios.db

# Reiniciar Apache
sudo systemctl restart apache2
```

## 📋 Archivos que Necesitas Subir

Estos archivos DEBEN estar actualizados en el servidor:

- ✅ `models.py` - Nuevo modelo con periodos_json
- ✅ `app.py` - Funciones actualizadas
- ✅ `templates/formulario.html` - Formulario con períodos
- ✅ `migrate_production.py` - Script de migración
- ✅ `check_migration_status.py` - Verificación
- ✅ `deploy_production.sh` - Script automático

## 🆘 Si Nada Funciona

1. Verificar que los archivos están en el servidor
2. Verificar permisos: `ls -la instance/formularios.db`
3. Ver logs completos: `sudo tail -n 200 /var/log/apache2/error.log`
4. Restaurar backup y contactar soporte

## ⏱️ Tiempo Estimado

- Opción A (Automática): 5-10 minutos
- Opción B (Manual): 10-15 minutos
