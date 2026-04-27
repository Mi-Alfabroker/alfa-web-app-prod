"""Copropiedad (Co-ownership/Condominium) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db


class Copropiedad(db.Model):
    """
    Represents a co-ownership/condominium property asset belonging to a client.
    
    This model maps to the 'copropiedades' table and contains all information
    about co-ownership properties (condominiums, residential complexes) that can be insured.
    """
    __tablename__ = 'copropiedades'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    
    # Property information
    tipo_copropiedad = db.Column(db.String(100))  # Residencial, Comercial, Mixto
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    estrato = db.Column(db.Integer)
    ano_construccion = db.Column(db.Integer)
    
    # Building structure
    numero_torres = db.Column(db.Integer)
    numero_maximo_pisos = db.Column(db.Integer)
    numero_maximo_sotanos = db.Column(db.Integer)
    
    # Unit counts
    cantidad_unidades_casa = db.Column(db.Integer)
    cantidad_unidades_apartamentos = db.Column(db.Integer)
    cantidad_unidades_locales = db.Column(db.Integer)
    cantidad_unidades_oficinas = db.Column(db.Integer)
    cantidad_unidades_otros = db.Column(db.Integer)
    
    # Asset values (avaluo)
    valor_edificio_area_comun_avaluo = db.Column(db.Numeric(15, 2))
    valor_edificio_area_privada_avaluo = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_avaluo = db.Column(db.Numeric(15, 2))
    valor_equipo_electrico_electronico_avaluo = db.Column(db.Numeric(15, 2))
    valor_muebles_avaluo = db.Column(db.Numeric(15, 2))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    usuario = db.relationship('Usuario', backref=db.backref('copropiedades', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'tipo_copropiedad': self.tipo_copropiedad,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'estrato': self.estrato,
            'ano_construccion': self.ano_construccion,
            'numero_torres': self.numero_torres,
            'numero_maximo_pisos': self.numero_maximo_pisos,
            'numero_maximo_sotanos': self.numero_maximo_sotanos,
            'cantidad_unidades_casa': self.cantidad_unidades_casa,
            'cantidad_unidades_apartamentos': self.cantidad_unidades_apartamentos,
            'cantidad_unidades_locales': self.cantidad_unidades_locales,
            'cantidad_unidades_oficinas': self.cantidad_unidades_oficinas,
            'cantidad_unidades_otros': self.cantidad_unidades_otros,
            'valor_edificio_area_comun_avaluo': float(self.valor_edificio_area_comun_avaluo) if self.valor_edificio_area_comun_avaluo else None,
            'valor_edificio_area_privada_avaluo': float(self.valor_edificio_area_privada_avaluo) if self.valor_edificio_area_privada_avaluo else None,
            'valor_maquinaria_equipo_avaluo': float(self.valor_maquinaria_equipo_avaluo) if self.valor_maquinaria_equipo_avaluo else None,
            'valor_equipo_electrico_electronico_avaluo': float(self.valor_equipo_electrico_electronico_avaluo) if self.valor_equipo_electrico_electronico_avaluo else None,
            'valor_muebles_avaluo': float(self.valor_muebles_avaluo) if self.valor_muebles_avaluo else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<Copropiedad {self.id}: {self.tipo_copropiedad} - {self.direccion}>'
