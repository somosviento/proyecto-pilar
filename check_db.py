#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar la estructura de la base de datos"""

import sqlite3
import os

db_path = 'formularios.db'

if os.path.exists(db_path):
    print(f"✅ Base de datos encontrada: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tablas en la base de datos:")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\nEstructura de formularios_actividad:")
    cursor.execute("PRAGMA table_info(formularios_actividad)")
    columns = cursor.fetchall()
    
    for col in columns:
        col_id, name, col_type, not_null, default, pk = col
        print(f"  {col_id}. {name:30s} {col_type:15s}")
    
    # Verificar columnas clave
    col_names = [col[1] for col in columns]
    print("\n📋 Verificación de columnas:")
    print(f"  ❌ requisitos: {'SÍ existe (DEBE ELIMINARSE)' if 'requisitos' in col_names else 'NO existe ✅'}")
    print(f"  ❌ fechas_propuestas: {'SÍ existe (DEBE ELIMINARSE)' if 'fechas_propuestas' in col_names else 'NO existe ✅'}")
    print(f"  ✅ periodos_json: {'SÍ existe ✅' if 'periodos_json' in col_names else 'NO existe (DEBE AGREGARSE)'}")
    print(f"  ✅ meses: {'SÍ existe ✅' if 'meses' in col_names else 'NO existe (DEBE AGREGARSE)'}")
    
    conn.close()
else:
    print(f"❌ Base de datos no encontrada: {db_path}")
