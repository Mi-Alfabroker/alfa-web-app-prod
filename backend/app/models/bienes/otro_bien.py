"""OtroBien (Other Asset) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db


class OtroBien(db.Model):
    """
    Represents other types of assets belonging to a client.
    
    This model maps to the 'otros_bienes' table and contains information
    about miscellaneous assets that don't fit into the standard categories
    (Hogar, Vehiculo, Copropiedad) but can still be insured.
    """
    __tablename__ = 'otros_bienes'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    
    # Asset information
    tipo_seguro = db.Column(db.String(255))  # Tipo de seguro aplicable
    bien_asegurado = db.Column(db.String(255))  # Descripción del bien
    valor_bien_asegurar = db.Column(db.Numeric(15, 2))
    detalles_bien_asegurado = db.Column(db.Text)  # Información adicional
    
    # Status and details
    estado = db.Column(db.String(100))  # e.g., 'Activo', 'Pendiente', 'Cancelado'
    comentarios = db.Column(db.Text)  # Additional comments or notes
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    usuario = db.relationship('Usuario', backref=db.backref('otros_bienes', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'tipo_seguro': self.tipo_seguro,
            'bien_asegurado': self.bien_asegurado,
            'valor_bien_asegurar': float(self.valor_bien_asegurar) if self.valor_bien_asegurar else None,
            'detalles_bien_asegurado': self.detalles_bien_asegurado,
            'estado': self.estado,
            'comentarios': self.comentarios,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<OtroBien {self.id}: {self.bien_asegurado}>'
