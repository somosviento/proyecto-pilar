import requests
import os

class EmailSender:
    def __init__(self):
        self.script_url = os.getenv('GOOGLE_APPS_SCRIPT_URL')
        self.token = os.getenv('GOOGLE_APPS_SCRIPT_TOKEN')
        self.email_secretaria = os.getenv('EMAIL_SECRETARIA')
    
    def _make_request(self, action, data):
        """Hace una petición a la API de Google Apps Script"""
        payload = {
            'token': self.token,
            'action': action,
            **data
        }
        
        try:
            response = requests.post(self.script_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en petición a Google Apps Script: {e}")
            return None
    
    def send_notification_email(self, formulario_data, document_id):
        """Envía un email de notificación con el formulario adjunto"""
        
        # Crear el contenido HTML del email
        html_body = self._create_email_body(formulario_data)
        
        # Preparar los datos del email
        email_data = {
            'to': self.email_secretaria,
            'subject': f'Nuevo Formulario de Actividad - {formulario_data["titulo_actividad"]}',
            'htmlBody': html_body,
            'senderName': 'Sistema de Formularios UNCOMA',
            'attachments': [
                {
                    'fileId': document_id
                    # No convertir - el archivo ya es PDF
                }
            ]
        }
        
        result = self._make_request('sendEmail', email_data)
        if result and result.get('success'):
            return True
        else:
            print(f"Error al enviar email: {result}")
            return False
    
    def send_notification_email_with_pdf(self, formulario_data, document_id):
        """Envía un email de notificación convirtiendo el documento a PDF"""
        
        print(f"[DEBUG] Enviando email con conversión a PDF para documento: {document_id}")
        
        # Crear el contenido HTML del email
        html_body = self._create_email_body(formulario_data)
        
        # Preparar los datos del email con conversión a PDF
        email_data = {
            'to': self.email_secretaria,
            'subject': f'Nuevo Formulario de Actividad - {formulario_data["titulo_actividad"]} (PDF)',
            'htmlBody': html_body,
            'senderName': 'Sistema de Formularios UNCOMA',
            'attachments': [
                {
                    'fileId': document_id,
                    'convertTo': 'pdf'  # ¡Esta es la línea clave!
                }
            ]
        }
        
        print(f"[DEBUG] Enviando email con datos: {email_data}")
        result = self._make_request('sendEmail', email_data)
        print(f"[DEBUG] Resultado del envío: {result}")
        
        if result and result.get('success'):
            print(f"[DEBUG] Email con PDF enviado exitosamente")
            return True
        else:
            print(f"[DEBUG] Error al enviar email con PDF: {result}")
            return False
    
    def _create_email_body(self, formulario_data):
        """Crea el cuerpo HTML del email con el resumen del formulario"""
        
        # Formatear el equipo
        equipo_html = ""
        if formulario_data.get('equipo'):
            equipo_html = "<ul>"
            for miembro in formulario_data['equipo']:
                equipo_html += f"<li><strong>{miembro.get('apellido_nombre', '')}</strong> - DNI: {miembro.get('dni', '')} - Email: {miembro.get('correo', '')}</li>"
            equipo_html += "</ul>"
        
        # Formatear las fechas
        fechas_html = ""
        if formulario_data.get('fechas'):
            fechas_html = ", ".join(formulario_data['fechas'])
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .field {{ margin-bottom: 15px; }}
                .field-label {{ font-weight: bold; color: #2c3e50; }}
                .field-value {{ margin-left: 10px; }}
                .section {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Nuevo Formulario de Actividad Educativa</h2>
                <p>Se ha recibido un nuevo formulario de actividad</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <div class="field">
                        <span class="field-label">Título de la Actividad:</span>
                        <span class="field-value">{formulario_data.get('titulo_actividad', '')}</span>
                    </div>
                    
                    <div class="field">
                        <span class="field-label">Docente Responsable:</span>
                        <span class="field-value">{formulario_data.get('docente_responsable', '')}</span>
                    </div>
                </div>
                
                <div class="section">
                    <div class="field">
                        <span class="field-label">Equipo:</span>
                        <div class="field-value">{equipo_html}</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="field">
                        <span class="field-label">Fundamentación:</span>
                        <div class="field-value">{formulario_data.get('fundamentacion', '')[:200]}...</div>
                    </div>
                    
                    <div class="field">
                        <span class="field-label">Objetivos:</span>
                        <div class="field-value">{formulario_data.get('objetivos', '')[:200]}...</div>
                    </div>
                    
                    <div class="field">
                        <span class="field-label">Metodología:</span>
                        <div class="field-value">{formulario_data.get('metodologia', '')[:200]}...</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="field">
                        <span class="field-label">Grados/Requisitos:</span>
                        <span class="field-value">{formulario_data.get('grados', '')}</span>
                    </div>

                    <div class="field">
                        <span class="field-label">Grados/Requisitos:</span>
                        <span class="field-value">{formulario_data.get('requisitos', '')}</span>
                    </div>
                    
                    <div class="field">
                        <span class="field-label">Materiales/Presupuesto:</span>
                        <span class="field-value">{formulario_data.get('materiales_presupuesto', '')}</span>
                    </div>
                    
                    <div class="field">
                        <span class="field-label">Fechas Propuestas:</span>
                        <span class="field-value">{fechas_html}</span>
                    </div>
                </div>
                
                <div class="section">
                    <p><strong>Nota:</strong> El formulario completo se adjunta como archivo PDF.</p>
                    <p><em>Este email fue generado automáticamente por el Sistema de Formularios UNCOMA.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body