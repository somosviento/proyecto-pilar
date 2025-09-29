#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Configuration for Proyecto Pilar - UNCOMA
Apache 2 Deployment with basepath /proyecto-pilar

Configuración WSGI para despliegue en Apache 2
Basepath de producción: /proyecto-pilar
"""

import sys
import os
from pathlib import Path

# Obtener el directorio actual del proyecto
project_dir = Path(__file__).parent.absolute()

# Agregar el directorio del proyecto al path de Python
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Configurar variables de entorno para producción
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', 'False')

# Importar la aplicación Flask
try:
    from app import app as application
    
    # Configurar basepath para producción
    application.config['APPLICATION_ROOT'] = '/proyecto-pilar'
    
    # Configurar ProxyFix para manejar headers de Apache correctamente
    from werkzeug.middleware.proxy_fix import ProxyFix
    application.wsgi_app = ProxyFix(
        application.wsgi_app, 
        x_for=1, 
        x_proto=1, 
        x_host=1, 
        x_prefix=1
    )
    
    # Log de inicio para debug
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(project_dir / 'logs' / 'pilar.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Aplicación Proyecto Pilar iniciada correctamente")
    logger.info(f"Directorio del proyecto: {project_dir}")
    logger.info(f"Basepath configurado: /proyecto-pilar")
    
except ImportError as e:
    # Crear una aplicación mínima en caso de error
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error():
        return f"Error importando la aplicación: {str(e)}", 500
    
    print(f"Error importando app: {e}")

# Verificar configuración para Apache
if __name__ != '__main__':
    # Configuraciones específicas para Apache
    application.config.update(
        # Configuración de seguridad
        SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production'),
        
        # Configuración de base de datos (usar ruta absoluta)
        DATABASE_PATH=str(project_dir / 'instance' / 'formularios.db'),
        
        # Configuración de archivos estáticos
        STATIC_FOLDER=str(project_dir / 'static'),
        TEMPLATE_FOLDER=str(project_dir / 'templates'),
        
        # Configuración de uploads y archivos temporales
        UPLOAD_FOLDER=str(project_dir / 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        
        # Configuración de logging
        LOG_LEVEL='INFO',
        LOG_FILE=str(project_dir / 'logs' / 'pilar.log'),
    )
    
    # Crear directorios necesarios si no existen
    for directory in ['logs', 'uploads', 'instance']:
        dir_path = project_dir / directory
        dir_path.mkdir(exist_ok=True)

# Para testing local
if __name__ == '__main__':
    print("Iniciando aplicación en modo de desarrollo...")
    print(f"Directorio del proyecto: {project_dir}")
    application.run(debug=True, host='0.0.0.0', port=5000)