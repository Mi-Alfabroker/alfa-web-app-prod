"""Poliza Copropiedad (Co-ownership Insurance Policy) domain model."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models import db
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza


class PolizaCopropiedad(BasePolizaMixin, db.Model):
    """
    Represents a co-ownership/condominium insurance policy.
    
    One Copropiedad (co-ownership asset) can have multiple PolizaCopropiedad (policies).
    Each policy can have up to 5 insurance provider options.
    """
    __tablename__ = 'polizas_copropiedad'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to the asset (Copropiedad)
    id_copropiedad = db.Column(
        db.Integer, 
        db.ForeignKey('copropiedades.id', ondelete='CASCADE'), 
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
    # SPECIFIC FIELDS FOR COPROPIEDAD POLICY (Insured values)
    # =========================================================================
    valor_area_comun_asegurado = db.Column(db.Numeric(15, 2))
    valor_area_privada_asegurado = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_asegurado = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_asegurado = db.Column(db.Numeric(15, 2))
    valor_muebles_asegurado = db.Column(db.Numeric(15, 2))
    valor_directores_asegurado = db.Column(db.Numeric(15, 2))
    valor_rce_asegurado = db.Column(db.Numeric(15, 2))
    valor_manejo_asegurado = db.Column(db.Numeric(15, 2))
    valor_transporte_valores_vigencia_asegurado = db.Column(db.Numeric(15, 2))
    valor_transporte_valores_despacho_asegurado = db.Column(db.Numeric(15, 2))
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    copropiedad = db.relationship(
        'Copropiedad', 
        backref=db.backref('polizas', lazy='dynamic')
    )
    
    aseguradora_1 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_1],
        backref=db.backref('polizas_copropiedad_1', lazy='dynamic')
    )
    aseguradora_2 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_2],
        backref=db.backref('polizas_copropiedad_2', lazy='dynamic')
    )
    aseguradora_3 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_3],
        backref=db.backref('polizas_copropiedad_3', lazy='dynamic')
    )
    aseguradora_4 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_4],
        backref=db.backref('polizas_copropiedad_4', lazy='dynamic')
    )
    aseguradora_5 = db.relationship(
        'Aseguradora',
        foreign_keys=[id_aseguradora_5],
        backref=db.backref('polizas_copropiedad_5', lazy='dynamic')
    )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        base = self.to_base_dict()
        specific = {
            'id': self.id,
            'id_copropiedad': self.id_copropiedad,
            'valor_area_comun_asegurado': float(self.valor_area_comun_asegurado) if self.valor_area_comun_asegurado else None,
            'valor_area_privada_asegurado': float(self.valor_area_privada_asegurado) if self.valor_area_privada_asegurado else None,
            'valor_maquinaria_equipo_asegurado': float(self.valor_maquinaria_equipo_asegurado) if self.valor_maquinaria_equipo_asegurado else None,
            'valor_equipo_electronico_asegurado': float(self.valor_equipo_electronico_asegurado) if self.valor_equipo_electronico_asegurado else None,
            'valor_muebles_asegurado': float(self.valor_muebles_asegurado) if self.valor_muebles_asegurado else None,
            'valor_directores_asegurado': float(self.valor_directores_asegurado) if self.valor_directores_asegurado else None,
            'valor_rce_asegurado': float(self.valor_rce_asegurado) if self.valor_rce_asegurado else None,
            'valor_manejo_asegurado': float(self.valor_manejo_asegurado) if self.valor_manejo_asegurado else None,
            'valor_transporte_valores_vigencia_asegurado': float(self.valor_transporte_valores_vigencia_asegurado) if self.valor_transporte_valores_vigencia_asegurado else None,
            'valor_transporte_valores_despacho_asegurado': float(self.valor_transporte_valores_despacho_asegurado) if self.valor_transporte_valores_despacho_asegurado else None,
        }
        return {**base, **specific}

    def calcular_valor_total_asegurado(self) -> float:
        """Calculate total insured value (without special coverages)."""
        total = 0
        if self.valor_area_comun_asegurado:
            total += float(self.valor_area_comun_asegurado)
        if self.valor_area_privada_asegurado:
            total += float(self.valor_area_privada_asegurado)
        if self.valor_maquinaria_equipo_asegurado:
            total += float(self.valor_maquinaria_equipo_asegurado)
        if self.valor_equipo_electronico_asegurado:
            total += float(self.valor_equipo_electronico_asegurado)
        if self.valor_muebles_asegurado:
            total += float(self.valor_muebles_asegurado)
        return total

    def calcular_valor_coberturas_especiales(self) -> float:
        """Calculate value of special coverages."""
        total = 0
        if self.valor_directores_asegurado:
            total += float(self.valor_directores_asegurado)
        if self.valor_rce_asegurado:
            total += float(self.valor_rce_asegurado)
        if self.valor_manejo_asegurado:
            total += float(self.valor_manejo_asegurado)
        if self.valor_transporte_valores_vigencia_asegurado:
            total += float(self.valor_transporte_valores_vigencia_asegurado)
        if self.valor_transporte_valores_despacho_asegurado:
            total += float(self.valor_transporte_valores_despacho_asegurado)
        return total

    def validar_valores_asegurados(self, copropiedad_avaluo) -> list[str]:
        """Validate that insured values don't exceed the asset's appraisal values."""
        errores = []
        
        if self.valor_area_comun_asegurado and copropiedad_avaluo.valor_edificio_area_comun_avaluo:
            if float(self.valor_area_comun_asegurado) > float(copropiedad_avaluo.valor_edificio_area_comun_avaluo):
                errores.append("El valor área común asegurado no puede exceder el avalúo")
        
        if self.valor_area_privada_asegurado and copropiedad_avaluo.valor_edificio_area_privada_avaluo:
            if float(self.valor_area_privada_asegurado) > float(copropiedad_avaluo.valor_edificio_area_privada_avaluo):
                errores.append("El valor área privada asegurado no puede exceder el avalúo")
        
        if self.valor_maquinaria_equipo_asegurado and copropiedad_avaluo.valor_maquinaria_equipo_avaluo:
            if float(self.valor_maquinaria_equipo_asegurado) > float(copropiedad_avaluo.valor_maquinaria_equipo_avaluo):
                errores.append("El valor maquinaria equipo asegurado no puede exceder el avalúo")
        
        if self.valor_equipo_electronico_asegurado and copropiedad_avaluo.valor_equipo_electrico_electronico_avaluo:
            if float(self.valor_equipo_electronico_asegurado) > float(copropiedad_avaluo.valor_equipo_electrico_electronico_avaluo):
                errores.append("El valor equipo electrónico asegurado no puede exceder el avalúo")
        
        if self.valor_muebles_asegurado and copropiedad_avaluo.valor_muebles_avaluo:
            if float(self.valor_muebles_asegurado) > float(copropiedad_avaluo.valor_muebles_avaluo):
                errores.append("El valor muebles asegurado no puede exceder el avalúo")
        
        return errores

    def validar_sublimites_rce(self, sublimites_aseguradora) -> list[str]:
        """Validate that RCE values meet sublimits."""
        if not self.valor_rce_asegurado or not sublimites_aseguradora:
            return []
        
        errores = []
        valor_rce = float(self.valor_rce_asegurado)
        
        if hasattr(sublimites_aseguradora, 'sublimite_rce_cop_contratistas'):
            sublimite = sublimites_aseguradora.sublimite_rce_cop_contratistas
            if sublimite and valor_rce * sublimite < 100000000:
                errores.append("RCE insuficiente para contratistas")
        
        return errores

    def __repr__(self) -> str:
        return f'<PolizaCopropiedad {self.id}: {self.consecutivo} - {self.estado}>'
