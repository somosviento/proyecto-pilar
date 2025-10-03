#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración para agregar campos email_responsable y dni_responsable
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Configurar variables de entorno
os.environ.setdefault('FLASK_ENV', 'production')

def migrate_database():
    """Agregar columnas email_responsable y dni_responsable a la tabla existente"""
    try:
        from app import app
        from models import db
        
        print("🔧 Iniciando migración de base de datos...")
        print(f"📁 Directorio del proyecto: {project_dir}")
        
        with app.app_context():
            # Conectar a la base de datos
            connection = db.engine.connect()
            
            # Verificar si las columnas ya existen
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('formularios_actividad')]
            
            print(f"📋 Columnas actuales en formularios_actividad: {columns}")
            
            # Agregar email_responsable si no existe
            if 'email_responsable' not in columns:
                print("➕ Agregando columna email_responsable...")
                connection.execute(db.text(
                    "ALTER TABLE formularios_actividad ADD COLUMN email_responsable VARCHAR(200)"
                ))
                connection.commit()
                print("✅ Columna email_responsable agregada")
            else:
                print("ℹ️  Columna email_responsable ya existe")
            
            # Agregar dni_responsable si no existe
            if 'dni_responsable' not in columns:
                print("➕ Agregando columna dni_responsable...")
                connection.execute(db.text(
                    "ALTER TABLE formularios_actividad ADD COLUMN dni_responsable VARCHAR(20)"
                ))
                connection.commit()
                print("✅ Columna dni_responsable agregada")
            else:
                print("ℹ️  Columna dni_responsable ya existe")
            
            connection.close()
            
            # Verificar que las columnas se agregaron correctamente
            inspector = inspect(db.engine)
            columns_after = [col['name'] for col in inspector.get_columns('formularios_actividad')]
            
            print(f"\n📋 Columnas después de la migración ({len(columns_after)} columnas):")
            for col in columns_after:
                print(f"   - {col}")
            
            print(f"\n🎉 Migración completada exitosamente!")
            
    except Exception as e:
        print(f"❌ Error al migrar la base de datos: {str(e)}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("🗃️  MIGRACIÓN DE BASE DE DATOS - PROYECTO PILAR")
    print("=" * 60)
    print("Agregando campos: email_responsable y dni_responsable")
    print("=" * 60)
    
    success = migrate_database()
    
    if success:
        print("\n✅ Migración exitosa. Puede ejecutar la aplicación normalmente.")
    else:
        print("\n❌ La migración falló. Revise los errores anteriores.")
    
    sys.exit(0 if success else 1)
