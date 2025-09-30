#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para explorar los datos guardados en formularios.db
Muestra la estructura y contenido de la base de datos
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def explore_database():
    """Explorar el contenido de la base de datos"""
    
    try:
        from app import app
        from models import db, FormularioActividad
        
        print("🗃️  EXPLORADOR DE BASE DE DATOS - PROYECTO PILAR")
        print("=" * 60)
        
        with app.app_context():
            # 1. Información de la base de datos
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado')
            print(f"📊 Base de datos: {db_uri}")
            
            # Verificar si la tabla existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'formularios_actividad' not in tables:
                print("❌ La tabla 'formularios_actividad' no existe")
                print("💡 Ejecutar: python init_db.py init")
                return False
            
            # 2. Estructura de la tabla
            print("\n📋 ESTRUCTURA DE LA TABLA 'formularios_actividad':")
            print("-" * 50)
            columns = inspector.get_columns('formularios_actividad')
            
            for i, col in enumerate(columns, 1):
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT: {col['default']}" if col['default'] else ""
                print(f"{i:2d}. {col['name']:<25} {col_type:<15} {nullable}{default}")
            
            # 3. Contar registros
            total_registros = FormularioActividad.query.count()
            print(f"\n📊 ESTADÍSTICAS:")
            print("-" * 50)
            print(f"Total de formularios: {total_registros}")
            
            if total_registros == 0:
                print("📝 No hay formularios registrados aún")
                return True
            
            # Contar por estado
            estados = db.session.query(
                FormularioActividad.estado, 
                db.func.count(FormularioActividad.estado)
            ).group_by(FormularioActividad.estado).all()
            
            print("Estados de formularios:")
            for estado, count in estados:
                print(f"  - {estado}: {count} formularios")
            
            # 4. Mostrar algunos registros de ejemplo
            print(f"\n📄 ÚLTIMOS 3 FORMULARIOS REGISTRADOS:")
            print("-" * 50)
            
            ultimos = FormularioActividad.query.order_by(
                FormularioActividad.fecha_creacion.desc()
            ).limit(3).all()
            
            for i, formulario in enumerate(ultimos, 1):
                print(f"\n{i}. ID: {formulario.id}")
                print(f"   Título: {formulario.titulo_actividad}")
                print(f"   Docente: {formulario.docente_responsable}")
                print(f"   Grados: {formulario.grados}")
                print(f"   Meses: {formulario.meses}")
                print(f"   Fecha: {formulario.fecha_creacion}")
                print(f"   Estado: {formulario.estado}")
                
                # Mostrar equipo si existe
                equipo = formulario.equipo
                if equipo:
                    print(f"   Equipo ({len(equipo)} miembros):")
                    for j, miembro in enumerate(equipo, 1):
                        print(f"     {j}. {miembro.get('apellido_nombre', 'N/A')} - DNI: {miembro.get('dni', 'N/A')}")
                
                # Mostrar fechas propuestas si existen
                fechas = formulario.fechas
                if fechas:
                    print(f"   Fechas propuestas: {', '.join(fechas)}")
                
                # Mostrar IDs de Google Drive si existen
                if formulario.documento_id:
                    print(f"   📄 Documento ID: {formulario.documento_id}")
                if formulario.carpeta_id:
                    print(f"   📁 Carpeta ID: {formulario.carpeta_id}")
            
            # 5. Campos más utilizados
            print(f"\n📈 ANÁLISIS DE DATOS:")
            print("-" * 50)
            
            # Grados más solicitados
            grados_query = db.session.query(FormularioActividad.grados).filter(
                FormularioActividad.grados.isnot(None),
                FormularioActividad.grados != ''
            ).all()
            
            if grados_query:
                print("Grados más solicitados:")
                grados_count = {}
                for (grados_str,) in grados_query:
                    if grados_str:
                        grados_list = [g.strip() for g in grados_str.split(',')]
                        for grado in grados_list:
                            grados_count[grado] = grados_count.get(grado, 0) + 1
                
                for grado, count in sorted(grados_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {grado}: {count} veces")
            
            # Meses más propuestos
            meses_query = db.session.query(FormularioActividad.meses).filter(
                FormularioActividad.meses.isnot(None),
                FormularioActividad.meses != ''
            ).all()
            
            if meses_query:
                print("\nMeses más propuestos:")
                meses_count = {}
                for (meses_str,) in meses_query:
                    if meses_str:
                        meses_list = [m.strip() for m in meses_str.split(',')]
                        for mes in meses_list:
                            meses_count[mes] = meses_count.get(mes, 0) + 1
                
                for mes, count in sorted(meses_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {mes}: {count} veces")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al explorar la base de datos: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

def show_database_schema():
    """Mostrar esquema detallado de los datos que se guardan"""
    
    print("\n🏗️  ESQUEMA DETALLADO DE DATOS GUARDADOS:")
    print("=" * 60)
    
    schema = {
        "Datos básicos del formulario": [
            "id (Integer) - ID único autoincremental",
            "titulo_actividad (Text) - Título de la actividad educativa",
            "docente_responsable (String 200) - Nombre completo del docente",
            "fundamentacion (Text) - Fundamentación de la actividad",
            "objetivos (Text) - Objetivos y propósitos",
            "metodologia (Text) - Metodología a utilizar"
        ],
        
        "Destinatarios y requisitos": [
            "grados (Text) - Grados destinatarios (ej: '1er Grado, 2do Grado')",
            "requisitos (Text) - Requisitos para participar",
            "materiales_presupuesto (Text) - Materiales y presupuesto necesario"
        ],
        
        "Planificación temporal": [
            "meses (Text) - Meses propuestos (ej: 'Enero, Marzo, Septiembre')",
            "fechas_propuestas (Text) - Fechas específicas en formato JSON"
        ],
        
        "Equipo de trabajo": [
            "equipo_json (Text) - Array JSON con datos del equipo:",
            "  └─ apellido_nombre: Nombre completo del miembro",
            "  └─ dni: DNI del miembro", 
            "  └─ correo: Email del miembro"
        ],
        
        "Metadatos y control": [
            "fecha_creacion (DateTime) - Cuándo se creó el registro",
            "fecha_modificacion (DateTime) - Última modificación",
            "estado (String 50) - Estado: 'pendiente', 'procesado', 'error'"
        ],
        
        "Integración Google Drive": [
            "documento_id (String 100) - ID del documento generado en Google Docs",
            "carpeta_id (String 100) - ID de la carpeta en Google Drive"
        ]
    }
    
    for categoria, campos in schema.items():
        print(f"\n📂 {categoria}:")
        print("-" * 40)
        for campo in campos:
            print(f"   {campo}")

def export_sample_data():
    """Exportar datos de ejemplo para documentación"""
    
    try:
        from app import app
        from models import FormularioActividad
        
        with app.app_context():
            # Obtener un registro de ejemplo
            sample = FormularioActividad.query.first()
            
            if sample:
                print(f"\n📄 EJEMPLO DE DATOS GUARDADOS:")
                print("=" * 60)
                
                sample_dict = sample.to_dict()
                
                # Mostrar como JSON formateado
                print(json.dumps(sample_dict, indent=2, ensure_ascii=False, default=str))
            else:
                print("\n📝 No hay datos de ejemplo disponibles")
                
    except Exception as e:
        print(f"❌ Error al exportar datos de ejemplo: {e}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Explorador de base de datos - Proyecto Pilar')
    parser.add_argument('--schema', action='store_true', help='Mostrar esquema de datos')
    parser.add_argument('--sample', action='store_true', help='Mostrar datos de ejemplo')
    
    args = parser.parse_args()
    
    # Exploración básica siempre
    success = explore_database()
    
    if args.schema:
        show_database_schema()
    
    if args.sample and success:
        export_sample_data()
    
    sys.exit(0 if success else 1)