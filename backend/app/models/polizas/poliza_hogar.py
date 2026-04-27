"""Poliza Hogar (Home Insurance Policy) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza


class PolizaHogar(BasePolizaMixin, db.Model):
    """
    Represents a home insurance policy.
    
    One Hogar (home asset) can have multiple PolizaHogar (policies).
    Each policy can have up to 5 insurance provider options.
    """
    __tablename__ = 'polizas_hogar'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the asset (Hogar)
    id_hogar = db.Column(
        db.Integer, 
        db.ForeignKey('hogares.id', ondelete='CASCADE'), 
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
    # SPECIFIC FIELDS FOR HOGAR POLICY (Insured values)
    # =========================================================================
    valor_inmueble_asegurado = db.Column(db.Numeric(15, 2))
    valor_contenidos_normales_asegurado = db.Column(db.Numeric(15, 2))
    valor_contenidos_especiales_asegurado = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_asegurado = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_asegurado = db.Column(db.Numeric(15, 2))
    valor_rc_asegurado = db.Column(db.Numeric(15, 2))
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    hogar = db.relationship(
        'Hogar', 
        backref=db.backref('polizas', lazy='dynamic')
    )
    
    aseguradora_1 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_1],
        backref=db.backref('polizas_hogar_1', lazy='dynamic')
    )
    aseguradora_2 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_2],
        backref=db.backref('polizas_hogar_2', lazy='dynamic')
    )
    aseguradora_3 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_3],
        backref=db.backref('polizas_hogar_3', lazy='dynamic')
    )
    aseguradora_4 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_4],
        backref=db.backref('polizas_hogar_4', lazy='dynamic')
    )
    aseguradora_5 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_5],
        backref=db.backref('polizas_hogar_5', lazy='dynamic')
    )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        base = self.to_base_dict()
        specific = {
            'id': self.id,
            'id_hogar': self.id_hogar,
            'valor_inmueble_asegurado': float(self.valor_inmueble_asegurado) if self.valor_inmueble_asegurado else None,
            'valor_contenidos_normales_asegurado': float(self.valor_contenidos_normales_asegurado) if self.valor_contenidos_normales_asegurado else None,
            'valor_contenidos_especiales_asegurado': float(self.valor_contenidos_especiales_asegurado) if self.valor_contenidos_especiales_asegurado else None,
            'valor_equipo_electronico_asegurado': float(self.valor_equipo_electronico_asegurado) if self.valor_equipo_electronico_asegurado else None,
            'valor_maquinaria_equipo_asegurado': float(self.valor_maquinaria_equipo_asegurado) if self.valor_maquinaria_equipo_asegurado else None,
            'valor_rc_asegurado': float(self.valor_rc_asegurado) if self.valor_rc_asegurado else None,
        }
        return {**base, **specific}

    def calcular_valor_total_asegurado(self) -> float:
        """Calculate total insured value (excluding RC)."""
        total = 0
        if self.valor_inmueble_asegurado:
            total += float(self.valor_inmueble_asegurado)
        if self.valor_contenidos_normales_asegurado:
            total += float(self.valor_contenidos_normales_asegurado)
        if self.valor_contenidos_especiales_asegurado:
            total += float(self.valor_contenidos_especiales_asegurado)
        if self.valor_equipo_electronico_asegurado:
            total += float(self.valor_equipo_electronico_asegurado)
        if self.valor_maquinaria_equipo_asegurado:
            total += float(self.valor_maquinaria_equipo_asegurado)
        return total

    def validar_valores_asegurados(self, hogar_avaluo) -> list[str]:
        """Validate that insured values don't exceed the asset's appraisal values."""
        errores = []
        
        if self.valor_inmueble_asegurado and hogar_avaluo.valor_inmueble_avaluo:
            if float(self.valor_inmueble_asegurado) > float(hogar_avaluo.valor_inmueble_avaluo):
                errores.append("El valor inmueble asegurado no puede exceder el avalúo")
        
        if self.valor_contenidos_normales_asegurado and hogar_avaluo.valor_contenidos_normales_avaluo:
            if float(self.valor_contenidos_normales_asegurado) > float(hogar_avaluo.valor_contenidos_normales_avaluo):
                errores.append("El valor contenidos normales asegurado no puede exceder el avalúo")
        
        if self.valor_contenidos_especiales_asegurado and hogar_avaluo.valor_contenidos_especiales_avaluo:
            if float(self.valor_contenidos_especiales_asegurado) > float(hogar_avaluo.valor_contenidos_especiales_avaluo):
                errores.append("El valor contenidos especiales asegurado no puede exceder el avalúo")
        
        if self.valor_equipo_electronico_asegurado and hogar_avaluo.valor_equipo_electronico_avaluo:
            if float(self.valor_equipo_electronico_asegurado) > float(hogar_avaluo.valor_equipo_electronico_avaluo):
                errores.append("El valor equipo electrónico asegurado no puede exceder el avalúo")
        
        if self.valor_maquinaria_equipo_asegurado and hogar_avaluo.valor_maquinaria_equipo_avaluo:
            if float(self.valor_maquinaria_equipo_asegurado) > float(hogar_avaluo.valor_maquinaria_equipo_avaluo):
                errores.append("El valor maquinaria equipo asegurado no puede exceder el avalúo")
        
        return errores

    def __repr__(self) -> str:
        return f'<PolizaHogar {self.id}: {self.consecutivo} - {self.estado}>'
