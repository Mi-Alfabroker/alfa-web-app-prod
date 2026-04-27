"""Vehiculo (Vehicle) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db


class Vehiculo(db.Model):
    """
    Represents a vehicle asset belonging to a client.
    
    This model maps to the 'vehiculos' table and contains all information
    about vehicles that can be insured.
    """
    __tablename__ = 'vehiculos'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    
    # Vehicle information
    tipo_vehiculo = db.Column(db.String(100))  # Automóvil, Motocicleta, Camión, etc.
    placa = db.Column(db.String(10))
    marca = db.Column(db.String(100))
    serie_referencia = db.Column(db.String(100))
    ano_modelo = db.Column(db.Integer)
    ano_nacimiento_conductor = db.Column(db.Integer)
    codigo_fasecolda = db.Column(db.String(50))
    
    # Asset values
    valor_vehiculo = db.Column(db.Numeric(15, 2))
    valor_accesorios_avaluo = db.Column(db.Numeric(15, 2))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    usuario = db.relationship('Usuario', backref=db.backref('vehiculos', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'tipo_vehiculo': self.tipo_vehiculo,
            'placa': self.placa,
            'marca': self.marca,
            'serie_referencia': self.serie_referencia,
            'ano_modelo': self.ano_modelo,
            'ano_nacimiento_conductor': self.ano_nacimiento_conductor,
            'codigo_fasecolda': self.codigo_fasecolda,
            'valor_vehiculo': float(self.valor_vehiculo) if self.valor_vehiculo else None,
            'valor_accesorios_avaluo': float(self.valor_accesorios_avaluo) if self.valor_accesorios_avaluo else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<Vehiculo {self.id}: {self.placa} - {self.marca}>'
