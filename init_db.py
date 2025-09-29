#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialización de base de datos para Proyecto Pilar
Crear las tablas necesarias si no existen
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Configurar variables de entorno
os.environ.setdefault('FLASK_ENV', 'production')

def init_database():
    """Inicializar la base de datos y crear todas las tablas"""
    try:
        from app import app
        from models import db, FormularioActividad
        
        print("🔧 Inicializando base de datos...")
        print(f"📁 Directorio del proyecto: {project_dir}")
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Tablas creadas exitosamente:")
            for table in tables:
                print(f"   - {table}")
                
            # Verificar columnas de la tabla principal
            if 'formularios_actividad' in tables:
                columns = inspector.get_columns('formularios_actividad')
                print(f"\n📋 Columnas en formularios_actividad ({len(columns)} columnas):")
                for col in columns:
                    print(f"   - {col['name']} ({col['type']})")
            
            print(f"\n🎉 Base de datos inicializada correctamente!")
            print(f"📊 Archivo de base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado')}")
            
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False
    
    return True

def check_database():
    """Verificar el estado actual de la base de datos"""
    try:
        from app import app
        from models import db, FormularioActividad
        
        print("🔍 Verificando estado de la base de datos...")
        
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if not tables:
                print("⚠️  No se encontraron tablas en la base de datos")
                return False
            
            print(f"✅ Se encontraron {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table}")
                
            # Intentar contar registros
            try:
                count = FormularioActividad.query.count()
                print(f"📊 Registros en formularios_actividad: {count}")
            except Exception as e:
                print(f"⚠️  Error al consultar registros: {str(e)}")
                
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gestión de base de datos - Proyecto Pilar')
    parser.add_argument('action', choices=['init', 'check'], 
                       help='Acción a realizar: init (inicializar) o check (verificar)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🗃️  GESTIÓN DE BASE DE DATOS - PROYECTO PILAR")
    print("=" * 60)
    
    if args.action == 'init':
        success = init_database()
        sys.exit(0 if success else 1)
    elif args.action == 'check':
        success = check_database()
        sys.exit(0 if success else 1)