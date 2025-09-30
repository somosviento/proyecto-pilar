#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la configuración de la base de datos
Ejecutar como: sudo -u www-data python3 test_database_config.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def test_database_config():
    print("=== PRUEBA DE CONFIGURACIÓN DE BASE DE DATOS ===")
    
    # Cargar variables de entorno como en producción
    try:
        from dotenv import load_dotenv
        env_path = project_dir / '.env'
        load_dotenv(dotenv_path=env_path)
        print(f"✅ Variables de entorno cargadas desde {env_path}")
    except Exception as e:
        print(f"⚠️  Error cargando .env: {e}")
    
    # Configurar variables como en wsgi.py
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ['DATABASE_PATH'] = str(project_dir / 'instance' / 'formularios.db')
    
    print(f"Variables de entorno relevantes:")
    print(f"  FLASK_ENV: {os.getenv('FLASK_ENV')}")
    print(f"  DATABASE_URL: {os.getenv('DATABASE_URL')}")
    print(f"  DATABASE_PATH: {os.getenv('DATABASE_PATH')}")
    
    # Probar importación y configuración de la app
    try:
        from app import app, db
        
        with app.app_context():
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"✅ App importada correctamente")
            print(f"URI de base de datos configurada: {db_uri}")
            
            # Verificar que la URI usa ruta absoluta
            if db_uri.startswith('sqlite:///') and '/' in db_uri[10:]:
                if os.path.isabs(db_uri[10:]):
                    print("✅ URI usa ruta absoluta")
                else:
                    print("⚠️  URI usa ruta relativa")
            
            # Probar conexión
            try:
                db.engine.execute("SELECT 1")
                print("✅ Conexión a la base de datos exitosa")
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
                
                # Verificar permisos del directorio
                db_path = Path(db_uri[10:])  # Remover 'sqlite:///'
                db_dir = db_path.parent
                
                print(f"Verificando directorio: {db_dir}")
                if db_dir.exists():
                    print(f"  ✅ Directorio existe")
                    print(f"  Propietario: {db_dir.stat().st_uid}")
                    print(f"  Permisos: {oct(db_dir.stat().st_mode)}")
                else:
                    print(f"  ❌ Directorio no existe")
                
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Error importando la aplicación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_database_config()
    if success:
        print("\n✅ Configuración de base de datos correcta")
        sys.exit(0)
    else:
        print("\n❌ Problemas en la configuración de base de datos")
        sys.exit(1)