"""Aseguradora (Insurance Provider) domain model."""
from datetime import datetime
from app.models import db


class Aseguradora(db.Model):
    """
    Represents an insurance provider entity.
    
    This model maps to the 'aseguradoras' table and contains
    all the information about insurance companies that the agency works with.
    """
    __tablename__ = 'aseguradoras'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    numeral_asistencia = db.Column(db.String(50))
    correo_comercial = db.Column(db.String(255))
    correo_reclamaciones = db.Column(db.String(255))
    direccion_oficina = db.Column(db.Text)
    contacto_asignado = db.Column(db.String(255))
    ruta_logo = db.Column(db.String(500))
    ruta_pais_logo = db.Column(db.String(500))
    respaldo_aseguradora = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # =========================================================================
    # CAMPOS PARA COPROPIEDAD
    # =========================================================================

    # Asistencia - Copropiedad
    cop_asistencia_area_comun = db.Column(db.String(255))    # vidrieria, plomeria, cerrajeria, electricista
    cop_asistencia_area_privada = db.Column(db.String(255))  # vidrieria, plomeria, cerrajeria, electricista

    # -------------------------------------------------------------------------
    # COBERTURA: DAÑOS MATERIALES
    # -------------------------------------------------------------------------
    cop_dm_deducible_terremoto = db.Column(db.String(255))      # porcentaje,tipo,minimo
    cop_dm_deducible_inundacion = db.Column(db.String(255))     # porcentaje,tipo,minimo
    cop_dm_deducible_incendio = db.Column(db.String(255))       # porcentaje,tipo,minimo
    cop_dm_deducible_amit = db.Column(db.String(255))           # porcentaje,tipo,minimo
    cop_dm_deducible_tuberia_vidrio = db.Column(db.String(255)) # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: DAÑOS INTERNOS
    # -------------------------------------------------------------------------
    cop_di_deducible_maq_equipo = db.Column(db.String(255))        # porcentaje,tipo,minimo
    cop_di_deducible_equipo_electronico = db.Column(db.String(255)) # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: SUSTRACCION CON VIOLENCIA
    # -------------------------------------------------------------------------
    cop_scv_deducible_maq_equipo = db.Column(db.String(255))        # porcentaje,tipo,minimo
    cop_scv_deducible_equipo_electronico = db.Column(db.String(255)) # porcentaje,tipo,minimo
    cop_scv_deducible_dineros = db.Column(db.String(255))           # porcentaje,tipo,minimo
    cop_scv_deducible_muebles = db.Column(db.String(255))           # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: DIRECTORES & ADMINISTRADORES
    # -------------------------------------------------------------------------
    cop_da_deducible_amparo_basico = db.Column(db.String(255))  # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: RCE - DEDUCIBLES
    # -------------------------------------------------------------------------
    cop_rce_deducible_contratistas = db.Column(db.String(255))   # porcentaje,tipo,minimo
    cop_rce_deducible_cruzada = db.Column(db.String(255))        # porcentaje,tipo,minimo
    cop_rce_deducible_patronal = db.Column(db.String(255))       # porcentaje,tipo,minimo
    cop_rce_deducible_parqueaderos = db.Column(db.String(255))   # porcentaje,tipo,minimo
    cop_rce_deducible_gastos_medicos = db.Column(db.String(255)) # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: RCE - SUBLIMITES
    # -------------------------------------------------------------------------
    cop_rce_sublimite_contratistas = db.Column(db.String(255))   # porcentaje,tipo,minimo
    cop_rce_sublimite_cruzada = db.Column(db.String(255))        # porcentaje,tipo,minimo
    cop_rce_sublimite_patronal = db.Column(db.String(255))       # porcentaje,tipo,minimo
    cop_rce_sublimite_parqueaderos = db.Column(db.String(255))   # porcentaje,tipo,minimo
    cop_rce_sublimite_gastos_medicos = db.Column(db.String(255)) # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: MANEJO
    # -------------------------------------------------------------------------
    cop_manejo_deducible_amparo_basico = db.Column(db.String(255))  # porcentaje,tipo,minimo

    # -------------------------------------------------------------------------
    # COBERTURA: TRANSPORTE DE VALORES
    # -------------------------------------------------------------------------
    cop_tv_deducible_amparo_basico = db.Column(db.String(255))  # porcentaje,tipo,minimo

    # =========================================================================
    # CAMPOS PARA HOGAR
    # =========================================================================
    # Deducibles Daños - Hogar
    hog_deducible_terremoto = db.Column(db.String(255))      # porcentaje,tipo,minimo
    hog_deducible_amit = db.Column(db.String(255))           # porcentaje,tipo,minimo
    hog_deducible_demas_eventos = db.Column(db.String(255))  # porcentaje,tipo,minimo

    # Deducibles Hurto Contenidos Normales - Hogar
    hog_hurto_cn_terremoto = db.Column(db.String(255))       # porcentaje,tipo,minimo
    hog_hurto_cn_demas_eventos = db.Column(db.String(255))   # porcentaje,tipo,minimo
    hog_hurto_cn_hurto = db.Column(db.String(255))           # porcentaje,tipo,minimo

    # Deducibles Hurto Contenidos Especiales - Hogar
    hog_hurto_ce_hurto = db.Column(db.String(255))           # porcentaje,tipo,minimo

    # Deducibles Hurto Equipo Electrónico - Hogar
    hog_hurto_ee_hurto = db.Column(db.String(255))           # porcentaje,tipo,minimo

    # Valores Asegurados - Hogar
    hog_valor_asegurado_inmueble = db.Column(db.String(255))
    hog_valor_asegurado_contenidos_normales = db.Column(db.String(255))
    hog_valor_asegurado_contenidos_especiales = db.Column(db.String(255))
    hog_valor_asegurado_equipo_electronico = db.Column(db.String(255))

    # Coberturas Adicionales - Hogar
    hog_cobertura_adicional_1 = db.Column(db.String(255))
    hog_cobertura_adicional_2 = db.Column(db.String(255))
    hog_cobertura_adicional_3 = db.Column(db.String(255))

    # =========================================================================
    # CAMPOS PARA VEHÍCULOS
    # =========================================================================
    # Valores Asegurados - Vehículos
    veh_valor_asegurado_vehiculo = db.Column(db.String(255))
    veh_valor_asegurado_accesorios = db.Column(db.String(255))
    veh_valor_asegurado_rc = db.Column(db.String(255))

    # Deducibles Daños - Vehículos
    veh_deducible_perdida_parcial = db.Column(db.String(255))  # porcentaje,tipo,minimo
    veh_deducible_perdida_total = db.Column(db.String(255))    # porcentaje,tipo,minimo
    veh_deducible_terremoto = db.Column(db.String(255))        # porcentaje,tipo,minimo

    # Deducibles Hurto - Vehículos
    veh_hurto_perdida_parcial = db.Column(db.String(255))      # porcentaje,tipo,minimo
    veh_hurto_perdida_total = db.Column(db.String(255))        # porcentaje,tipo,minimo

    # Deducible RC - Vehículos
    veh_deducible_rc = db.Column(db.String(255))               # porcentaje,tipo,minimo

    # Sublímites RC - Vehículos
    veh_rc_sublimite_bienes_terceros = db.Column(db.String(255))
    veh_rc_sublimite_amparo_patrimonial = db.Column(db.String(255))
    veh_rc_sublimite_muerte_lesion_una = db.Column(db.String(255))
    veh_rc_sublimite_muerte_lesion_dos_mas = db.Column(db.String(255))

    # Coberturas Adicionales - Vehículos
    veh_cobertura_adicional_1 = db.Column(db.String(255))
    veh_cobertura_adicional_2 = db.Column(db.String(255))
    veh_cobertura_adicional_3 = db.Column(db.String(255))
    veh_cobertura_adicional_4 = db.Column(db.String(255))
    veh_cobertura_adicional_5 = db.Column(db.String(255))
    veh_cobertura_adicional_6 = db.Column(db.String(255))
    veh_cobertura_adicional_7 = db.Column(db.String(255))

    # =========================================================================
    # CAMPOS PARA OTROS
    # =========================================================================
    # Valores Asegurados - Otros
    otr_valor_asegurado_inmueble = db.Column(db.String(255))
    otr_valor_asegurado_contenidos_normales = db.Column(db.String(255))
    otr_valor_asegurado_contenidos_especiales = db.Column(db.String(255))
    otr_valor_asegurado_equipo_electronico = db.Column(db.String(255))

    # Deducibles Daños - Otros
    otr_deducible_terremoto = db.Column(db.String(255))        # porcentaje,tipo,minimo
    otr_deducible_amit = db.Column(db.String(255))             # porcentaje,tipo,minimo
    otr_deducible_demas_eventos = db.Column(db.String(255))    # porcentaje,tipo,minimo

    # Deducibles Hurto - Otros
    otr_hurto_cn_deducible = db.Column(db.String(255))         # porcentaje,tipo,minimo
    otr_hurto_ce_deducible = db.Column(db.String(255))         # porcentaje,tipo,minimo
    otr_hurto_ee_deducible = db.Column(db.String(255))         # porcentaje,tipo,minimo

    # Coberturas Adicionales - Otros
    otr_cobertura_adicional_1 = db.Column(db.String(255))
    otr_cobertura_adicional_2 = db.Column(db.String(255))
    otr_cobertura_adicional_3 = db.Column(db.String(255))






    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        return {
            # Base fields
            'id': self.id,
            'nombre': self.nombre,
            'numeral_asistencia': self.numeral_asistencia,
            'correo_comercial': self.correo_comercial,
            'correo_reclamaciones': self.correo_reclamaciones,
            'direccion_oficina': self.direccion_oficina,
            'contacto_asignado': self.contacto_asignado,
            'ruta_logo': self.ruta_logo,
            'ruta_pais_logo': self.ruta_pais_logo,
            'respaldo_aseguradora': self.respaldo_aseguradora,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            
            # Copropiedad - Asistencia
            'cop_asistencia_area_comun': self.cop_asistencia_area_comun,
            'cop_asistencia_area_privada': self.cop_asistencia_area_privada,
            
            # Copropiedad - Daños Materiales
            'cop_dm_deducible_terremoto': self.cop_dm_deducible_terremoto,
            'cop_dm_deducible_inundacion': self.cop_dm_deducible_inundacion,
            'cop_dm_deducible_incendio': self.cop_dm_deducible_incendio,
            'cop_dm_deducible_amit': self.cop_dm_deducible_amit,
            'cop_dm_deducible_tuberia_vidrio': self.cop_dm_deducible_tuberia_vidrio,
            
            # Copropiedad - Daños Internos
            'cop_di_deducible_maq_equipo': self.cop_di_deducible_maq_equipo,
            'cop_di_deducible_equipo_electronico': self.cop_di_deducible_equipo_electronico,
            
            # Copropiedad - Sustracción con Violencia
            'cop_scv_deducible_maq_equipo': self.cop_scv_deducible_maq_equipo,
            'cop_scv_deducible_equipo_electronico': self.cop_scv_deducible_equipo_electronico,
            'cop_scv_deducible_dineros': self.cop_scv_deducible_dineros,
            'cop_scv_deducible_muebles': self.cop_scv_deducible_muebles,
            
            # Copropiedad - Directores & Administradores
            'cop_da_deducible_amparo_basico': self.cop_da_deducible_amparo_basico,
            
            # Copropiedad - RCE Deducibles
            'cop_rce_deducible_contratistas': self.cop_rce_deducible_contratistas,
            'cop_rce_deducible_cruzada': self.cop_rce_deducible_cruzada,
            'cop_rce_deducible_patronal': self.cop_rce_deducible_patronal,
            'cop_rce_deducible_parqueaderos': self.cop_rce_deducible_parqueaderos,
            'cop_rce_deducible_gastos_medicos': self.cop_rce_deducible_gastos_medicos,
            
            # Copropiedad - RCE Sublimites
            'cop_rce_sublimite_contratistas': self.cop_rce_sublimite_contratistas,
            'cop_rce_sublimite_cruzada': self.cop_rce_sublimite_cruzada,
            'cop_rce_sublimite_patronal': self.cop_rce_sublimite_patronal,
            'cop_rce_sublimite_parqueaderos': self.cop_rce_sublimite_parqueaderos,
            'cop_rce_sublimite_gastos_medicos': self.cop_rce_sublimite_gastos_medicos,
            
            # Copropiedad - Manejo
            'cop_manejo_deducible_amparo_basico': self.cop_manejo_deducible_amparo_basico,
            
            # Copropiedad - Transporte de Valores
            'cop_tv_deducible_amparo_basico': self.cop_tv_deducible_amparo_basico,
            
            # Hogar - Deducibles Daños
            'hog_deducible_terremoto': self.hog_deducible_terremoto,
            'hog_deducible_amit': self.hog_deducible_amit,
            'hog_deducible_demas_eventos': self.hog_deducible_demas_eventos,
            
            # Hogar - Deducibles Hurto Contenidos Normales
            'hog_hurto_cn_terremoto': self.hog_hurto_cn_terremoto,
            'hog_hurto_cn_demas_eventos': self.hog_hurto_cn_demas_eventos,
            'hog_hurto_cn_hurto': self.hog_hurto_cn_hurto,
            
            # Hogar - Deducibles Hurto Contenidos Especiales
            'hog_hurto_ce_hurto': self.hog_hurto_ce_hurto,
            
            # Hogar - Deducibles Hurto Equipo Electrónico
            'hog_hurto_ee_hurto': self.hog_hurto_ee_hurto,
            
            # Hogar - Valores Asegurados
            'hog_valor_asegurado_inmueble': self.hog_valor_asegurado_inmueble,
            'hog_valor_asegurado_contenidos_normales': self.hog_valor_asegurado_contenidos_normales,
            'hog_valor_asegurado_contenidos_especiales': self.hog_valor_asegurado_contenidos_especiales,
            'hog_valor_asegurado_equipo_electronico': self.hog_valor_asegurado_equipo_electronico,
            
            # Hogar - Coberturas Adicionales
            'hog_cobertura_adicional_1': self.hog_cobertura_adicional_1,
            'hog_cobertura_adicional_2': self.hog_cobertura_adicional_2,
            'hog_cobertura_adicional_3': self.hog_cobertura_adicional_3,
            
            # Vehículos - Valores Asegurados
            'veh_valor_asegurado_vehiculo': self.veh_valor_asegurado_vehiculo,
            'veh_valor_asegurado_accesorios': self.veh_valor_asegurado_accesorios,
            'veh_valor_asegurado_rc': self.veh_valor_asegurado_rc,
            
            # Vehículos - Deducibles Daños
            'veh_deducible_perdida_parcial': self.veh_deducible_perdida_parcial,
            'veh_deducible_perdida_total': self.veh_deducible_perdida_total,
            'veh_deducible_terremoto': self.veh_deducible_terremoto,
            
            # Vehículos - Deducibles Hurto
            'veh_hurto_perdida_parcial': self.veh_hurto_perdida_parcial,
            'veh_hurto_perdida_total': self.veh_hurto_perdida_total,
            
            # Vehículos - Deducible RC
            'veh_deducible_rc': self.veh_deducible_rc,
            
            # Vehículos - Sublímites RC
            'veh_rc_sublimite_bienes_terceros': self.veh_rc_sublimite_bienes_terceros,
            'veh_rc_sublimite_amparo_patrimonial': self.veh_rc_sublimite_amparo_patrimonial,
            'veh_rc_sublimite_muerte_lesion_una': self.veh_rc_sublimite_muerte_lesion_una,
            'veh_rc_sublimite_muerte_lesion_dos_mas': self.veh_rc_sublimite_muerte_lesion_dos_mas,
            
            # Vehículos - Coberturas Adicionales
            'veh_cobertura_adicional_1': self.veh_cobertura_adicional_1,
            'veh_cobertura_adicional_2': self.veh_cobertura_adicional_2,
            'veh_cobertura_adicional_3': self.veh_cobertura_adicional_3,
            'veh_cobertura_adicional_4': self.veh_cobertura_adicional_4,
            'veh_cobertura_adicional_5': self.veh_cobertura_adicional_5,
            'veh_cobertura_adicional_6': self.veh_cobertura_adicional_6,
            'veh_cobertura_adicional_7': self.veh_cobertura_adicional_7,
            
            # Otros - Valores Asegurados
            'otr_valor_asegurado_inmueble': self.otr_valor_asegurado_inmueble,
            'otr_valor_asegurado_contenidos_normales': self.otr_valor_asegurado_contenidos_normales,
            'otr_valor_asegurado_contenidos_especiales': self.otr_valor_asegurado_contenidos_especiales,
            'otr_valor_asegurado_equipo_electronico': self.otr_valor_asegurado_equipo_electronico,
            
            # Otros - Deducibles Daños
            'otr_deducible_terremoto': self.otr_deducible_terremoto,
            'otr_deducible_amit': self.otr_deducible_amit,
            'otr_deducible_demas_eventos': self.otr_deducible_demas_eventos,
            
            # Otros - Deducibles Hurto
            'otr_hurto_cn_deducible': self.otr_hurto_cn_deducible,
            'otr_hurto_ce_deducible': self.otr_hurto_ce_deducible,
            'otr_hurto_ee_deducible': self.otr_hurto_ee_deducible,
            
            # Otros - Coberturas Adicionales
            'otr_cobertura_adicional_1': self.otr_cobertura_adicional_1,
            'otr_cobertura_adicional_2': self.otr_cobertura_adicional_2,
            'otr_cobertura_adicional_3': self.otr_cobertura_adicional_3,
        }

    def __repr__(self) -> str:
        return f'<Aseguradora {self.id}: {self.nombre}>'
