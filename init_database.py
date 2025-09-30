#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos SQLite
Ejecutar como: sudo -u www-data python3 init_database.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def main():
    print("=== Inicializando Base de Datos Proyecto Pilar ===")
    
    # Verificar directorio instance
    instance_dir = project_dir / 'instance'
    db_file = instance_dir / 'formularios.db'
    
    print(f"Directorio del proyecto: {project_dir}")
    print(f"Directorio instance: {instance_dir}")
    print(f"Archivo de base de datos: {db_file}")
    
    # Crear directorio instance si no existe
    if not instance_dir.exists():
        try:
            instance_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
            print(f"✅ Directorio instance creado: {instance_dir}")
        except Exception as e:
            print(f"❌ Error creando directorio instance: {e}")
            return False
    
    # Verificar permisos de escritura
    try:
        test_file = instance_dir / 'test_permissions.tmp'
        test_file.write_text('test')
        test_file.unlink()
        print("✅ Permisos de escritura verificados")
    except Exception as e:
        print(f"❌ Error de permisos: {e}")
        print("Asegúrate de ejecutar este script como: sudo -u www-data python3 init_database.py")
        return False
    
    # Cargar variables de entorno
    try:
        from dotenv import load_dotenv
        env_path = project_dir / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            print(f"✅ Variables de entorno cargadas desde {env_path}")
        else:
            print(f"⚠️  Archivo .env no encontrado en {env_path}")
    except ImportError:
        print("⚠️  python-dotenv no instalado, continuando sin variables de entorno")
    
    # Configurar variables de entorno para producción (como en wsgi.py)
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ['DATABASE_PATH'] = str(db_file)
    
    # Inicializar la aplicación y base de datos
    try:
        from app import app, db
        
        with app.app_context():
            # Mostrar configuración de la base de datos
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')
            print(f"URI de base de datos: {db_uri}")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
            
            # Verificar que el archivo se creó
            if db_file.exists():
                file_stats = db_file.stat()
                print(f"✅ Archivo de base de datos creado: {db_file}")
                print(f"   Tamaño: {file_stats.st_size} bytes")
                print(f"   Permisos: {oct(file_stats.st_mode)[-3:]}")
            else:
                print("❌ El archivo de base de datos no se creó")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\n=== Inicialización completada exitosamente ===")
        print("Próximos pasos:")
        print("1. Reiniciar Apache: sudo systemctl restart apache2")
        print("2. Verificar logs: sudo tail -f /var/log/apache2/error.log")
        print("3. Probar el formulario en el navegador")
        sys.exit(0)
    else:
        print("\n=== Error en la inicialización ===")
        sys.exit(1)