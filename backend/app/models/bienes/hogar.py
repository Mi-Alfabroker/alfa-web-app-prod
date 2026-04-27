"""Hogar (Home) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db


class Hogar(db.Model):
    """
    Represents a home/residential property asset belonging to a client.
    
    This model maps to the 'hogares' table and contains all information
    about residential properties that can be insured.
    """
    __tablename__ = 'hogares'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    
    # Property information
    tipo_inmueble = db.Column(db.String(100))  # Casa, Apartamento, Finca, etc.
    ciudad_inmueble = db.Column(db.String(100))
    direccion_inmueble = db.Column(db.String(255))
    numero_pisos = db.Column(db.Integer)
    ano_construccion = db.Column(db.Integer)
    
    # Asset values (avaluo)
    valor_inmueble_avaluo = db.Column(db.Numeric(15, 2))
    valor_contenidos_normales_avaluo = db.Column(db.Numeric(15, 2))
    valor_contenidos_especiales_avaluo = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_avaluo = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_avaluo = db.Column(db.Numeric(15, 2))
    
    # Status and details
    estado = db.Column(db.String(100))  # e.g., 'Activo', 'Pendiente', 'Cancelado'
    comentarios_detalles = db.Column(db.Text)  # Additional notes or details
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    usuario = db.relationship('Usuario', backref=db.backref('hogares', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'tipo_inmueble': self.tipo_inmueble,
            'ciudad_inmueble': self.ciudad_inmueble,
            'direccion_inmueble': self.direccion_inmueble,
            'numero_pisos': self.numero_pisos,
            'ano_construccion': self.ano_construccion,
            'valor_inmueble_avaluo': float(self.valor_inmueble_avaluo) if self.valor_inmueble_avaluo else None,
            'valor_contenidos_normales_avaluo': float(self.valor_contenidos_normales_avaluo) if self.valor_contenidos_normales_avaluo else None,
            'valor_contenidos_especiales_avaluo': float(self.valor_contenidos_especiales_avaluo) if self.valor_contenidos_especiales_avaluo else None,
            'valor_equipo_electronico_avaluo': float(self.valor_equipo_electronico_avaluo) if self.valor_equipo_electronico_avaluo else None,
            'valor_maquinaria_equipo_avaluo': float(self.valor_maquinaria_equipo_avaluo) if self.valor_maquinaria_equipo_avaluo else None,
            'estado': self.estado,
            'comentarios_detalles': self.comentarios_detalles,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<Hogar {self.id}: {self.tipo_inmueble} - {self.direccion_inmueble}>'
