#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para forzar la creación de tablas con el modelo actualizado"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

print("=== Creación de Base de Datos - Proyecto Pilar ===\n")

from app import app, db

# Eliminar bases de datos existentes
for db_file in ['formularios.db', 'instance/formularios.db']:
    if os.path.exists(db_file):
        print(f"🗑️  Eliminando base de datos antigua: {db_file}")
        os.remove(db_file)

# Crear directorio instance si no existe
os.makedirs('instance', exist_ok=True)

with app.app_context():
    print("📋 Creando todas las tablas con el modelo actualizado...")
    db.create_all()
    
    # Verificar la creación
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"\n✅ Tablas creadas: {tables}\n")
    
    if 'formularios_actividad' in tables:
        columns = inspector.get_columns('formularios_actividad')
        print("Estructura de formularios_actividad:")
        for col in columns:
            print(f"  - {col['name']:30s} {str(col['type']):15s}")
        
        # Verificar columnas clave
        col_names = [col['name'] for col in columns]
        print("\n📋 Verificación de columnas:")
        print(f"  ❌ requisitos: {'SÍ existe (ERROR)' if 'requisitos' in col_names else 'NO existe ✅'}")
        print(f"  ❌ fechas_propuestas: {'SÍ existe (ERROR)' if 'fechas_propuestas' in col_names else 'NO existe ✅'}")
        print(f"  ✅ periodos_json: {'SÍ existe ✅' if 'periodos_json' in col_names else 'NO existe (ERROR)'}")
        print(f"  ✅ meses: {'SÍ existe ✅' if 'meses' in col_names else 'NO existe (ERROR)'}")
        
        print("\n✅ Base de datos creada exitosamente con la estructura actualizada!")
    else:
        print("❌ Error: No se pudo crear la tabla formularios_actividad")
