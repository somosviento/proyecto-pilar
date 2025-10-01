# Guía de Migración para Producción - Proyecto Pilar

## 🚨 Migración Urgente Requerida

La base de datos en producción necesita ser actualizada para soportar la nueva funcionalidad de períodos.

## ❌ Error Actual
```
table formularios_actividad has no column named periodos_json
```

## 📋 Cambios en la Base de Datos

### Eliminados:
- ❌ Campo `requisitos`
- ❌ Campo `fechas_propuestas`

### Agregados:
- ✅ Campo `periodos_json` - Almacena períodos en formato JSON
- ✅ Campo `meses` - Texto legible de los períodos

## 🔧 Pasos para Migrar en Producción

### 1. Conectarse al Servidor
```bash
ssh usuario@tu-servidor
cd /var/www/proyecto-pilar
```

### 2. Activar el Entorno Virtual
```bash
source .venv/bin/activate
```

### 3. Subir Archivos Actualizados
Asegúrate de tener estos archivos actualizados en el servidor:
- `models.py` - Modelo actualizado
- `app.py` - Manejadores actualizados  
- `templates/formulario.html` - Formulario con períodos
- `migrate_production.py` - Script de migración

Puedes usar `scp` o `git pull` según tu método de despliegue:

```bash
# Opción A: Git
git pull origin master

# Opción B: SCP (desde tu máquina local)
scp models.py usuario@servidor:/var/www/proyecto-pilar/
scp app.py usuario@servidor:/var/www/proyecto-pilar/
scp migrate_production.py usuario@servidor:/var/www/proyecto-pilar/
scp templates/formulario.html usuario@servidor:/var/www/proyecto-pilar/templates/
```

### 4. Ejecutar el Script de Migración
```bash
python migrate_production.py /var/www/proyecto-pilar/instance/formularios.db
```

El script:
- ✅ Creará un backup automático de la base de datos
- ✅ Migrará los datos existentes a la nueva estructura
- ✅ Verificará que la migración fue exitosa

### 5. Verificar los Permisos
```bash
# Asegurarse de que www-data pueda acceder a la base de datos
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/formularios.db
sudo chmod 664 /var/www/proyecto-pilar/instance/formularios.db
```

### 6. Reiniciar Apache
```bash
sudo systemctl restart apache2
```

### 7. Verificar que Funciona
Abre el navegador y prueba:
```
https://tu-dominio/proyecto-pilar/
```

Completa un formulario de prueba con:
- Selecciona ciclos (Primer/Segundo/Tercer Ciclo)
- Agrega períodos con año y meses
- Verifica que se envía sin errores

## 🔙 Plan de Rollback (Si algo sale mal)

Si la migración falla, puedes restaurar el backup:

```bash
# El backup se crea automáticamente con formato:
# formularios.db.backup.YYYYMMDD_HHMMSS

# Listar backups disponibles
ls -lh /var/www/proyecto-pilar/instance/*.backup.*

# Restaurar desde backup (reemplaza con la fecha correcta)
cp /var/www/proyecto-pilar/instance/formularios.db.backup.20251001_120000 \
   /var/www/proyecto-pilar/instance/formularios.db

# Reiniciar Apache
sudo systemctl restart apache2
```

## 📝 Verificación Post-Migración

### Verificar estructura de la base de datos:
```bash
sqlite3 /var/www/proyecto-pilar/instance/formularios.db << EOF
.headers on
PRAGMA table_info(formularios_actividad);
EOF
```

Deberías ver:
- ✅ `periodos_json` en la lista
- ❌ `requisitos` NO debe aparecer
- ❌ `fechas_propuestas` NO debe aparecer

### Verificar logs de Apache:
```bash
sudo tail -f /var/log/apache2/error.log
```

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs: `sudo tail -n 100 /var/log/apache2/error.log`
2. Verifica permisos de archivos
3. Confirma que los archivos actualizados están en el servidor
4. Restaura el backup si es necesario

## ✅ Checklist Final

- [ ] Backup creado automáticamente
- [ ] Migración ejecutada sin errores
- [ ] Estructura de base de datos verificada
- [ ] Permisos de archivos correctos
- [ ] Apache reiniciado
- [ ] Formulario probado con datos reales
- [ ] Sin errores en logs de Apache
