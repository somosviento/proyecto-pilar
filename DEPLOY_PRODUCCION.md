# Guía de Despliegue en Producción - Servidor Apache

**Fecha:** 3 de octubre de 2025  
**Commit:** d361234  
**Branch:** master

## 📋 Cambios en esta versión

### Nuevas funcionalidades
- ✅ Agregados campos **Email** y **DNI** del docente responsable
- ✅ Validación HTML5 para email
- ✅ Validación de patrón para DNI (7-8 dígitos)
- ✅ Campos obligatorios en formulario y backend
- ✅ Inclusión de nuevos campos en PDFs generados
- ✅ Placeholders para Google Docs: `[[EMAIL_RESPONSABLE]]` y `[[DNI_RESPONSABLE]]`

### Archivos modificados
- `app.py` - Backend actualizado para nuevos campos
- `models.py` - Modelo de base de datos con nuevas columnas
- `templates/formulario.html` - Formulario HTML con nuevos campos
- `utils/pdf_generator.py` - Generación de PDF con email y DNI

### Archivos nuevos
- `migrate_add_email_dni.py` - Script de migración de base de datos
- `CAMBIOS_EMAIL_DNI.md` - Documentación detallada de cambios
- `DEPLOY_PRODUCCION.md` - Esta guía

## 🚀 Pasos para el despliegue

### 1. Conectarse al servidor de producción

```bash
ssh usuario@servidor-produccion
```

### 2. Navegar al directorio del proyecto

```bash
cd /ruta/a/proyecto-pilar
# Ejemplo: cd /var/www/proyecto-pilar
```

### 3. Hacer backup de la base de datos

```bash
# Crear directorio de backups si no existe
mkdir -p backups

# Hacer backup de la base de datos actual con fecha y hora
cp instance/formularios.db backups/formularios_$(date +%Y%m%d_%H%M%S).db

# Verificar que el backup se creó correctamente
ls -lh backups/
```

### 4. Hacer pull de los cambios desde GitHub

```bash
# Verificar el estado actual
git status

# Hacer pull de los cambios
git pull origin master

# Verificar que se descargó el commit correcto
git log --oneline -5
# Debe aparecer: d361234 feat: Agregar campos Email y DNI al formulario del docente responsable
```

### 5. Activar el entorno virtual

```bash
# Si usa virtualenv
source venv/bin/activate

# Si usa otro nombre de entorno virtual, ajustar según corresponda
# source .venv/bin/activate
```

### 6. Instalar/actualizar dependencias (si hubiera cambios)

```bash
pip install -r requirements.txt
```

### 7. **IMPORTANTE: Ejecutar migración de base de datos**

```bash
# Ejecutar el script de migración para agregar las nuevas columnas
python migrate_add_email_dni.py

# Debe ver:
# ✅ Columna email_responsable agregada
# ✅ Columna dni_responsable agregada
# ✅ Migración exitosa. Puede ejecutar la aplicación normalmente.
```

### 8. Verificar la base de datos

```bash
# Verificar que las columnas se agregaron correctamente
python init_db.py check

# Debe mostrar las 19 columnas incluyendo:
# - email_responsable
# - dni_responsable
```

### 9. Actualizar el template de Google Docs (si aplica)

Si está usando un template de Google Docs, agregar los siguientes placeholders donde desee que aparezcan:

- `[[EMAIL_RESPONSABLE]]` - Para el correo electrónico
- `[[DNI_RESPONSABLE]]` - Para el DNI

### 10. Reiniciar el servidor Apache

```bash
# Verificar configuración de Apache
sudo apache2ctl configtest

# Si todo está OK, reiniciar
sudo systemctl restart apache2

# O si usa service
sudo service apache2 restart

# Verificar que Apache esté corriendo
sudo systemctl status apache2
```

### 11. Verificar los logs

```bash
# Ver logs de Apache
sudo tail -f /var/log/apache2/error.log

# Ver logs de la aplicación (si configuró logging)
tail -f /var/log/proyecto-pilar/app.log  # Ajustar ruta según su configuración
```

## ✅ Verificación post-despliegue

### 1. Acceder a la aplicación

Abrir el navegador y acceder a la URL de producción:
```
https://su-dominio.com/pilar
```

### 2. Verificar el formulario

- ✅ Debe mostrar los nuevos campos "Correo electrónico" y "DNI"
- ✅ Los campos deben estar marcados como obligatorios (asterisco rojo)
- ✅ El campo email debe validar formato de correo
- ✅ El campo DNI debe aceptar solo 7-8 dígitos

### 3. Probar el formulario completo

1. Llenar todos los campos del formulario
2. Ingresar un email válido (ej: prueba@uncoma.edu.ar)
3. Ingresar un DNI válido (ej: 12345678)
4. Enviar el formulario
5. Verificar que:
   - Los datos se guarden correctamente
   - El PDF generado incluya email y DNI
   - El documento de Google Docs incluya los campos (si aplica)

### 4. Verificar endpoint de salud

```bash
curl https://su-dominio.com/pilar/health
```

Debe retornar:
```json
{
  "status": "OK",
  "timestamp": "2025-10-03T...",
  "version": "1.0.0"
}
```

## 🔧 Troubleshooting

### Error: "Column not found: email_responsable"

**Causa:** La migración no se ejecutó correctamente.

**Solución:**
```bash
python migrate_add_email_dni.py
sudo systemctl restart apache2
```

### Error: "UNIQUE constraint failed"

**Causa:** Los campos son NOT NULL pero registros antiguos no tienen valores.

**Solución:** La migración permite NULL temporalmente. Los nuevos registros deben tener estos campos.

### Error 500 en el formulario

**Causa:** Posibles errores de configuración o permisos.

**Solución:**
```bash
# Verificar permisos de la base de datos
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db

# Verificar permisos del directorio
sudo chown www-data:www-data instance/
sudo chmod 775 instance/

# Reiniciar Apache
sudo systemctl restart apache2
```

### Los cambios no aparecen

**Causa:** Cache del navegador o Apache mod_wsgi no recargó.

**Solución:**
```bash
# Limpiar cache de navegador (Ctrl + Shift + R)

# Tocar el archivo wsgi para forzar recarga
touch wsgi.py

# O reiniciar Apache
sudo systemctl restart apache2
```

## 📊 Rollback (si es necesario)

Si surge algún problema crítico:

### 1. Restaurar base de datos

```bash
# Detener Apache
sudo systemctl stop apache2

# Restaurar backup
cp backups/formularios_YYYYMMDD_HHMMSS.db instance/formularios.db

# Reiniciar Apache
sudo systemctl start apache2
```

### 2. Volver al commit anterior

```bash
# Ver commits
git log --oneline

# Volver al commit anterior (reemplazar HASH con el hash del commit anterior)
git checkout 2b2f96b

# O hacer un revert
git revert d361234

# Push del revert
git push origin master
```

## 📞 Contacto y soporte

Si encuentra problemas durante el despliegue:

1. Verificar los logs de error
2. Revisar la sección de Troubleshooting
3. Contactar al equipo de desarrollo

## 📝 Checklist de despliegue

- [ ] Backup de base de datos realizado
- [ ] Pull de cambios desde GitHub exitoso
- [ ] Migración de base de datos ejecutada
- [ ] Columnas verificadas en la base de datos
- [ ] Template de Google Docs actualizado (si aplica)
- [ ] Apache reiniciado
- [ ] Formulario accesible en producción
- [ ] Nuevos campos visibles y funcionales
- [ ] Validaciones de email y DNI funcionando
- [ ] Prueba de envío de formulario exitosa
- [ ] PDF generado incluye nuevos campos
- [ ] Logs sin errores
- [ ] Endpoint /health respondiendo OK

## ✨ Notas adicionales

- Los registros antiguos en la base de datos NO tienen email ni DNI (quedan como NULL)
- Solo los NUEVOS formularios requieren estos campos obligatoriamente
- Si necesita completar datos de registros antiguos, contacte al administrador
- Los placeholders de Google Docs son opcionales - solo si usa templates

---

**Estado del despliegue:** ⏳ Pendiente  
**Desplegado por:** _________________  
**Fecha/Hora:** _________________  
**Incidencias:** _________________
