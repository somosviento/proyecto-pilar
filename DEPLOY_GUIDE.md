# 🚀 DESPLIEGUE A PRODUCCIÓN - Octubre 2025

## 📋 Cambios Incluidos en esta Versión

### 1. **Sistema de Períodos (Año + Meses)**
- ❌ Eliminado: Campo `requisitos`
- ❌ Eliminado: Campo `fechas_propuestas`  
- ✅ Agregado: Campo `periodos_json` - Array JSON con formato `[{ano: "2025", meses: ["Marzo"]}, ...]`
- ✅ Actualizado: Campo `meses` - Texto legible (ej: "2025: Marzo, Abril | 2026: Julio")
- ✅ Formulario con selección dinámica de año + meses
- ✅ Soporte multi-año para planificación

### 2. **Campo Departamento/Instituto**
- ✅ Agregado: Campo `departamento` después de "Docente Responsable"
- ✅ Campo opcional para especificar Departamento/Instituto de pertenencia

### 3. **Campo Claustro en Equipo**
- ✅ Agregado: Campo `claustro` en cada integrante del equipo
- ✅ Opciones: Docente, Nodocente, Estudiante, Graduado/a, Investigador/a, Otro
- ✅ Campo condicional "Otro" con texto libre
- ℹ️  Se guarda en el JSON de `equipo_json`, no requiere columna separada

### 4. **Mejoras de UI**
- ✅ Favicon agregado (elimina error 404)
- ✅ Iconos Font Awesome en botones
- ✅ Simplificación de grados a 3 ciclos
- ✅ Grid de 5 meses por fila (excluyendo Enero y Diciembre)

---

## 🔧 PASO A PASO PARA DESPLIEGUE

### **Paso 1: Subir Archivos Actualizados**

#### Archivos Modificados que DEBEN subirse:
```
✅ models.py              - Modelo actualizado con departamento y periodos
✅ app.py                 - Backend con nuevos campos
✅ templates/formulario.html  - Formulario con todos los cambios
✅ migrate_complete.py    - Script de migración v2.0
```

#### Método A: Usando Git (Recomendado)
```bash
# En el servidor
cd /var/www/proyecto-pilar
git pull origin master
```

#### Método B: Usando SCP desde Windows
```powershell
# Desde tu PC Windows
scp models.py usuario@servidor:/var/www/proyecto-pilar/
scp app.py usuario@servidor:/var/www/proyecto-pilar/
scp templates/formulario.html usuario@servidor:/var/www/proyecto-pilar/templates/
scp migrate_complete.py usuario@servidor:/var/www/proyecto-pilar/
```

---

### **Paso 2: Ejecutar Migración en Producción**

```bash
# Conectar al servidor
ssh usuario@servidor
cd /var/www/proyecto-pilar

# Activar entorno virtual
source .venv/bin/activate

# Ejecutar migración completa
python3 migrate_complete.py instance/formularios.db

# Cuando pregunte, escribir: s
```

**¿Qué hace el script?**
- ✅ Crea backup automático con timestamp
- ✅ Elimina columnas obsoletas (requisitos, fechas_propuestas)
- ✅ Agrega nuevas columnas (periodos_json, departamento)
- ✅ Migra todos los datos existentes
- ✅ Verifica que todo se aplicó correctamente

---

### **Paso 3: Actualizar Permisos**

```bash
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db
```

---

### **Paso 4: Reiniciar Apache**

```bash
sudo systemctl restart apache2

# Verificar que Apache inició correctamente
sudo systemctl status apache2
```

---

### **Paso 5: Verificar Funcionamiento**

1. **Abrir navegador**: `https://tu-dominio/proyecto-pilar/`

2. **Probar formulario completo**:
   - ✅ Campo "Departamento/Instituto" visible
   - ✅ Selección de ciclos funciona
   - ✅ Agregar períodos con año y meses funciona
   - ✅ Campo "Claustro" en integrantes del equipo
   - ✅ Campo "Otro" aparece/desaparece según selección

3. **Enviar formulario de prueba**:
   - ✅ Se envía sin errores
   - ✅ Datos se guardan en la base de datos
   - ✅ Sin errores en logs de Apache

4. **Monitorear logs** (opcional):
   ```bash
   sudo tail -f /var/log/apache2/error.log
   ```

---

## 🔙 ROLLBACK (Si algo sale mal)

El script crea backups automáticos. Para restaurar:

```bash
# Ver backups disponibles
ls -lh /var/www/proyecto-pilar/instance/*.backup.*

# Restaurar (reemplaza con tu fecha)
cp /var/www/proyecto-pilar/instance/formularios.db.backup.20251001_143000 \
   /var/www/proyecto-pilar/instance/formularios.db

# Reiniciar Apache
sudo systemctl restart apache2
```

---

## 📊 Estructura de Base de Datos Actualizada

### Campos en `formularios_actividad`:
```
id                    INTEGER PRIMARY KEY
titulo_actividad      TEXT NOT NULL
docente_responsable   VARCHAR(200) NOT NULL
departamento          VARCHAR(200)           ← NUEVO
equipo_json           TEXT                   (incluye claustro)
fundamentacion        TEXT NOT NULL
objetivos             TEXT NOT NULL
metodologia           TEXT NOT NULL
grados                TEXT
materiales_presupuesto TEXT
periodos_json         TEXT                   ← NUEVO (reemplaza fechas_propuestas)
meses                 TEXT                   (texto legible de períodos)
fecha_creacion        DATETIME
fecha_modificacion    DATETIME
documento_id          VARCHAR(100)
carpeta_id            VARCHAR(100)
estado                VARCHAR(50)
```

### Formato de `equipo_json`:
```json
[
  {
    "apellido_nombre": "García, María",
    "dni": "12345678",
    "correo": "garcia@uncoma.edu.ar",
    "claustro": "Docente"
  }
]
```

### Formato de `periodos_json`:
```json
[
  {
    "ano": "2025",
    "meses": ["Marzo", "Abril"]
  },
  {
    "ano": "2026", 
    "meses": ["Mayo", "Junio"]
  }
]
```

---

## 🆘 Troubleshooting

### Error: "table has no column named periodos_json"
```bash
# Verificar que la migración se ejecutó
python3 -c "import sqlite3; conn = sqlite3.connect('instance/formularios.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(formularios_actividad)'); print([row[1] for row in cursor.fetchall()])"

# Si falta periodos_json, ejecutar migración nuevamente
python3 migrate_complete.py instance/formularios.db
```

### Error: "Permission denied"
```bash
sudo chown www-data:www-data instance/formularios.db
sudo chmod 664 instance/formularios.db
sudo systemctl restart apache2
```

### Apache no reinicia
```bash
# Ver el error específico
sudo systemctl status apache2 -l

# Ver logs
sudo tail -n 50 /var/log/apache2/error.log

# Verificar sintaxis
sudo apache2ctl configtest
```

---

## ✅ Checklist de Despliegue

**Antes de empezar:**
- [ ] Backup manual de la base de datos actual
- [ ] Todos los archivos subidos al servidor
- [ ] Acceso SSH con permisos sudo

**Durante el despliegue:**
- [ ] Git pull ejecutado (o archivos subidos manualmente)
- [ ] Migración ejecutada sin errores
- [ ] Backup automático creado
- [ ] Permisos actualizados
- [ ] Apache reiniciado exitosamente

**Después del despliegue:**
- [ ] Formulario carga sin errores
- [ ] Todos los campos nuevos visibles
- [ ] Formulario de prueba enviado exitosamente
- [ ] Datos guardados correctamente en BD
- [ ] Sin errores en logs de Apache
- [ ] Funcionalidad de períodos operativa
- [ ] Campo claustro funciona (muestra "Otro" cuando corresponde)

---

## ⏱️ Tiempo Estimado

- Subir archivos: **5 minutos**
- Ejecutar migración: **2-5 minutos**
- Permisos y restart: **2 minutos**
- Verificación: **5 minutos**
- **Total: 15-20 minutos**

---

## 📞 Contacto y Soporte

Si encuentras problemas:
1. Revisa los logs de Apache
2. Verifica que la migración se completó
3. Confirma permisos de archivos
4. Restaura backup si es necesario

---

**¡Listo para producción!** 🚀
