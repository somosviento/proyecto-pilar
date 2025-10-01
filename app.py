from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import base64

# Importar nuestras utilidades
from models import db, FormularioActividad
from utils.google_drive import GoogleDriveManager
from utils.email_sender import EmailSender
from utils.pdf_generator import PDFGenerator

# Cargar variables de entorno
load_dotenv()

# Debug: Verificar que las variables de entorno se carguen correctamente
print(f"[DEBUG] Variables de entorno cargadas:")
print(f"[DEBUG]   GOOGLE_APPS_SCRIPT_URL: {os.getenv('GOOGLE_APPS_SCRIPT_URL')}")
print(f"[DEBUG]   GOOGLE_APPS_SCRIPT_TOKEN: {os.getenv('GOOGLE_APPS_SCRIPT_TOKEN')[:10] if os.getenv('GOOGLE_APPS_SCRIPT_TOKEN') else 'None'}...")
print(f"[DEBUG]   GOOGLE_DRIVE_ROOT_FOLDER_ID: {os.getenv('GOOGLE_DRIVE_ROOT_FOLDER_ID')}")
print(f"[DEBUG]   TEMPLATE_DOC_ID: {os.getenv('TEMPLATE_DOC_ID')}")
print()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'tu-clave-secreta-por-defecto')

# Configurar ruta de base de datos
if os.getenv('FLASK_ENV') == 'production' or os.getenv('DATABASE_PATH'):
    # En producción, usar ruta absoluta desde wsgi.py
    database_path = os.getenv('DATABASE_PATH')
    if database_path:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    else:
        # Fallback: construir ruta absoluta
        project_root = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(project_root, 'instance', 'formularios.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    # En desarrollo, usar variable de entorno o ruta relativa
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/formularios.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Debug: Mostrar configuración de base de datos
print(f"[DEBUG] Database URI configurada: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Configuración para producción con basepath se maneja en wsgi.py

# Inicializar la base de datos
db.init_app(app)

# Inicializar las utilidades
google_drive = GoogleDriveManager()
email_sender = EmailSender()
pdf_generator = PDFGenerator()

# Crear las tablas al iniciar la aplicación se hará en el main

@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('formulario.html')

@app.route('/favicon.ico')
def favicon():
    """Servir favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), 
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/enviar_formulario', methods=['POST'])
def enviar_formulario():
    """Procesar el envío del formulario"""
    try:
        # 1. Recopilar datos del formulario
        datos_formulario = extraer_datos_formulario(request)
        
        # 2. Validar datos requeridos
        if not validar_datos_requeridos(datos_formulario):
            return jsonify({
                'success': False,
                'message': 'Faltan campos obligatorios'
            })
        
        # 3. Guardar en la base de datos
        formulario = crear_formulario_db(datos_formulario)
        db.session.add(formulario)
        db.session.commit()
        
        # 4. Procesar el formulario (Google Drive y Email)
        resultado_procesamiento = procesar_formulario(formulario, datos_formulario)
        
        if resultado_procesamiento['success']:
            # Actualizar el estado del formulario
            formulario.estado = 'procesado'
            formulario.documento_id = resultado_procesamiento.get('document_id')
            formulario.carpeta_id = resultado_procesamiento.get('folder_id')
            db.session.commit()
            
            # Redirigir a página de confirmación
            return redirect(url_for('confirmacion_envio', formulario_id=formulario.id))
        else:
            # Marcar como error pero mantener en la base de datos
            formulario.estado = 'error'
            db.session.commit()
            
            return jsonify({
                'success': False,
                'message': f'Error al procesar: {resultado_procesamiento.get("message", "Error desconocido")}',
                'data': {'formulario_id': formulario.id}
            })
    
    except Exception as e:
        app.logger.error(f'Error en enviar_formulario: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

def extraer_datos_formulario(request):
    """Extrae y organiza los datos del formulario"""
    
    # Extraer equipo
    equipo_json = request.form.get('equipo', '[]')
    try:
        equipo = json.loads(equipo_json)
    except:
        equipo = []
    
    # Extraer períodos (reemplaza fechas_propuestas)
    periodos_json = request.form.get('periodos', '[]')
    try:
        periodos = json.loads(periodos_json)
    except:
        periodos = []
    
    # Generar texto legible para el campo 'meses' a partir de los períodos
    meses_texto = generar_texto_periodos(periodos)
    
    datos = {
        'titulo_actividad': request.form.get('titulo_actividad', '').strip(),
        'docente_responsable': request.form.get('docente_responsable', '').strip(),
        'departamento': request.form.get('departamento', '').strip(),
        'equipo': equipo,
        'fundamentacion': request.form.get('fundamentacion', '').strip(),
        'objetivos': request.form.get('objetivos', '').strip(),
        'metodologia': request.form.get('metodologia', '').strip(),
        'grados': request.form.get('grados', '').strip(),
        'materiales_presupuesto': request.form.get('materiales_presupuesto', '').strip(),
        'meses': meses_texto,
        'periodos': periodos
    }
    
    # Debug: imprimir los valores de grados y períodos
    app.logger.info(f"[DEBUG] Grados recibidos: '{datos['grados']}'")
    app.logger.info(f"[DEBUG] Períodos recibidos: {datos['periodos']}")
    app.logger.info(f"[DEBUG] Meses (texto): '{datos['meses']}'")
    print(f"[DEBUG] Grados recibidos: '{datos['grados']}'")
    print(f"[DEBUG] Períodos recibidos: {datos['periodos']}")
    print(f"[DEBUG] Meses (texto): '{datos['meses']}'")
    
    return datos

def generar_texto_periodos(periodos):
    """
    Convierte la estructura de períodos a texto legible
    Ejemplo: [{ano: "2025", meses: ["Marzo", "Abril"]}, {ano: "2026", meses: ["Julio"]}]
    Retorna: "2025: Marzo, Abril | 2026: Julio"
    """
    if not periodos:
        return ''
    
    textos_por_ano = []
    for periodo in periodos:
        ano = periodo.get('ano', '')
        meses = periodo.get('meses', [])
        if ano and meses:
            meses_str = ', '.join(meses)
            textos_por_ano.append(f"{ano}: {meses_str}")
    
    return ' | '.join(textos_por_ano)

def validar_datos_requeridos(datos):
    """Valida que los campos obligatorios estén presentes"""
    campos_requeridos = ['titulo_actividad', 'docente_responsable', 'fundamentacion', 'objetivos', 'metodologia']
    
    for campo in campos_requeridos:
        if not datos.get(campo) or len(datos[campo].strip()) == 0:
            return False
    
    return True

def crear_formulario_db(datos):
    """Crea un objeto FormularioActividad para guardar en la base de datos"""
    
    formulario = FormularioActividad(
        titulo_actividad=datos['titulo_actividad'],
        docente_responsable=datos['docente_responsable'],
        departamento=datos['departamento'],
        fundamentacion=datos['fundamentacion'],
        objetivos=datos['objetivos'],
        metodologia=datos['metodologia'],
        grados=datos['grados'],
        materiales_presupuesto=datos['materiales_presupuesto'],
        meses=datos['meses']
    )
    
    # Asignar equipo y períodos usando las propiedades
    formulario.equipo = datos['equipo']
    formulario.periodos = datos['periodos']
    
    return formulario

def procesar_formulario(formulario_db, datos_formulario):
    """Procesa el formulario: genera documento y envía email"""
    
    try:
        # 1. Extraer apellido del docente para nombres de archivos
        docente_apellido = extraer_apellido(datos_formulario['docente_responsable'])
        app.logger.info(f'Apellido extraído: {docente_apellido}')
        
        # 2. Crear carpeta en Google Drive
        folder_name = google_drive.create_folder_name(docente_apellido)
        app.logger.info(f'Nombre de carpeta a crear: {folder_name}')
        
        try:
            folder_id = google_drive.create_folder(folder_name)
            app.logger.info(f'Resultado de crear carpeta: {folder_id}')
        except Exception as e:
            app.logger.error(f'Error específico al crear carpeta: {str(e)}')
            return {
                'success': False,
                'message': f'Error al crear carpeta en Google Drive: {str(e)}'
            }
        
        if not folder_id:
            app.logger.error('create_folder devolvió None o valor falsy')
            return {
                'success': False,
                'message': 'No se pudo crear la carpeta en Google Drive'
            }
        
        # 3. Generar documento desde template de Google Docs usando la API
        template_id = os.getenv('TEMPLATE_DOC_ID')
        document_result = None
        
        if template_id:
            # Generar documento usando el template de Google Docs via API
            filename = google_drive.create_filename(docente_apellido, extension='docx')
            fields = pdf_generator.create_template_fields(datos_formulario)
            
            app.logger.info(f'Generando documento desde template: {template_id}')
            app.logger.info(f'Nombre de archivo: {filename}')
            app.logger.info(f'Carpeta destino: {folder_id}')
            
            # Generar documento Google Docs desde template
            doc_result = google_drive.generate_document_from_template(
                template_id, filename, fields, folder_id, 
                None,  # Sin firma
                datos_formulario.get('equipo')
            )
            
            if doc_result:
                app.logger.info(f'Documento generado exitosamente: {doc_result["document_id"]}')
                print(f'[DEBUG] Documento generado exitosamente: {doc_result["document_id"]}')
                
                # Enviar email con el documento convertido a PDF (no generar PDF local)
                print(f'[DEBUG] Enviando email con documento de Google Docs convertido a PDF')
                
                email_success = email_sender.send_notification_email_with_pdf(
                    datos_formulario, 
                    doc_result['document_id']
                )
                print(f'[DEBUG] Resultado envío email con PDF convertido: {email_success}')
                
                document_result = {
                    'document_id': doc_result['document_id'],
                    'document_url': doc_result['document_url'],
                    'pdf_download_url': f'https://docs.google.com/document/d/{doc_result["document_id"]}/export?format=pdf'
                }
                
                # Verificar resultado del envío
                if not email_success:
                    app.logger.warning('El documento se generó pero falló el envío del email')
                
                print(f'[DEBUG] Preparando respuesta final exitosa con documento convertido a PDF')
                return {
                    'success': True,
                    'message': 'Formulario procesado correctamente. Documento con imagen de firma enviado como PDF por email.',
                    'document_id': document_result['document_id'],
                    'document_url': document_result['document_url'],
                    'pdf_download_url': document_result.get('pdf_download_url'),
                    'folder_id': folder_id,
                    'email_sent': email_success,
                    'generation_method': 'google_docs_template_with_signature_to_pdf'
                }
            else:
                app.logger.error('Falló la generación del documento desde template')
                print(f'[DEBUG] Falló la generación del documento desde template')
                return {
                    'success': False,
                    'message': 'No se pudo generar documento desde template de Google Docs'
                }
    
    except Exception as e:
        app.logger.error(f'Error en procesar_formulario: {str(e)}')
        print(f'[DEBUG] ERROR CAPTURADO: {str(e)}')
        print(f'[DEBUG] Tipo de error: {type(e).__name__}')
        import traceback
        print(f'[DEBUG] Traceback: {traceback.format_exc()}')
        return {
            'success': False,
            'message': f'Error en el procesamiento: {str(e)}'
        }

def extraer_apellido(nombre_completo):
    """Extrae el apellido del nombre completo (asume que el apellido es la primera palabra)"""
    if not nombre_completo:
        return 'Sin_Apellido'
    
    palabras = nombre_completo.strip().split()
    if palabras:
        return palabras[0]
    else:
        return 'Sin_Apellido'

@app.route('/confirmacion/<int:formulario_id>')
def confirmacion_envio(formulario_id):
    """Página de confirmación después del envío exitoso"""
    try:
        formulario = FormularioActividad.query.get_or_404(formulario_id)
        
        # Verificar que el formulario fue procesado exitosamente
        if formulario.estado != 'procesado':
            return redirect(url_for('index'))
        
        return render_template('confirmacion.html', 
                             fecha_procesamiento=formulario.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
                             numero_formulario=f"FORM-{formulario.id:06d}")
    
    except Exception as e:
        app.logger.error(f'Error en confirmacion_envio: {str(e)}')
        return redirect(url_for('index'))

@app.route('/formularios')
def listar_formularios():
    """Página para listar todos los formularios enviados (para administración)"""
    formularios = FormularioActividad.query.order_by(FormularioActividad.fecha_creacion.desc()).all()
    
    formularios_data = []
    for formulario in formularios:
        data = formulario.to_dict()
        formularios_data.append(data)
    
    return jsonify({
        'success': True,
        'data': formularios_data
    })

@app.route('/formulario/<int:formulario_id>')
def ver_formulario(formulario_id):
    """Ver un formulario específico"""
    formulario = FormularioActividad.query.get_or_404(formulario_id)
    return jsonify({
        'success': True,
        'data': formulario.to_dict()
    })

@app.route('/health')
def health_check():
    """Endpoint de verificación de estado de la aplicación"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Recurso no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'message': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
    
    # Configuración para desarrollo con recarga automática
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'  # Por defecto True para desarrollo
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"🚀 Iniciando aplicación en modo {'DEBUG' if debug_mode else 'PRODUCCIÓN'}")
    print(f"📡 Puerto: {port}")
    print(f"🔄 Recarga automática: {'ACTIVADA' if debug_mode else 'DESACTIVADA'}")
    print(f"🌐 URL: http://localhost:{port}")
    print("=" * 50)
    
    app.run(
        debug=debug_mode, 
        host='0.0.0.0', 
        port=port,
        use_reloader=debug_mode,  # Recarga automática en modo debug
        use_debugger=debug_mode   # Debugger integrado en modo debug
    )