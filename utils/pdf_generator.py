from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
import os
import base64
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configurar estilos personalizados para el PDF"""
        
        # Estilo para el título principal
        self.styles.add(ParagraphStyle(
            name='TitleStyle',
            parent=self.styles['Title'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.navy
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtitleStyle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.darkblue
        ))
        
        # Estilo para texto normal con justificación
        self.styles.add(ParagraphStyle(
            name='JustifiedStyle',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Estilo para etiquetas de campos
        self.styles.add(ParagraphStyle(
            name='FieldLabelStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.darkblue,
            spaceAfter=5
        ))
    
    def generate_formulario_pdf(self, formulario_data):
        """Genera un PDF con los datos del formulario"""
        
        # Crear un buffer de bytes para el PDF
        buffer = BytesIO()
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Crear la historia del documento
        story = []
        
        # Agregar contenido al PDF
        self._add_header(story)
        self._add_basic_info(story, formulario_data)
        self._add_team_section(story, formulario_data)
        self._add_content_sections(story, formulario_data)
        self._add_practical_info(story, formulario_data)
        
        # Construir el PDF
        doc.build(story)
        
        # Obtener el contenido del buffer
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
    
    def _add_header(self, story):
        """Agregar encabezado del documento"""
        
        # Título principal
        title = Paragraph("FORMULARIO DE ACTIVIDAD EDUCATIVA", self.styles['TitleStyle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Información de la convocatoria
        year = datetime.now().year
        convocatoria = Paragraph(f"Convocatoria {year}", self.styles['Normal'])
        story.append(convocatoria)
        story.append(Spacer(1, 20))
    
    def _add_basic_info(self, story, data):
        """Agregar información básica del formulario"""
        
        # Título de la actividad
        story.append(Paragraph("Título de la Actividad", self.styles['SubtitleStyle']))
        story.append(Paragraph(data.get('titulo_actividad', ''), self.styles['JustifiedStyle']))
        story.append(Spacer(1, 15))
        
        # Docente responsable
        story.append(Paragraph("Docente Responsable", self.styles['SubtitleStyle']))
        story.append(Paragraph(data.get('docente_responsable', ''), self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Email del docente responsable
        story.append(Paragraph("Correo electrónico", self.styles['FieldLabelStyle']))
        story.append(Paragraph(data.get('email_responsable', ''), self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # DNI del docente responsable
        story.append(Paragraph("DNI", self.styles['FieldLabelStyle']))
        story.append(Paragraph(data.get('dni_responsable', ''), self.styles['Normal']))
        story.append(Spacer(1, 15))
    
    def _add_team_section(self, story, data):
        """Agregar sección del equipo"""
        
        story.append(Paragraph("Equipo", self.styles['SubtitleStyle']))
        
        # Crear tabla para el equipo
        equipo = data.get('equipo', [])
        if equipo:
            # Encabezados de la tabla
            table_data = [['Apellido y Nombre', 'DNI', 'Correo Electrónico']]
            
            # Agregar filas del equipo
            for miembro in equipo:
                table_data.append([
                    miembro.get('apellido_nombre', ''),
                    miembro.get('dni', ''),
                    miembro.get('correo', '')
                ])
            
            # Crear la tabla
            team_table = Table(table_data, colWidths=[3*inch, 1.5*inch, 2.5*inch])
            team_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(team_table)
        else:
            story.append(Paragraph("No se especificó equipo", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
    
    def _add_content_sections(self, story, data):
        """Agregar las secciones de contenido del formulario"""
        
        # Fundamentación
        story.append(Paragraph("Fundamentación", self.styles['SubtitleStyle']))
        fundamentacion = data.get('fundamentacion', '')
        story.append(Paragraph(fundamentacion, self.styles['JustifiedStyle']))
        story.append(Spacer(1, 15))
        
        # Objetivos o Propósitos
        story.append(Paragraph("Objetivos o Propósitos", self.styles['SubtitleStyle']))
        objetivos = data.get('objetivos', '')
        story.append(Paragraph(objetivos, self.styles['JustifiedStyle']))
        story.append(Spacer(1, 15))
        
        # Metodología
        story.append(Paragraph("Metodología", self.styles['SubtitleStyle']))
        metodologia = data.get('metodologia', '')
        story.append(Paragraph(metodologia, self.styles['JustifiedStyle']))
        story.append(Spacer(1, 15))
    
    def _add_practical_info(self, story, data):
        """Agregar información práctica del formulario"""
        
        # Grados incluidos / Requisitos
        story.append(Paragraph("Grados que estarían incluidos en la actividad / Requisitos", self.styles['SubtitleStyle']))
        grados = data.get('grados_requisitos', '')
        story.append(Paragraph(grados, self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Materiales e insumos / Presupuesto
        story.append(Paragraph("(Materiales e insumos) Presupuesto", self.styles['SubtitleStyle']))
        materiales = data.get('materiales_presupuesto', '')
        story.append(Paragraph(materiales, self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Fechas propuestas
        story.append(Paragraph("Proponer fechas para la realización de la actividad", self.styles['SubtitleStyle']))
        fechas = data.get('fechas', [])
        if fechas:
            fechas_text = ", ".join(fechas)
        else:
            fechas_text = "No se especificaron fechas"
        story.append(Paragraph(fechas_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Firma del docente
        story.append(Paragraph("Firma del Docente Responsable", self.styles['SubtitleStyle']))
        
        # Agregar imagen de firma si existe
        firma_data = data.get('firma_docente')
        if firma_data and self._procesar_firma_para_pdf(firma_data, story):
            pass  # La firma se agregó exitosamente
        else:
            # Si no hay firma, agregar espacio para firmar
            story.append(Spacer(1, 40))
            story.append(Paragraph("_________________________________", self.styles['Normal']))
            story.append(Paragraph("Firma del Docente Responsable", self.styles['FieldLabelStyle']))
        
        story.append(Spacer(1, 20))
        
        # Información de generación
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_generacion = f"Documento generado automáticamente el {fecha_generacion}"
        story.append(Spacer(1, 30))
        story.append(Paragraph(info_generacion, self.styles['FieldLabelStyle']))
    
    def _procesar_firma_para_pdf(self, firma_data, story):
        """Procesa y agrega la imagen de firma al PDF"""
        try:
            if not firma_data or not firma_data.startswith('data:image/'):
                print(f"[DEBUG] Firma no válida o vacía: {firma_data[:50] if firma_data else 'None'}")
                return False
            
            print(f"[DEBUG] Procesando firma para PDF. Tamaño: {len(firma_data)} caracteres")
            
            # Extraer datos base64 de la imagen
            header, encoded = firma_data.split(',', 1)
            print(f"[DEBUG] Header de imagen: {header}")
            
            image_data = base64.b64decode(encoded)
            print(f"[DEBUG] Datos decodificados. Tamaño: {len(image_data)} bytes")
            
            # Crear imagen desde los datos
            image_buffer = BytesIO(image_data)
            
            # Agregar la imagen al PDF con tamaño apropiado
            img = Image(image_buffer, width=3*inch, height=1.5*inch)
            story.append(img)
            story.append(Spacer(1, 10))
            story.append(Paragraph("Firma del Docente Responsable", self.styles['FieldLabelStyle']))
            
            print(f"[DEBUG] Firma agregada exitosamente al PDF")
            return True
            
        except Exception as e:
            print(f"[DEBUG] Error procesando firma para PDF: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return False
    
    def create_template_fields(self, formulario_data):
        """Crear los campos para reemplazar en el template de Google Docs"""
        
        # Formatear información del equipo
        equipo_text = self._formatear_equipo_para_template(formulario_data.get('equipo', []))
        
        # Formatear fechas
        fechas_text = ""
        if formulario_data.get('fechas'):
            fechas_text = ", ".join(formulario_data['fechas'])
        if not fechas_text.strip():
            fechas_text = "No especificado"
        
        # Procesar información de firma
        firma_info = self._procesar_firma_para_template(formulario_data.get('firma_docente'))
        
        # Crear el diccionario de campos para reemplazar
        # Función auxiliar para asegurar que no haya campos vacíos
        def ensure_not_empty(value, default="No especificado"):
            if not value or not str(value).strip():
                return default
            return str(value).strip()
        
        fields = {
            'TITULO_ACTIVIDAD': ensure_not_empty(formulario_data.get('titulo_actividad', '')),
            'DOCENTE_RESPONSABLE': ensure_not_empty(formulario_data.get('docente_responsable', '')),
            'EMAIL_RESPONSABLE': ensure_not_empty(formulario_data.get('email_responsable', '')),
            'DNI_RESPONSABLE': ensure_not_empty(formulario_data.get('dni_responsable', '')),
            'DEPARTAMENTO': ensure_not_empty(formulario_data.get('departamento', '')),
            'EQUIPO': ensure_not_empty(equipo_text),
            'FUNDAMENTACION': ensure_not_empty(formulario_data.get('fundamentacion', '')),
            'OBJETIVOS': ensure_not_empty(formulario_data.get('objetivos', '')),
            'METODOLOGIA': ensure_not_empty(formulario_data.get('metodologia', '')),
            'GRADOS': ensure_not_empty(formulario_data.get('grados', '')),
            'MATERIALES_PRESUPUESTO': ensure_not_empty(formulario_data.get('materiales_presupuesto', '')),
            'PERIODOS': ensure_not_empty(formulario_data.get('meses', '')),
            'FECHA_GENERACION': datetime.now().strftime("%d/%m/%Y"),
            'AÑO_CONVOCATORIA': str(datetime.now().year),
            'CUADRO_FIRMA': ensure_not_empty(firma_info)
        }
        
        return fields
    
    def _procesar_firma_para_template(self, firma_data):
        """Procesa la firma para el template de Google Docs"""
        if firma_data and firma_data.startswith('data:image/'):
            # Usar solo el placeholder - la imagen real se insertará via Google Apps Script
            return '[[CUADRO_FIRMA]]'
        else:
            return '\n\n\nFirma del Docente Responsable:\n\n_________________________________\n\n'
    
    def _formatear_equipo_para_template(self, equipo_data):
        """Formatear información del equipo para el template de Google Docs (incluye claustro)"""
        if not equipo_data:
            return "No se especificó equipo de trabajo."
        
        # Crear texto formateado para el equipo
        equipo_text = ""
        for i, miembro in enumerate(equipo_data, 1):
            nombre = miembro.get('apellido_nombre', '').strip()
            dni = miembro.get('dni', '').strip()
            correo = miembro.get('correo', '').strip()
            claustro = miembro.get('claustro', '').strip()
            
            if nombre:  # Solo agregar si hay al menos un nombre
                equipo_text += f"{i}. {nombre}"
                if dni:
                    equipo_text += f" (DNI: {dni})"
                if correo:
                    equipo_text += f" - {correo}"
                if claustro:
                    equipo_text += f" - Claustro: {claustro}"
                equipo_text += "\n"
        
        # Si no hay miembros válidos
        if not equipo_text.strip():
            return "No se especificó equipo de trabajo."
        
        return equipo_text.strip()