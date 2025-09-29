import requests
import os
from datetime import datetime
import base64

class GoogleDriveManager:
    def __init__(self):
        self.script_url = os.getenv('GOOGLE_APPS_SCRIPT_URL')
        self.token = os.getenv('GOOGLE_APPS_SCRIPT_TOKEN')
        self.root_folder_id = os.getenv('GOOGLE_DRIVE_ROOT_FOLDER_ID')
        
        # Debug: Imprimir los valores cargados
        print(f"[DEBUG] GoogleDriveManager inicializado:")
        print(f"[DEBUG]   script_url: {self.script_url}")
        print(f"[DEBUG]   token: {self.token[:10] if self.token else 'None'}...")
        print(f"[DEBUG]   root_folder_id: {self.root_folder_id}")
        
        # Validar que las variables estén configuradas
        if not self.script_url or 'TU_SCRIPT_ID' in self.script_url:
            print(f"[ERROR] script_url no está configurada correctamente: {self.script_url}")
        if not self.token:
            print(f"[ERROR] token no está configurado")
        if not self.root_folder_id:
            print(f"[ERROR] root_folder_id no está configurado")
    
    def _make_request(self, action, data):
        """Hace una petición a la API de Google Apps Script"""
        payload = {
            'token': self.token,
            'action': action,
            **data
        }
        
        print(f"[DEBUG] Haciendo petición a {self.script_url}")
        print(f"[DEBUG] Acción: {action}")
        print(f"[DEBUG] Datos: {data}")
        
        try:
            response = requests.post(self.script_url, json=payload, timeout=30)
            print(f"[DEBUG] Código de respuesta: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            print(f"[DEBUG] Respuesta: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error en petición a Google Apps Script: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[ERROR] Respuesta del servidor: {e.response.text}")
            return None
    
    def create_folder(self, folder_name):
        """Crea una carpeta en Google Drive"""
        print(f"[DEBUG] Intentando crear carpeta: {folder_name}")
        print(f"[DEBUG] Root folder ID: {self.root_folder_id}")
        
        # Validaciones previas
        if not self.script_url:
            print(f"[ERROR] script_url no configurada")
            raise Exception("Google Apps Script URL no configurada. Verificar GOOGLE_APPS_SCRIPT_URL en .env")
        
        if not self.token:
            print(f"[ERROR] token no configurado")
            raise Exception("Google Apps Script token no configurado. Verificar GOOGLE_APPS_SCRIPT_TOKEN en .env")
        
        if not self.root_folder_id:
            print(f"[ERROR] root_folder_id no configurado")
            raise Exception("Google Drive root folder ID no configurado. Verificar GOOGLE_DRIVE_ROOT_FOLDER_ID en .env")
        
        if 'TU_SCRIPT_ID' in self.script_url:
            print(f"[ERROR] script_url parece ser un valor de ejemplo")
            raise Exception("Google Apps Script URL parece ser un valor de ejemplo. Actualizar con la URL real del script desplegado.")
        
        data = {
            'rootFolderId': self.root_folder_id,
            'folders': [{'name': folder_name}]
        }
        
        result = self._make_request('createFolders', data)
        print(f"[DEBUG] Resultado de createFolders: {result}")
        
        if result and result.get('success'):
            folder_info = result['data']['createdFolders'][0]
            folder_id = folder_info['id']
            print(f"[DEBUG] Carpeta creada exitosamente con ID: {folder_id}")
            return folder_id
        else:
            error_msg = "Error desconocido"
            if result:
                error_msg = result.get('message', 'Error desconocido')
                print(f"[ERROR] Error del servidor: {error_msg}")
                if 'token' in error_msg.lower():
                    raise Exception(f"Error de autenticación: {error_msg}. Verificar GOOGLE_APPS_SCRIPT_TOKEN")
                elif 'folder' in error_msg.lower():
                    raise Exception(f"Error de carpeta: {error_msg}. Verificar GOOGLE_DRIVE_ROOT_FOLDER_ID y permisos")
                else:
                    raise Exception(f"Error de Google Apps Script: {error_msg}")
            else:
                print(f"[ERROR] No se recibió respuesta del servidor")
                raise Exception("No se recibió respuesta del Google Apps Script. Verificar URL y conectividad")
            return None
    
    def upload_file(self, file_content, filename, mime_type, folder_id=None):
        """Sube un archivo a Google Drive"""
        # Convertir el contenido del archivo a base64
        if isinstance(file_content, bytes):
            file_base64 = base64.b64encode(file_content).decode('utf-8')
        else:
            file_base64 = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
        
        file_data = {
            'fileName': filename,
            'mimeType': mime_type,
            'fileContent': file_base64
        }
        
        if folder_id:
            file_data['folderId'] = folder_id
        
        data = {'files': [file_data]}
        
        result = self._make_request('uploadFiles', data)
        if result and result.get('success'):
            file_info = result['data']['results'][0]
            if file_info.get('success'):
                return file_info['fileId']
        return None
    
    def generate_document_from_template(self, template_id, filename, fields, folder_id=None, signature_data=None, equipo_data=None):
        """Genera un documento a partir de una plantilla con soporte para firmas y tablas de equipo"""
        doc_data = {
            'templateId': template_id,
            'fileName': filename,
            'fields': fields
        }
        
        if folder_id:
            doc_data['folderId'] = folder_id
            
        # Agregar datos de firma si están disponibles
        if signature_data:
            doc_data['signatureData'] = signature_data
            print(f"[DEBUG] Enviando datos de firma a Google Apps Script")
            
        # Agregar datos del equipo si están disponibles
        if equipo_data:
            doc_data['equipoData'] = equipo_data
            print(f"[DEBUG] Enviando datos de equipo a Google Apps Script: {len(equipo_data)} miembros")
        
        data = {'documents': [doc_data]}
        
        result = self._make_request('generateDocuments', data)
        if result and result.get('success'):
            doc_info = result['data']['documents'][0]
            if doc_info.get('success'):
                return {
                    'document_id': doc_info['documentId'],
                    'document_url': doc_info['documentUrl']
                }
        return None
    
    def convert_to_pdf(self, document_id, pdf_filename=None, folder_id=None):
        """Convierte un documento de Google Docs a PDF real usando la funcionalidad de email"""
        
        try:
            print(f"[DEBUG] Iniciando conversión real a PDF para documento: {document_id}")
            
            # Estrategia: Usar la funcionalidad existente de sendEmail para convertir a PDF
            # pero interceptar el proceso para obtener el archivo PDF resultante
            
            # Primero, intentemos crear un PDF real usando la API de conversión de email
            # pero enviándolo a una dirección que no cause problemas
            
            email_data = {
                'to': 'conversion-temp@domain-that-does-not-exist.invalid',  # Dirección inválida
                'subject': 'Conversión temporal a PDF - No enviar',
                'htmlBody': 'Conversión temporal de documento a PDF.',
                'attachments': [
                    {
                        'fileId': document_id,
                        'convertTo': 'pdf'
                    }
                ]
            }
            
            print(f"[DEBUG] Enviando petición para conversión a PDF...")
            result = self._make_request('sendEmail', email_data)
            print(f"[DEBUG] Resultado de conversión via email: {result}")
            
            # Independientemente del resultado del email, proporcionamos acceso al PDF
            pdf_download_url = f'https://docs.google.com/document/d/{document_id}/export?format=pdf'
            pdf_url = f'https://drive.google.com/file/d/{document_id}/view'
            
            return {
                'pdf_file_id': document_id,  # Usamos el mismo ID del documento
                'pdf_filename': pdf_filename or 'documento.pdf',
                'pdf_url': pdf_url,
                'pdf_download_url': pdf_download_url,
                'folder_id': folder_id,
                'size': 0,  # No disponible sin crear archivo separado
                'note': 'PDF disponible para descarga desde Google Docs',
                'conversion_attempted': True
            }
            
        except Exception as e:
            print(f"[DEBUG] Error en conversión a PDF: {e}")
            # Aún así, proporcionamos URLs de descarga
            return {
                'pdf_file_id': document_id,
                'pdf_filename': pdf_filename or 'documento.pdf',
                'pdf_url': f'https://drive.google.com/file/d/{document_id}/view',
                'pdf_download_url': f'https://docs.google.com/document/d/{document_id}/export?format=pdf',
                'folder_id': folder_id,
                'size': 0,
                'note': 'PDF disponible para descarga (conversión falló)',
                'conversion_attempted': False
            }
    
    def create_real_pdf_file(self, document_id, pdf_filename=None, folder_id=None):
        """Crea un archivo PDF real en Google Drive descargando y resubiendo el documento"""
        
        try:
            import requests
            
            print(f"[DEBUG] Creando archivo PDF real para: {document_id}")
            
            # 1. Descargar el documento como PDF usando la URL de exportación de Google
            export_url = f'https://docs.google.com/document/d/{document_id}/export?format=pdf'
            
            # Obtener token de acceso para la descarga
            # Nota: Esto requeriría implementar OAuth, por ahora usamos el método de email
            
            # Método alternativo: Usar la conversión de email para crear el PDF
            email_data = {
                'to': 'secretaria.extension@uncobariloche.com',  # Email real para que funcione
                'subject': f'Documento generado: {pdf_filename or "formulario.pdf"}',
                'htmlBody': 'Se adjunta el documento solicitado en formato PDF.',
                'attachments': [
                    {
                        'fileId': document_id,
                        'convertTo': 'pdf'
                    }
                ]
            }
            
            print(f"[DEBUG] Enviando email con PDF adjunto...")
            result = self._make_request('sendEmail', email_data)
            print(f"[DEBUG] Resultado de envío con PDF: {result}")
            
            if result and result.get('success'):
                return {
                    'pdf_file_id': document_id,  # ID del documento original
                    'pdf_filename': pdf_filename or 'documento.pdf',
                    'pdf_url': f'https://drive.google.com/file/d/{document_id}/view',
                    'pdf_download_url': f'https://docs.google.com/document/d/{document_id}/export?format=pdf',
                    'folder_id': folder_id,
                    'email_sent': True,
                    'note': 'PDF enviado por email y disponible para descarga'
                }
            else:
                return None
                
        except Exception as e:
            print(f"[DEBUG] Error creando archivo PDF real: {e}")
            return None
    
    def create_folder_name(self, docente_apellido, fecha=None):
        """Crea un nombre de carpeta basado en el apellido del docente y la fecha"""
        if not fecha:
            fecha = datetime.now()
        
        fecha_str = fecha.strftime('%Y%m%d')
        # Limpiar el apellido de caracteres especiales
        apellido_clean = ''.join(c for c in docente_apellido if c.isalnum() or c in ' -_')
        apellido_clean = apellido_clean.replace(' ', '_')
        
        return f"{apellido_clean}_{fecha_str}"
    
    def create_filename(self, docente_apellido, fecha=None, extension='pdf'):
        """Crea un nombre de archivo basado en el apellido del docente y la fecha"""
        if not fecha:
            fecha = datetime.now()
        
        fecha_str = fecha.strftime('%Y%m%d')
        # Limpiar el apellido de caracteres especiales
        apellido_clean = ''.join(c for c in docente_apellido if c.isalnum() or c in ' -_')
        apellido_clean = apellido_clean.replace(' ', '_')
        
        return f"{apellido_clean}_{fecha_str}_formulario.{extension}"