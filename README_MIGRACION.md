# 🚨 SOLUCIÓN COMPLETA AL ERROR DE PRODUCCIÓN

## ❌ Error Actual
```
table formularios_actividad has no column named periodos_json
```

**Causa**: La base de datos en producción tiene estructura antigua, el código tiene estructura nueva.

---

## ✅ SOLUCIÓN PASO A PASO

### 📦 **Paso 1: Preparar Archivos en tu PC**

Los siguientes archivos están listos para subir:
- ✅ `models.py` - Modelo actualizado
- ✅ `app.py` - Backend actualizado
- ✅ `templates/formulario.html` - Formulario con períodos
- ✅ `migrate_production.py` - Script de migración
- ✅ `check_migration_status.py` - Verificación
- ✅ `deploy_production.sh` - Despliegue automático

---

### 🚀 **Paso 2: Subir Archivos al Servidor**

#### **Opción A: Usando PowerShell (Recomendado para Windows)**

1. Edita `upload_to_server.ps1` y configura:
   ```powershell
   $SERVER_USER = "tu_usuario"
   $SERVER_HOST = "tu_servidor.com"
   $SERVER_PATH = "/var/www/proyecto-pilar"
   ```

2. Ejecuta el script:
   ```powershell
   .\upload_to_server.ps1
   ```

#### **Opción B: Manual con scp**

```powershell
# Desde PowerShell en Windows
scp models.py usuario@servidor:/var/www/proyecto-pilar/
scp app.py usuario@servidor:/var/www/proyecto-pilar/
scp templates\formulario.html usuario@servidor:/var/www/proyecto-pilar/templates/
scp migrate_production.py usuario@servidor:/var/www/proyecto-pilar/
scp check_migration_status.py usuario@servidor:/var/www/proyecto-pilar/
scp deploy_production.sh usuario@servidor:/var/www/proyecto-pilar/
```

#### **Opción C: Usando Git**

Si tienes Git configurado en el servidor:
```bash
# En el servidor
cd /var/www/proyecto-pilar
git pull origin master
```

---

### 🔧 **Paso 3: Ejecutar Migración en el Servidor**

#### **Opción A: Automática (Recomendado)**

```bash
# Conectar al servidor
ssh usuario@servidor

# Ir al directorio
cd /var/www/proyecto-pilar

# Dar permisos
chmod +x deploy_production.sh

# Ejecutar script automático
./deploy_production.sh
```

El script hace TODO automáticamente:
- ✅ Activa entorno virtual
- ✅ Verifica archivos
- ✅ Crea backup
- ✅ Ejecuta migración
- ✅ Actualiza permisos
- ✅ Reinicia Apache

#### **Opción B: Manual (Si la automática falla)**

```bash
# 1. Conectar
ssh usuario@servidor
cd /var/www/proyecto-pilar

# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Verificar estado
python3 check_migration_status.py

# 4. Backup manual
cp instance/formularios.db instance/formularios.db.backup_manual

# 5. Ejecutar migración
python3 migrate_production.py instance/formularios.db
# Cuando pregunte, escribir: s

# 6. Permisos
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db

# 7. Reiniciar Apache
sudo systemctl restart apache2
```

---

### ✅ **Paso 4: Verificar que Funciona**

1. **Abrir el navegador**: `https://tu-dominio/proyecto-pilar/`

2. **Probar el formulario**:
   - Completar todos los campos
   - Seleccionar ciclos (Primer/Segundo/Tercer Ciclo)
   - Agregar períodos con años y meses
   - Enviar

3. **Debe funcionar sin errores** ✅

---

### 📊 **Paso 5: Monitorear (Opcional)**

Si quieres ver los logs en tiempo real:

```bash
ssh usuario@servidor
sudo tail -f /var/log/apache2/error.log
```

---

## 🔙 ROLLBACK (Si algo sale mal)

La migración crea backups automáticos:

```bash
# Ver backups disponibles
ls -lh /var/www/proyecto-pilar/instance/*.backup.*

# Restaurar (reemplaza con la fecha correcta)
cp /var/www/proyecto-pilar/instance/formularios.db.backup.20251001_143000 \
   /var/www/proyecto-pilar/instance/formularios.db

# Reiniciar
sudo systemctl restart apache2
```

---

## 🆘 TROUBLESHOOTING

### Error: "Permission denied"
```bash
sudo chown www-data:www-data /var/www/proyecto-pilar/instance/formularios.db
sudo chmod 664 /var/www/proyecto-pilar/instance/formularios.db
sudo systemctl restart apache2
```

### Error: "File not found"
Verifica que subiste todos los archivos:
```bash
ls -la /var/www/proyecto-pilar/migrate_production.py
ls -la /var/www/proyecto-pilar/models.py
ls -la /var/www/proyecto-pilar/app.py
```

### Apache no reinicia
```bash
# Ver el error
sudo systemctl status apache2 -l

# Ver logs
sudo tail -n 50 /var/log/apache2/error.log

# Verificar sintaxis
sudo apache2ctl configtest
```

---

## ⏱️ TIEMPO ESTIMADO

- **Subir archivos**: 2-5 minutos
- **Migración automática**: 5-10 minutos  
- **Migración manual**: 10-15 minutos
- **Total**: 15-20 minutos máximo

---

## 📝 CHECKLIST FINAL

Antes de empezar:
- [ ] Tienes acceso SSH al servidor
- [ ] Tienes permisos sudo en el servidor
- [ ] Archivos actualizados localmente

Después de migrar:
- [ ] ✅ Migración ejecutada sin errores
- [ ] ✅ Apache reiniciado
- [ ] ✅ Formulario probado y funciona
- [ ] ✅ Sin errores en logs

---

## 📞 CONTACTO

Si tienes problemas:
1. Lee `QUICKFIX.md` para soluciones rápidas
2. Revisa `MIGRATION_GUIDE.md` para detalles técnicos
3. Ejecuta `check_migration_status.py` para diagnóstico
4. Revisa logs: `sudo tail -n 100 /var/log/apache2/error.log`

---

**¡Listo! Con esto deberías poder resolver el error en producción.** 🚀
