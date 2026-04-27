"""Poliza Vehiculo (Vehicle Insurance Policy) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza


class PolizaVehiculo(BasePolizaMixin, db.Model):
    """
    Represents a vehicle insurance policy.
    
    One Vehiculo (vehicle asset) can have multiple PolizaVehiculo (policies).
    Each policy can have up to 5 insurance provider options.
    """
    __tablename__ = 'polizas_vehiculo'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the asset (Vehiculo)
    id_vehiculo = db.Column(
        db.Integer, 
        db.ForeignKey('vehiculos.id', ondelete='CASCADE'), 
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
    # SPECIFIC FIELDS FOR VEHICULO POLICY (Insured values)
    # =========================================================================
    valor_vehiculo_asegurado = db.Column(db.Numeric(15, 2))
    valor_accesorios_asegurado = db.Column(db.Numeric(15, 2))
    valor_rc_asegurado = db.Column(db.Numeric(15, 2))
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    vehiculo = db.relationship(
        'Vehiculo', 
        backref=db.backref('polizas', lazy='dynamic')
    )
    
    aseguradora_1 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_1],
        backref=db.backref('polizas_vehiculo_1', lazy='dynamic')
    )
    aseguradora_2 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_2],
        backref=db.backref('polizas_vehiculo_2', lazy='dynamic')
    )
    aseguradora_3 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_3],
        backref=db.backref('polizas_vehiculo_3', lazy='dynamic')
    )
    aseguradora_4 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_4],
        backref=db.backref('polizas_vehiculo_4', lazy='dynamic')
    )
    aseguradora_5 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_5],
        backref=db.backref('polizas_vehiculo_5', lazy='dynamic')
    )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        base = self.to_base_dict()
        specific = {
            'id': self.id,
            'id_vehiculo': self.id_vehiculo,
            'valor_vehiculo_asegurado': float(self.valor_vehiculo_asegurado) if self.valor_vehiculo_asegurado else None,
            'valor_accesorios_asegurado': float(self.valor_accesorios_asegurado) if self.valor_accesorios_asegurado else None,
            'valor_rc_asegurado': float(self.valor_rc_asegurado) if self.valor_rc_asegurado else None,
        }
        return {**base, **specific}

    def calcular_valor_total_asegurado(self) -> float:
        """Calculate total insured value (excluding RC)."""
        total = 0
        if self.valor_vehiculo_asegurado:
            total += float(self.valor_vehiculo_asegurado)
        if self.valor_accesorios_asegurado:
            total += float(self.valor_accesorios_asegurado)
        return total

    def validar_valores_asegurados(self, vehiculo_avaluo) -> list[str]:
        """Validate that insured values don't exceed the asset's appraisal values."""
        errores = []
        
        if self.valor_vehiculo_asegurado and vehiculo_avaluo.valor_vehiculo:
            if float(self.valor_vehiculo_asegurado) > float(vehiculo_avaluo.valor_vehiculo):
                errores.append("El valor del vehículo asegurado no puede exceder el avalúo")
        
        if self.valor_accesorios_asegurado and vehiculo_avaluo.valor_accesorios_avaluo:
            if float(self.valor_accesorios_asegurado) > float(vehiculo_avaluo.valor_accesorios_avaluo):
                errores.append("El valor de accesorios asegurado no puede exceder el avalúo")
        
        return errores

    def es_valor_minimo_rc_suficiente(self, sublimites_aseguradora) -> tuple[bool, list[str]]:
        """Verify if the RC value meets minimum sublimits."""
        if not self.valor_rc_asegurado:
            return False, ["Debe especificar un valor de RC"]
        
        errores = []
        valor_rc = float(self.valor_rc_asegurado)
        
        if sublimites_aseguradora:
            if hasattr(sublimites_aseguradora, 'sublimite_rc_veh_bienes_terceros'):
                sublimite = sublimites_aseguradora.sublimite_rc_veh_bienes_terceros
                if sublimite and valor_rc * sublimite < 50000000:
                    errores.append("RC insuficiente para bienes de terceros")
        
        return len(errores) == 0, errores

    def __repr__(self) -> str:
        return f'<PolizaVehiculo {self.id}: {self.consecutivo} - {self.estado}>'
