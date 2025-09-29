#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración directa de variables de entorno para Proyecto Pilar
Solo usar si el archivo .env no funciona en producción
"""

import os

def set_production_env():
    """Configurar variables de entorno directamente"""
    
    # Variables críticas para Google Drive
    env_vars = {
        'FLASK_ENV': 'production',
        'FLASK_DEBUG': 'False',
        'FLASK_SECRET_KEY': 'tu-clave-secreta-muy-segura-para-produccion',
        'GOOGLE_APPS_SCRIPT_URL': 'https://script.google.com/macros/s/AKfycbyOCTQyZdowgCEPr3yJyz7c-ppRsDJFsQoiplAswZv6Cun7URbvr1V1Tsv4O89tdc-Z/exec',
        'GOOGLE_APPS_SCRIPT_TOKEN': 'quintral1250',
        'GOOGLE_DRIVE_ROOT_FOLDER_ID': '1DLlVYgv2HaXz8WAI2yYEvEAy79nNpboI',
        'TEMPLATE_DOC_ID': '1GcqJ5uN11iSDOyMzJFVQccO0YxmVmDRbLMoOkjT9X9M',
        'EMAIL_SECRETARIA': 'secretaria.extension@uncobariloche.com',
        'DATABASE_URL': 'sqlite:///instance/formularios.db'
    }
    
    print("[CONFIG] Configurando variables de entorno directamente...")
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"[CONFIG] {key}: {'***CONFIGURADA***' if 'TOKEN' in key or 'SECRET' in key else value}")
    
    print("[CONFIG] Variables configuradas correctamente")
    return True

if __name__ == '__main__':
    set_production_env()
    
    # Verificar que se cargaron
    print("\n[VERIFY] Verificando variables:")
    critical_vars = [
        'GOOGLE_APPS_SCRIPT_URL',
        'GOOGLE_DRIVE_ROOT_FOLDER_ID', 
        'TEMPLATE_DOC_ID'
    ]
    
    for var in critical_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:50]}...")
        else:
            print(f"❌ {var}: NO CONFIGURADA")