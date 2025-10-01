#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar campo departamento a la base de datos
"""

import sqlite3
import os

def agregar_campo_departamento():
    """Agrega el campo departamento a la tabla formularios_actividad"""
    
    # Rutas de base de datos
    db_paths = [
        'formularios.db',
        'instance/formularios.db'
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"\n📋 Actualizando base de datos: {db_path}")
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Verificar si la columna ya existe
                cursor.execute("PRAGMA table_info(formularios_actividad)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'departamento' in columns:
                    print("   ✅ La columna 'departamento' ya existe")
                else:
                    # Agregar la columna
                    cursor.execute("""
                        ALTER TABLE formularios_actividad 
                        ADD COLUMN departamento VARCHAR(200)
                    """)
                    conn.commit()
                    print("   ✅ Columna 'departamento' agregada exitosamente")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("AGREGAR CAMPO DEPARTAMENTO")
    print("=" * 60)
    
    if agregar_campo_departamento():
        print("\n✅ Actualización completada")
    else:
        print("\n❌ Hubo errores durante la actualización")
