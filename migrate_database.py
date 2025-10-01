#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración de base de datos para Proyecto Pilar
Actualiza la estructura de la base de datos para el nuevo sistema de períodos
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def migrate_database():
    """
    Migra la base de datos a la nueva estructura:
    - Elimina columna 'requisitos'
    - Elimina columna 'fechas_propuestas'
    - Agrega columna 'periodos_json'
    - Actualiza el campo 'meses' para texto legible de períodos
    """
    print("=== Migración de Base de Datos - Proyecto Pilar ===\n")
    
    from app import app, db
    import sqlite3
    
    with app.app_context():
        # Obtener la ruta de la base de datos
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_path = db_uri.replace('sqlite:///', '')
        
        if not os.path.isabs(db_path):
            db_path = os.path.join(project_dir, db_path)
        
        print(f"Base de datos: {db_path}")
        
        if not os.path.exists(db_path):
            print("⚠️  La base de datos no existe. Creando nueva base de datos...")
            db.create_all()
            print("✅ Nueva base de datos creada con la estructura actualizada")
            return
        
        # Conectar directamente con sqlite3 para hacer la migración
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Verificar las columnas existentes
            cursor.execute("PRAGMA table_info(formularios_actividad)")
            columns = {row[1]: row for row in cursor.fetchall()}
            
            print("\nColumnas actuales en la tabla:")
            for col_name in columns.keys():
                print(f"  - {col_name}")
            
            # Crear tabla temporal con la nueva estructura
            print("\n📋 Creando tabla temporal con nueva estructura...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS formularios_actividad_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo_actividad TEXT NOT NULL,
                    docente_responsable VARCHAR(200) NOT NULL,
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
            
            # Copiar datos de la tabla antigua a la nueva (sin requisitos y fechas_propuestas)
            print("📦 Migrando datos existentes...")
            cursor.execute("""
                INSERT INTO formularios_actividad_new 
                (id, titulo_actividad, docente_responsable, equipo_json, 
                 fundamentacion, objetivos, metodologia, grados, 
                 materiales_presupuesto, meses, fecha_creacion, 
                 fecha_modificacion, documento_id, carpeta_id, estado)
                SELECT 
                    id, titulo_actividad, docente_responsable, equipo_json,
                    fundamentacion, objetivos, metodologia, grados,
                    materiales_presupuesto, meses, fecha_creacion,
                    fecha_modificacion, documento_id, carpeta_id, estado
                FROM formularios_actividad
            """)
            
            rows_migrated = cursor.rowcount
            print(f"✅ {rows_migrated} registros migrados")
            
            # Eliminar tabla antigua y renombrar la nueva
            print("🔄 Actualizando estructura de la tabla...")
            cursor.execute("DROP TABLE formularios_actividad")
            cursor.execute("ALTER TABLE formularios_actividad_new RENAME TO formularios_actividad")
            
            conn.commit()
            print("\n✅ Migración completada exitosamente!")
            print("\nCambios aplicados:")
            print("  ❌ Eliminada columna: requisitos")
            print("  ❌ Eliminada columna: fechas_propuestas")
            print("  ✅ Agregada columna: periodos_json")
            print("  ℹ️  Campo 'meses' ahora almacena texto legible de períodos")
            
        except Exception as e:
            conn.rollback()
            print(f"\n❌ Error durante la migración: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            conn.close()
        
        return True

if __name__ == '__main__':
    print("ADVERTENCIA: Este script modificará la estructura de la base de datos.")
    print("Se recomienda hacer un backup antes de continuar.\n")
    
    respuesta = input("¿Desea continuar con la migración? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'yes', 'y']:
        success = migrate_database()
        if success:
            print("\n=== Migración finalizada ===")
            sys.exit(0)
        else:
            print("\n=== Migración falló ===")
            sys.exit(1)
    else:
        print("Migración cancelada por el usuario.")
        sys.exit(0)
