#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar las columnas de la base de datos
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def check_columns():
    """Verificar las columnas de la tabla formularios_actividad"""
    try:
        from app import app
        from models import db
        from sqlalchemy import inspect
        
        print("🔍 Verificando columnas de la base de datos...")
        
        with app.app_context():
            inspector = inspect(db.engine)
            columns = inspector.get_columns('formularios_actividad')
            
            print(f"\n📋 Columnas en formularios_actividad ({len(columns)} columnas):\n")
            
            # Verificar si existen las columnas críticas
            column_names = [col['name'] for col in columns]
            
            for i, col in enumerate(columns, 1):
                marker = ""
                if col['name'] in ['email_responsable', 'dni_responsable']:
                    marker = " ✅ (NUEVA)"
                print(f"  {i:2d}. {col['name']:30s} {col['type']}{marker}")
            
            # Verificar columnas requeridas
            print("\n🔍 Verificación de columnas críticas:")
            required_columns = [
                'email_responsable',
                'dni_responsable',
                'titulo_actividad',
                'docente_responsable',
                'departamento'
            ]
            
            for col_name in required_columns:
                if col_name in column_names:
                    print(f"   ✅ {col_name}")
                else:
                    print(f"   ❌ {col_name} - FALTA")
            
            # Verificar si hay registros
            from models import FormularioActividad
            count = FormularioActividad.query.count()
            print(f"\n📊 Total de registros: {count}")
            
            if count > 0:
                # Verificar si los registros antiguos tienen NULL en las nuevas columnas
                with_email = FormularioActividad.query.filter(
                    FormularioActividad.email_responsable.isnot(None)
                ).count()
                with_dni = FormularioActividad.query.filter(
                    FormularioActividad.dni_responsable.isnot(None)
                ).count()
                
                print(f"   - Con email: {with_email}/{count}")
                print(f"   - Con DNI: {with_dni}/{count}")
                
                if with_email < count or with_dni < count:
                    print(f"\n⚠️  Advertencia: Hay {count - with_email} registros sin email y {count - with_dni} sin DNI")
                    print("   Esto es normal para registros anteriores a la migración.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("🗃️  VERIFICACIÓN DE COLUMNAS - PROYECTO PILAR")
    print("=" * 70)
    
    success = check_columns()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Verificación completada")
    else:
        print("❌ Verificación falló")
    
    sys.exit(0 if success else 1)
