"""Poliza OtroBien (Other Asset Insurance Policy) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza


class PolizaOtroBien(BasePolizaMixin, db.Model):
    """
    Represents an insurance policy for other types of assets.
    
    One OtroBien (other asset) can have multiple PolizaOtroBien (policies).
    Each policy can have up to 5 insurance provider options.
    """
    __tablename__ = 'polizas_otro_bien'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the asset (OtroBien)
    id_otro_bien = db.Column(
        db.Integer, 
        db.ForeignKey('otros_bienes.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    
    # Foreign keys to insurance providers (up to 5 options)
    id_aseguradora_1 = db.Column(
        db.Integer,
        db.ForeignKey('aseguradoras.id', ondelete='SET NULL'),
        nullable=True
    )
    id_aseguradora_2 = db.Column(
        db.Integer,
        db.ForeignKey('aseguradoras.id', ondelete='SET NULL'),
        nullable=True
    )
    id_aseguradora_3 = db.Column(
        db.Integer,
        db.ForeignKey('aseguradoras.id', ondelete='SET NULL'),
        nullable=True
    )
    id_aseguradora_4 = db.Column(
        db.Integer,
        db.ForeignKey('aseguradoras.id', ondelete='SET NULL'),
        nullable=True
    )
    id_aseguradora_5 = db.Column(
        db.Integer,
        db.ForeignKey('aseguradoras.id', ondelete='SET NULL'),
        nullable=True
    )
    
    # =========================================================================
    # SPECIFIC FIELDS FOR OTRO BIEN POLICY (Insured values)
    # =========================================================================
    valor_asegurado = db.Column(db.Numeric(15, 2))
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    otro_bien = db.relationship(
        'OtroBien', 
        backref=db.backref('polizas', lazy='dynamic')
    )
    
    aseguradora_1 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_1],
        backref=db.backref('polizas_otro_bien_1', lazy='dynamic')
    )
    aseguradora_2 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_2],
        backref=db.backref('polizas_otro_bien_2', lazy='dynamic')
    )
    aseguradora_3 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_3],
        backref=db.backref('polizas_otro_bien_3', lazy='dynamic')
    )
    aseguradora_4 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_4],
        backref=db.backref('polizas_otro_bien_4', lazy='dynamic')
    )
    aseguradora_5 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_5],
        backref=db.backref('polizas_otro_bien_5', lazy='dynamic')
    )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        base = self.to_base_dict()
        specific = {
            'id': self.id,
            'id_otro_bien': self.id_otro_bien,
            'valor_asegurado': float(self.valor_asegurado) if self.valor_asegurado else None,
        }
        return {**base, **specific}

    def calcular_valor_total_asegurado(self) -> float:
        """Calculate total insured value."""
        return float(self.valor_asegurado) if self.valor_asegurado else 0

    def validar_valores_asegurados(self, otro_bien_avaluo) -> list[str]:
        """Validate that insured value doesn't exceed the asset's appraisal value."""
        errores = []
        
        if self.valor_asegurado and otro_bien_avaluo.valor_bien_asegurar:
            if float(self.valor_asegurado) > float(otro_bien_avaluo.valor_bien_asegurar):
                errores.append("El valor asegurado no puede exceder el avalúo del bien")
        
        return errores

    def es_valor_minimo_suficiente(self, valor_minimo_requerido: int = 1000000) -> tuple[bool, str]:
        """Verify if the insured value meets minimum requirements."""
        if not self.valor_asegurado:
            return False, "Debe especificar un valor asegurado"
        
        valor = float(self.valor_asegurado)
        if valor < valor_minimo_requerido:
            return False, f"El valor asegurado debe ser al menos {valor_minimo_requerido:,.0f}"
        
        return True, "Valor asegurado válido"

    def __repr__(self) -> str:
        return f'<PolizaOtroBien {self.id}: {self.consecutivo} - {self.estado}>'
