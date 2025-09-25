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
    
    # Equipo (guardado como JSON)
    equipo_json = db.Column(db.Text)  # JSON string con el array de miembros del equipo
    
    fundamentacion = db.Column(db.Text, nullable=False)
    objetivos = db.Column(db.Text, nullable=False)
    metodologia = db.Column(db.Text, nullable=False)
    grados = db.Column(db.Text)
    requisitos = db.Column(db.Text)
    materiales_presupuesto = db.Column(db.Text)
    meses = db.Column(db.Text)  # Meses propuestos separados por comas
    fechas_propuestas = db.Column(db.Text)  # JSON string con las fechas
    
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
    def fechas(self):
        """Deserializa las fechas desde JSON"""
        if self.fechas_propuestas:
            try:
                return json.loads(self.fechas_propuestas)
            except:
                return []
        return []
    
    @fechas.setter
    def fechas(self, value):
        """Serializa las fechas a JSON"""
        if value:
            self.fechas_propuestas = json.dumps(value)
        else:
            self.fechas_propuestas = None
    
    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar el uso"""
        return {
            'id': self.id,
            'titulo_actividad': self.titulo_actividad,
            'docente_responsable': self.docente_responsable,
            'equipo': self.equipo,
            'fundamentacion': self.fundamentacion,
            'objetivos': self.objetivos,
            'metodologia': self.metodologia,
            'grados': self.grados,
            'requisitos': self.requisitos,
            'materiales_presupuesto': self.materiales_presupuesto,
            'meses': self.meses,
            'fechas': self.fechas,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'documento_id': self.documento_id,
            'carpeta_id': self.carpeta_id,
            'estado': self.estado
        }
    
    def __repr__(self):
        return f'<FormularioActividad {self.id}: {self.titulo_actividad}>'