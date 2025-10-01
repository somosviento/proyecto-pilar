#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración COMPLETA para producción - Proyecto Pilar
Versión: 2.0
Fecha: Octubre 2025

Cambios incluidos:
1. Elimina columnas obsoletas: requisitos, fechas_propuestas
2. Agrega columna: periodos_json (JSON con años y meses)
3. Actualiza columna: meses (texto legible de períodos)
4. Agrega columna: departamento (Departamento/Instituto)
5. Nota: El campo claustro se guarda en equipo_json, no requiere columna nueva
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime

def migrate_complete_database(db_path):
    """
    Migra la base de datos al esquema completo actualizado
    """
    print("=" * 70)
    print("MIGRACIÓN COMPLETA DE BASE DE DATOS - PROYECTO PILAR v2.0")
    print("=" * 70)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base de datos: {db_path}\n")
    
    if not os.path.exists(db_path):
        print(f"❌ ERROR: La base de datos no existe en: {db_path}")
        return False
    
    # Crear backup
    backup_path = f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📦 Creando backup en: {backup_path}")
    
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado exitosamente\n")
    except Exception as e:
        print(f"⚠️  Advertencia: No se pudo crear backup: {e}\n")
    
    # Conectar a la base de datos
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar columnas existentes
        print("📋 Verificando estructura actual...")
        cursor.execute("PRAGMA table_info(formularios_actividad)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        col_names = list(columns.keys())
        print(f"   Columnas encontradas: {len(col_names)}")
        
        # Verificar qué cambios se necesitan
        needs_migration = False
        changes = []
        
        # Verificar cambios de periodos
        if 'periodos_json' not in col_names:
            changes.append("✅ Agregar columna: periodos_json")
            needs_migration = True
        
        if 'requisitos' in col_names:
            changes.append("❌ Eliminar columna: requisitos")
            needs_migration = True
        
        if 'fechas_propuestas' in col_names:
            changes.append("❌ Eliminar columna: fechas_propuestas")
            needs_migration = True
        
        # Verificar cambio de departamento
        if 'departamento' not in col_names:
            changes.append("✅ Agregar columna: departamento")
            needs_migration = True
        
        if not needs_migration:
            print("\n✅ La base de datos ya tiene la estructura actualizada.")
            print("   No se requiere migración.\n")
            conn.close()
            return True
        
        print(f"\n🔧 Cambios a aplicar:")
        for change in changes:
            print(f"   {change}")
        
        print("\n🚀 Iniciando migración...")
        
        # Crear tabla temporal con nueva estructura
        print("   1. Creando tabla temporal con nueva estructura...")
        cursor.execute("""
            CREATE TABLE formularios_actividad_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo_actividad TEXT NOT NULL,
                docente_responsable VARCHAR(200) NOT NULL,
                departamento VARCHAR(200),
                equipo_json TEXT,
                fundamentacion TEXT NOT NULL,
                objetivos TEXT NOT NULL,
                metodologia TEXT NOT NULL,
                grados TEXT,
                materiales_presupuesto TEXT,
                periodos_json TEXT,
                meses TEXT,
                fecha_creacion DATETIME,
                fecha_modificacion DATETIME,
                documento_id VARCHAR(100),
                carpeta_id VARCHAR(100),
                estado VARCHAR(50)
            )
        """)
        
        # Copiar datos (solo columnas que existen en ambas tablas)
        print("   2. Migrando datos existentes...")
        
        # Determinar qué columnas copiar
        new_columns = ['id', 'titulo_actividad', 'docente_responsable', 'equipo_json',
                      'fundamentacion', 'objetivos', 'metodologia', 'grados',
                      'materiales_presupuesto', 'meses', 'fecha_creacion',
                      'fecha_modificacion', 'documento_id', 'carpeta_id', 'estado']
        
        # Agregar departamento si ya existía
        if 'departamento' in col_names:
            new_columns.insert(3, 'departamento')  # Después de docente_responsable
        
        columns_to_copy = [col for col in new_columns if col in col_names]
        columns_str = ', '.join(columns_to_copy)
        
        cursor.execute(f"""
            INSERT INTO formularios_actividad_new ({columns_str})
            SELECT {columns_str}
            FROM formularios_actividad
        """)
        
        rows_migrated = cursor.rowcount
        print(f"   ✅ {rows_migrated} registros migrados")
        
        # Eliminar tabla antigua y renombrar nueva
        print("   3. Actualizando estructura...")
        cursor.execute("DROP TABLE formularios_actividad")
        cursor.execute("ALTER TABLE formularios_actividad_new RENAME TO formularios_actividad")
        
        # Commit cambios
        conn.commit()
        
        # Verificar la nueva estructura
        print("\n📋 Verificando estructura actualizada...")
        cursor.execute("PRAGMA table_info(formularios_actividad)")
        new_cols = {row[1]: row for row in cursor.fetchall()}
        
        verification_ok = True
        
        # Verificar periodos
        if 'periodos_json' not in new_cols:
            print("   ❌ ERROR: Columna 'periodos_json' no fue creada")
            verification_ok = False
        else:
            print("   ✅ Columna 'periodos_json' creada correctamente")
        
        if 'requisitos' in new_cols:
            print("   ❌ ERROR: Columna 'requisitos' no fue eliminada")
            verification_ok = False
        else:
            print("   ✅ Columna 'requisitos' eliminada correctamente")
        
        if 'fechas_propuestas' in new_cols:
            print("   ❌ ERROR: Columna 'fechas_propuestas' no fue eliminada")
            verification_ok = False
        else:
            print("   ✅ Columna 'fechas_propuestas' eliminada correctamente")
        
        # Verificar departamento
        if 'departamento' not in new_cols:
            print("   ❌ ERROR: Columna 'departamento' no fue creada")
            verification_ok = False
        else:
            print("   ✅ Columna 'departamento' creada correctamente")
        
        conn.close()
        
        if verification_ok:
            print("\n" + "=" * 70)
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 70)
            print(f"\n📊 Resumen:")
            print(f"   - Registros migrados: {rows_migrated}")
            print(f"   - Backup guardado en: {backup_path}")
            print(f"   - Base de datos actualizada: {db_path}")
            print("\n📝 Cambios aplicados:")
            print("   ✅ Campo 'periodos_json' agregado (períodos con año+meses)")
            print("   ✅ Campo 'departamento' agregado (Depto/Instituto)")
            print("   ✅ Campo 'requisitos' eliminado")
            print("   ✅ Campo 'fechas_propuestas' eliminado")
            print("   ℹ️  Campo 'claustro' incluido en equipo_json (no requiere columna)")
            print("\n⚠️  IMPORTANTE: Reiniciar Apache para aplicar cambios:")
            print("   sudo systemctl restart apache2")
            print("\n")
            return True
        else:
            print("\n❌ La verificación falló. Revise los errores.")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR durante la migración: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            conn.rollback()
            conn.close()
        except:
            pass
        
        print(f"\n⚠️  Se puede restaurar el backup desde: {backup_path}")
        return False

if __name__ == '__main__':
    # Determinar la ruta de la base de datos
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        # Usar la ruta de producción por defecto
        db_path = '/var/www/proyecto-pilar/instance/formularios.db'
        
        # Si no existe, buscar alternativas
        if not os.path.exists(db_path):
            alternatives = [
                'instance/formularios.db',
                'formularios.db',
                '../instance/formularios.db'
            ]
            
            for alt in alternatives:
                if os.path.exists(alt):
                    db_path = alt
                    break
    
    print(f"\nRuta de base de datos: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"\n❌ ERROR: No se encontró la base de datos en: {db_path}")
        print("\nUso: python migrate_complete.py [ruta_a_base_de_datos]")
        print("Ejemplo: python migrate_complete.py /var/www/proyecto-pilar/instance/formularios.db")
        sys.exit(1)
    
    print("\n⚠️  ADVERTENCIA: Este script modificará la base de datos en producción.")
    print("Se creará un backup automáticamente antes de realizar cambios.")
    
    respuesta = input("\n¿Desea continuar con la migración? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'yes', 'y']:
        success = migrate_complete_database(db_path)
        sys.exit(0 if success else 1)
    else:
        print("\n❌ Migración cancelada por el usuario.")
        sys.exit(0)
