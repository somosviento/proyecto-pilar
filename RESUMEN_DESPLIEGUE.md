# 🚀 RESUMEN DE DESPLIEGUE - PROYECTO PILAR

## ✅ Cambios listos para producción

**Fecha:** 3 de octubre de 2025  
**Commits realizados:** 2  
**Estado:** ✅ **Pusheado a GitHub**

---

## 📦 Commits realizados

### 1. Commit principal (d361234)
```
feat: Agregar campos Email y DNI al formulario del docente responsable

- Agregados campos email_responsable y dni_responsable después de Docente Responsable
- Actualizada base de datos con nuevas columnas (migración incluida)
- Campos obligatorios con validación HTML5 (email) y patrón (DNI 7-8 dígitos)
- Actualizado PDF generator para incluir nuevos campos
- Actualizado template fields para Google Docs con placeholders EMAIL_RESPONSABLE y DNI_RESPONSABLE
- Incluye script de migración migrate_add_email_dni.py (ya ejecutado)
- Documentación de cambios en CAMBIOS_EMAIL_DNI.md
```

**Archivos modificados:**
- ✅ `app.py` - Backend actualizado
- ✅ `models.py` - Modelo de BD con nuevas columnas
- ✅ `templates/formulario.html` - Formulario HTML
- ✅ `utils/pdf_generator.py` - Generación de PDF
- ✅ `migrate_add_email_dni.py` - Script de migración (NUEVO)
- ✅ `CAMBIOS_EMAIL_DNI.md` - Documentación (NUEVO)

### 2. Commit de documentación (749b564)
```
docs: Agregar guía de despliegue en producción con Apache

- Instrucciones paso a paso para despliegue
- Checklist de verificación
- Sección de troubleshooting
- Procedimiento de rollback si es necesario
```

**Archivos agregados:**
- ✅ `DEPLOY_PRODUCCION.md` - Guía completa de despliegue

---

## 🔍 Verificación del repositorio

### Estado de Git
```
✅ Branch: master
✅ Todos los cambios commiteados
✅ Push exitoso a origin/master
✅ No hay archivos pendientes
```

### Verificar en GitHub
URL del repositorio: https://github.com/somosviento/proyecto-pilar

Commits más recientes que debes ver:
1. `749b564` - docs: Agregar guía de despliegue en producción con Apache
2. `d361234` - feat: Agregar campos Email y DNI al formulario del docente responsable

---

## 🎯 PASOS INMEDIATOS PARA PRODUCCIÓN

### Opción A: Despliegue desde el servidor (RECOMENDADO)

Conectarse al servidor y ejecutar:

```bash
# 1. Conectar al servidor
ssh usuario@servidor-produccion

# 2. Ir al directorio del proyecto
cd /ruta/a/proyecto-pilar

# 3. HACER BACKUP DE LA BASE DE DATOS (IMPORTANTE)
mkdir -p backups
cp instance/formularios.db backups/formularios_$(date +%Y%m%d_%H%M%S).db

# 4. Hacer pull de los cambios
git pull origin master

# 5. Activar entorno virtual
source venv/bin/activate  # o .venv/bin/activate según tu configuración

# 6. EJECUTAR MIGRACIÓN DE BASE DE DATOS (CRÍTICO)
python migrate_add_email_dni.py

# 7. Verificar que se agregaron las columnas
python init_db.py check

# 8. Reiniciar Apache
sudo systemctl restart apache2

# 9. Verificar logs
sudo tail -f /var/log/apache2/error.log
```

### Opción B: Despliegue manual (si no tienes acceso SSH)

1. Descargar el código desde GitHub
2. Subir archivos al servidor vía FTP/SFTP
3. Ejecutar migración desde el panel de control del hosting
4. Reiniciar el servidor web

---

## ⚠️ IMPORTANTE - MIGRACIÓN DE BASE DE DATOS

**ES CRÍTICO ejecutar el script de migración:**

```bash
python migrate_add_email_dni.py
```

Este script agrega las columnas necesarias:
- `email_responsable` (VARCHAR 200)
- `dni_responsable` (VARCHAR 20)

**Si no ejecutas la migración, la aplicación fallará con errores de columna no encontrada.**

---

## 📋 Checklist de despliegue

Antes de considerar el despliegue completo, verificar:

- [ ] **Backup de base de datos realizado** ⚠️ MUY IMPORTANTE
- [ ] Git pull ejecutado correctamente
- [ ] Migración de BD ejecutada (`migrate_add_email_dni.py`)
- [ ] Columnas verificadas en la BD
- [ ] Apache reiniciado sin errores
- [ ] Formulario accesible en el navegador
- [ ] Nuevos campos Email y DNI visibles
- [ ] Validación de email funciona (probar con email inválido)
- [ ] Validación de DNI funciona (probar con letras)
- [ ] Prueba de envío de formulario completo
- [ ] PDF generado incluye email y DNI
- [ ] Verificar logs sin errores
- [ ] Endpoint `/health` responde OK

---

## 🔧 Actualización del Template de Google Docs (Opcional)

Si usas un template de Google Docs, agregar estos placeholders:

- `[[EMAIL_RESPONSABLE]]` - Correo electrónico del docente
- `[[DNI_RESPONSABLE]]` - DNI del docente

**Ubicación sugerida:** Justo después de `[[DOCENTE_RESPONSABLE]]`

---

## 📞 En caso de problemas

### Error más común: "Column not found: email_responsable"

**Solución:**
```bash
python migrate_add_email_dni.py
sudo systemctl restart apache2
```

### La aplicación no inicia

**Verificar:**
```bash
# Logs de Apache
sudo tail -50 /var/log/apache2/error.log

# Permisos de la base de datos
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db

# Reiniciar Apache
sudo systemctl restart apache2
```

### Los cambios no se ven

**Solución:**
```bash
# Forzar recarga de WSGI
touch wsgi.py

# Limpiar cache del navegador
# Presionar Ctrl + Shift + R en el navegador

# Reiniciar Apache
sudo systemctl restart apache2
```

---

## 🔄 Rollback (si algo sale mal)

### 1. Restaurar base de datos
```bash
sudo systemctl stop apache2
cp backups/formularios_YYYYMMDD_HHMMSS.db instance/formularios.db
sudo systemctl start apache2
```

### 2. Volver al commit anterior
```bash
git checkout 2b2f96b  # Commit anterior a los cambios
git push origin master --force  # Solo si es necesario
```

---

## 📊 Monitoreo post-despliegue

Después del despliegue, monitorear durante las primeras horas:

1. **Logs de Apache:** `sudo tail -f /var/log/apache2/error.log`
2. **Formularios enviados:** Verificar que se guarden correctamente
3. **PDFs generados:** Verificar que incluyan email y DNI
4. **Emails enviados:** Verificar que lleguen correctamente
5. **Performance:** Verificar que no haya degradación

---

## 📝 Notas finales

- Los registros **antiguos** en la BD no tienen email/DNI (quedan NULL)
- Solo los **nuevos** formularios requieren estos campos
- La aplicación es **compatible** con registros antiguos
- Si necesitas completar datos antiguos, contacta al administrador
- La migración es **idempotente** (puede ejecutarse varias veces sin problemas)

---

## ✅ Estado actual

**Código:** ✅ Pusheado a GitHub  
**Documentación:** ✅ Completa  
**Migración BD:** ✅ Preparada  
**Guía despliegue:** ✅ Disponible  
**Listo para producción:** ✅ SÍ

---

**Próximo paso:** Conectarse al servidor de producción y seguir los pasos del despliegue.

**Tiempo estimado:** 10-15 minutos (incluyendo verificaciones)

**Riesgo:** BAJO (incluye rollback y backups)

---

¿Necesitas ayuda con el despliegue? Consulta `DEPLOY_PRODUCCION.md` para instrucciones detalladas.
