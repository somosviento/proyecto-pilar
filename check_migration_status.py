#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pre-verificación para la migración
Verifica el estado actual y los archivos necesarios
"""

import os
import sys
import sqlite3
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica si un archivo existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"  {status} {description}: {filepath}")
    return exists

def check_database(db_path):
    """Verifica el estado de la base de datos"""
    print("\n📋 Estado de la Base de Datos:")
    print(f"   Ubicación: {db_path}")
    
    if not os.path.exists(db_path):
        print("   ❌ La base de datos NO existe")
        return False
    
    print("   ✅ La base de datos existe")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener columnas
        cursor.execute("PRAGMA table_info(formularios_actividad)")
        columns = {row[1]: row for row in cursor.fetchall()}
        col_names = list(columns.keys())
        
        print(f"   📊 Columnas encontradas: {len(col_names)}")
        
        # Verificar estado
        needs_migration = False
        
        print("\n   🔍 Verificación de estructura:")
        
        if 'periodos_json' in col_names:
            print("      ✅ periodos_json: Ya existe (migración ya aplicada)")
        else:
            print("      ❌ periodos_json: NO existe (NECESITA MIGRACIÓN)")
            needs_migration = True
        
        if 'requisitos' in col_names:
            print("      ⚠️  requisitos: Existe (DEBE ELIMINARSE en migración)")
            needs_migration = True
        else:
            print("      ✅ requisitos: No existe")
        
        if 'fechas_propuestas' in col_names:
            print("      ⚠️  fechas_propuestas: Existe (DEBE ELIMINARSE en migración)")
            needs_migration = True
        else:
            print("      ✅ fechas_propuestas: No existe")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM formularios_actividad")
        count = cursor.fetchone()[0]
        print(f"\n   📊 Registros en la base de datos: {count}")
        
        conn.close()
        
        return needs_migration
        
    except Exception as e:
        print(f"   ❌ Error al verificar base de datos: {e}")
        return False

def main():
    print("=" * 70)
    print("PRE-VERIFICACIÓN DE MIGRACIÓN - PROYECTO PILAR")
    print("=" * 70)
    
    # Detectar si estamos en producción o desarrollo
    is_production = os.path.exists('/var/www/proyecto-pilar')
    
    if is_production:
        print("\n🖥️  Entorno: PRODUCCIÓN")
        base_path = '/var/www/proyecto-pilar'
        db_path = '/var/www/proyecto-pilar/instance/formularios.db'
    else:
        print("\n💻 Entorno: DESARROLLO")
        base_path = os.getcwd()
        db_path = os.path.join(base_path, 'instance', 'formularios.db')
        if not os.path.exists(db_path):
            db_path = os.path.join(base_path, 'formularios.db')
    
    print(f"   Ruta base: {base_path}")
    
    # Verificar archivos críticos
    print("\n📁 Archivos Críticos:")
    
    files_ok = True
    files_ok &= check_file_exists(os.path.join(base_path, 'app.py'), 'Aplicación principal')
    files_ok &= check_file_exists(os.path.join(base_path, 'models.py'), 'Modelos de datos')
    files_ok &= check_file_exists(os.path.join(base_path, 'templates/formulario.html'), 'Formulario HTML')
    files_ok &= check_file_exists(os.path.join(base_path, 'migrate_production.py'), 'Script de migración')
    
    # Verificar base de datos
    needs_migration = check_database(db_path)
    
    # Verificar permisos (solo en Linux)
    if is_production and os.name != 'nt':
        print("\n🔐 Permisos de Archivos:")
        
        try:
            import stat
            st = os.stat(db_path)
            mode = stat.filemode(st.st_mode)
            print(f"   Base de datos: {mode}")
            
            # Verificar propietario
            import pwd
            owner = pwd.getpwuid(st.st_uid).pw_name
            print(f"   Propietario: {owner}")
            
            if owner != 'www-data':
                print("   ⚠️  ADVERTENCIA: El propietario debería ser 'www-data'")
                print("   Ejecutar: sudo chown www-data:www-data", db_path)
        except Exception as e:
            print(f"   ℹ️  No se pudieron verificar permisos: {e}")
    
    # Resumen y recomendaciones
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    
    if not files_ok:
        print("\n❌ Faltan archivos críticos. Sube todos los archivos antes de migrar.")
        return False
    
    if needs_migration:
        print("\n⚠️  MIGRACIÓN NECESARIA")
        print("\n📝 Pasos siguientes:")
        print("   1. Crear backup manual (opcional pero recomendado):")
        if is_production:
            print(f"      cp {db_path} {db_path}.manual_backup")
        else:
            print(f"      copy instance\\formularios.db instance\\formularios.db.backup")
        
        print("\n   2. Ejecutar migración:")
        if is_production:
            print(f"      python migrate_production.py {db_path}")
        else:
            print("      python migrate_production.py")
        
        print("\n   3. Reiniciar servidor:")
        if is_production:
            print("      sudo systemctl restart apache2")
        else:
            print("      (Reiniciar Flask si está corriendo)")
    else:
        print("\n✅ La base de datos ya tiene la estructura correcta.")
        print("   No se requiere migración.")
        
        if is_production:
            print("\n   Si sigue habiendo errores:")
            print("   1. Verificar que Apache se haya reiniciado:")
            print("      sudo systemctl restart apache2")
            print("\n   2. Revisar logs:")
            print("      sudo tail -f /var/log/apache2/error.log")
    
    print("\n" + "=" * 70)
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
