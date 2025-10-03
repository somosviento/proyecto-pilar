from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class FormularioActividad(db.Model):
    __tablename__ = 'formularios_actividad'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campos del formulario
    titulo_actividad = db.Column(db.Text, nullable=False)
    docente_responsable = db.Column(db.String(200), nullable=False)
    email_responsable = db.Column(db.String(200), nullable=False)  # Email del docente responsable
    dni_responsable = db.Column(db.String(20), nullable=False)  # DNI del docente responsable
    departamento = db.Column(db.String(200))  # Departamento/Instituto de pertenencia
    
    # Equipo (guardado como JSON)
    equipo_json = db.Column(db.Text)  # JSON string con el array de miembros del equipo
    
    fundamentacion = db.Column(db.Text, nullable=False)
    objetivos = db.Column(db.Text, nullable=False)
    metodologia = db.Column(db.Text, nullable=False)
    grados = db.Column(db.Text)
    materiales_presupuesto = db.Column(db.Text)
    
    # Períodos (año + meses) guardado como JSON
    periodos_json = db.Column(db.Text)  # JSON string con formato [{"ano": "2025", "meses": ["Marzo", "Abril"]}, ...]
    meses = db.Column(db.Text)  # Texto legible de períodos para mostrar (ej: "2025: Marzo, Abril | 2026: Mayo")
    
    # Metadatos del formulario
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # IDs de Google Drive
    documento_id = db.Column(db.String(100))  # ID del documento generado en Google Drive
    carpeta_id = db.Column(db.String(100))    # ID de la carpeta en Google Drive
    
    # Estado del procesamiento
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, procesado, error
    
    @property
    def equipo(self):
        """Deserializa el equipo desde JSON"""
        if self.equipo_json:
            try:
                return json.loads(self.equipo_json)
            except:
                return []
        return []
    
    @equipo.setter
    def equipo(self, value):
        """Serializa el equipo a JSON"""
        if value:
            self.equipo_json = json.dumps(value)
        else:
            self.equipo_json = None
    
    @property
    def periodos(self):
        """Deserializa los períodos desde JSON"""
        if self.periodos_json:
            try:
                return json.loads(self.periodos_json)
            except:
                return []
        return []
    
    @periodos.setter
    def periodos(self, value):
        """Serializa los períodos a JSON"""
        if value:
            self.periodos_json = json.dumps(value)
        else:
            self.periodos_json = None
    
    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar el uso"""
        return {
            'id': self.id,
            'titulo_actividad': self.titulo_actividad,
            'docente_responsable': self.docente_responsable,
            'email_responsable': self.email_responsable,
            'dni_responsable': self.dni_responsable,
            'departamento': self.departamento,
            'equipo': self.equipo,
            'fundamentacion': self.fundamentacion,
            'objetivos': self.objetivos,
            'metodologia': self.metodologia,
            'grados': self.grados,
            'materiales_presupuesto': self.materiales_presupuesto,
            'periodos': self.periodos,
            'meses': self.meses,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'documento_id': self.documento_id,
            'carpeta_id': self.carpeta_id,
            'estado': self.estado
        }
    
    def __repr__(self):
        return f'<FormularioActividad {self.id}: {self.titulo_actividad}>'