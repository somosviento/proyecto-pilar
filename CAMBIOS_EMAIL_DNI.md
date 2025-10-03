# Cambios: Incorporación de campos Email y DNI

**Fecha:** 3 de octubre de 2025

## Resumen
Se han agregado dos nuevos campos obligatorios al formulario después del campo "Docente Responsable":
- **Correo electrónico** (`email_responsable`)
- **DNI** (`dni_responsable`)

## Archivos modificados

### 1. `templates/formulario.html`
- ✅ Agregados dos nuevos campos en el formulario HTML:
  - Campo de correo electrónico con validación de tipo `email`
  - Campo de DNI con validación de patrón (7-8 dígitos)
- Ambos campos son obligatorios (marcados con asterisco rojo)
- Ubicados justo después del campo "Docente Responsable"

### 2. `models.py`
- ✅ Agregadas dos nuevas columnas a la tabla `formularios_actividad`:
  - `email_responsable` (VARCHAR(200), NOT NULL)
  - `dni_responsable` (VARCHAR(20), NOT NULL)
- ✅ Actualizado el método `to_dict()` para incluir los nuevos campos

### 3. `app.py`
- ✅ Actualizada la función `extraer_datos_formulario()` para capturar los nuevos campos
- ✅ Actualizada la función `validar_datos_requeridos()` para validar que los nuevos campos no estén vacíos
- ✅ Actualizada la función `crear_formulario_db()` para guardar los nuevos campos en la base de datos

### 4. `utils/pdf_generator.py`
- ✅ Actualizado el método `_add_basic_info()` para incluir email y DNI en el PDF generado
- ✅ Actualizado el método `create_template_fields()` para incluir los placeholders:
  - `{{EMAIL_RESPONSABLE}}`
  - `{{DNI_RESPONSABLE}}`

### 5. `migrate_add_email_dni.py` (NUEVO)
- ✅ Script de migración creado para agregar las nuevas columnas a la base de datos existente
- ✅ Migración ejecutada exitosamente

## Base de datos

### Migración exitosa
```
✅ Columna email_responsable agregada
✅ Columna dni_responsable agregada
```

**Total de columnas en `formularios_actividad`:** 19 columnas

## Placeholders para Google Docs Template

Si está usando un template de Google Docs, asegúrese de agregar estos placeholders donde desee que aparezcan los datos:

- `{{EMAIL_RESPONSABLE}}` - Para el correo electrónico del docente responsable
- `{{DNI_RESPONSABLE}}` - Para el DNI del docente responsable

## Validaciones implementadas

1. **Email**: Validación HTML5 de tipo email
2. **DNI**: Validación de patrón para aceptar solo 7-8 dígitos numéricos
3. **Ambos campos son obligatorios** en el formulario y en la validación del backend

## Testing recomendado

1. ✅ Verificar que el formulario muestre los nuevos campos
2. ✅ Intentar enviar el formulario sin completar email o DNI (debe mostrar error)
3. ✅ Intentar ingresar un email inválido (debe mostrar error)
4. ✅ Intentar ingresar un DNI con letras o formato incorrecto (debe mostrar error)
5. ⏳ Completar el formulario correctamente y verificar que:
   - Los datos se guarden en la base de datos
   - Aparezcan en el PDF generado
   - Aparezcan en el documento de Google Docs (si aplica)

## Próximos pasos

1. **Actualizar el template de Google Docs** (si aplica):
   - Agregar los placeholders `{{EMAIL_RESPONSABLE}}` y `{{DNI_RESPONSABLE}}` en el template
   
2. **Actualizar registros existentes** (opcional):
   - Los registros anteriores tendrán estos campos como NULL
   - Si es necesario, se puede crear un script para actualizar registros antiguos

3. **Documentación**:
   - Actualizar el manual de usuario si existe
   - Informar a los usuarios sobre los nuevos campos obligatorios

## Notas técnicas

- Los campos se agregaron en la posición correcta (después de "Docente Responsable")
- La migración es compatible con registros existentes (permite NULL temporalmente)
- El código incluye validación tanto en el frontend (HTML5) como en el backend (Python)
- Los nuevos campos se incluyen automáticamente en los PDFs y documentos generados
