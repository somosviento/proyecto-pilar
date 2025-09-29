#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación de configuración para Proyecto Pilar
Verificar que todas las variables de entorno estén configuradas correctamente
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Cargar variables de entorno
load_dotenv()

def validate_config():
    """Validar toda la configuración necesaria"""
    
    print("🔍 VALIDACIÓN DE CONFIGURACIÓN - PROYECTO PILAR")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # Variables críticas para Google Drive
    required_vars = {
        'GOOGLE_APPS_SCRIPT_URL': {
            'value': os.getenv('GOOGLE_APPS_SCRIPT_URL'),
            'description': 'URL del Google Apps Script',
            'example': 'https://script.google.com/macros/s/TU_SCRIPT_ID/exec'
        },
        'GOOGLE_APPS_SCRIPT_TOKEN': {
            'value': os.getenv('GOOGLE_APPS_SCRIPT_TOKEN'),
            'description': 'Token de seguridad para Google Apps Script',
            'example': 'tu-token-secreto-seguro'
        },
        'GOOGLE_DRIVE_ROOT_FOLDER_ID': {
            'value': os.getenv('GOOGLE_DRIVE_ROOT_FOLDER_ID'),
            'description': 'ID de la carpeta raíz en Google Drive',
            'example': '1aBcDeFgHiJkLmNoPqRsTuVwXyZ'
        },
        'TEMPLATE_DOC_ID': {
            'value': os.getenv('TEMPLATE_DOC_ID'),
            'description': 'ID del template de Google Docs',
            'example': '1aBcDeFgHiJkLmNoPqRsTuVwXyZ'
        }
    }
    
    # Variables opcionales
    optional_vars = {
        'FLASK_SECRET_KEY': {
            'value': os.getenv('FLASK_SECRET_KEY'),
            'description': 'Clave secreta de Flask',
            'example': 'tu-clave-secreta-muy-segura'
        },
        'DATABASE_URL': {
            'value': os.getenv('DATABASE_URL'),
            'description': 'URL de la base de datos',
            'example': 'sqlite:///formularios.db'
        },
        'SMTP_SERVER': {
            'value': os.getenv('SMTP_SERVER'),
            'description': 'Servidor SMTP para envío de emails',
            'example': 'smtp.gmail.com'
        }
    }
    
    print("📋 VARIABLES CRÍTICAS:")
    print("-" * 40)
    
    for var_name, config in required_vars.items():
        value = config['value']
        if not value:
            errors.append(f"❌ {var_name}: NO CONFIGURADA")
            print(f"❌ {var_name}")
            print(f"   Descripción: {config['description']}")
            print(f"   Ejemplo: {config['example']}")
        elif 'TU_' in value or 'tu-' in value.lower():
            errors.append(f"⚠️  {var_name}: Usando valor de ejemplo")
            print(f"⚠️  {var_name}: {value[:50]}...")
            print(f"   ⚠️  PARECE SER UN VALOR DE EJEMPLO, actualizar con valor real")
        else:
            print(f"✅ {var_name}: {value[:50]}..." if len(value) > 50 else f"✅ {var_name}: {value}")
        print()
    
    print("📋 VARIABLES OPCIONALES:")
    print("-" * 40)
    
    for var_name, config in optional_vars.items():
        value = config['value']
        if not value:
            warnings.append(f"⚠️  {var_name}: No configurada (opcional)")
            print(f"⚠️  {var_name}: No configurada")
        else:
            print(f"✅ {var_name}: {value[:50]}..." if len(value) > 50 else f"✅ {var_name}: {value}")
        print()
    
    # Verificar archivos críticos
    print("📁 ARCHIVOS Y DIRECTORIOS:")
    print("-" * 40)
    
    critical_files = [
        '.env',
        'wsgi.py',
        'app.py',
        'models.py',
        'utils/google_drive.py',
        'utils/email_sender.py',
        'utils/pdf_generator.py'
    ]
    
    for file_path in critical_files:
        full_path = project_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            errors.append(f"❌ Archivo faltante: {file_path}")
            print(f"❌ {file_path}")
    
    # Verificar permisos de directorio instance
    instance_dir = project_dir / 'instance'
    if instance_dir.exists():
        print(f"✅ instance/")
        if instance_dir.is_dir():
            print(f"   ✅ Es un directorio")
        else:
            errors.append("❌ instance/ no es un directorio")
    else:
        warnings.append("⚠️  Directorio instance/ no existe (se creará automáticamente)")
        print(f"⚠️  instance/ (se creará automáticamente)")
    
    print()
    
    # Resumen
    print("📊 RESUMEN:")
    print("-" * 40)
    
    if not errors:
        if warnings:
            print("🟡 CONFIGURACIÓN PARCIAL")
            print(f"   ✅ Sin errores críticos")
            print(f"   ⚠️  {len(warnings)} advertencias")
        else:
            print("🟢 CONFIGURACIÓN COMPLETA")
            print("   ✅ Todas las variables críticas configuradas")
            print("   ✅ Todos los archivos presentes")
    else:
        print("🔴 CONFIGURACIÓN INCOMPLETA")
        print(f"   ❌ {len(errors)} errores críticos")
        print(f"   ⚠️  {len(warnings)} advertencias")
    
    print()
    
    if errors:
        print("🔧 ERRORES A CORREGIR:")
        for error in errors:
            print(f"   {error}")
        print()
    
    if warnings:
        print("⚠️  ADVERTENCIAS:")
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    print("💡 PRÓXIMOS PASOS:")
    if errors:
        print("   1. Editar el archivo .env con las variables faltantes")
        print("   2. Ejecutar: python validate_config.py")
        print("   3. Una vez sin errores, reiniciar la aplicación")
    else:
        print("   1. La configuración está completa")
        print("   2. Puedes proceder con el despliegue/pruebas")
    
    print()
    return len(errors) == 0

def test_google_drive_connection():
    """Probar la conexión con Google Drive"""
    
    print("🔌 PRUEBA DE CONEXIÓN CON GOOGLE DRIVE")
    print("=" * 60)
    
    try:
        from utils.google_drive import GoogleDriveManager
        
        # Crear instancia del manager
        drive_manager = GoogleDriveManager()
        
        # Verificar configuración básica
        if not drive_manager.script_url or not drive_manager.token or not drive_manager.root_folder_id:
            print("❌ Configuración incompleta de Google Drive")
            return False
        
        # Intentar crear una carpeta de prueba
        test_folder_name = f"test_conexion_{int(datetime.now().timestamp())}"
        
        print(f"📁 Intentando crear carpeta de prueba: {test_folder_name}")
        
        folder_id = drive_manager.create_folder(test_folder_name)
        
        if folder_id:
            print(f"✅ Carpeta creada exitosamente con ID: {folder_id}")
            print("✅ Conexión con Google Drive funcionando correctamente")
            return True
        else:
            print("❌ No se pudo crear la carpeta de prueba")
            print("❌ Verificar configuración de Google Apps Script y permisos")
            return False
            
    except Exception as e:
        print(f"❌ Error al probar conexión: {str(e)}")
        return False

if __name__ == '__main__':
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='Validación de configuración - Proyecto Pilar')
    parser.add_argument('--test-drive', action='store_true', 
                       help='Probar conexión con Google Drive')
    
    args = parser.parse_args()
    
    # Validación básica de configuración
    config_ok = validate_config()
    
    # Prueba de conexión si se solicita
    if args.test_drive and config_ok:
        drive_ok = test_google_drive_connection()
        sys.exit(0 if drive_ok else 1)
    else:
        sys.exit(0 if config_ok else 1)