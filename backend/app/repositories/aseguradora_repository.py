"""Repository for Aseguradora data access operations."""
from typing import Optional
from app.models import db
from app.models.aseguradora import Aseguradora


class AseguradoraRepository:
    """
    Data Access Layer for Aseguradora entities.
    
    Handles all database CRUD operations for insurance providers.
    Following the Repository Pattern to abstract data persistence.
    """

    @staticmethod
    def get_all() -> list[Aseguradora]:
        """Retrieve all insurance providers."""
        return Aseguradora.query.all()

    @staticmethod
    def get_by_id(aseguradora_id: int) -> Optional[Aseguradora]:
        """Retrieve an insurance provider by its ID."""
        return Aseguradora.query.get(aseguradora_id)

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Aseguradora]:
        """Retrieve an insurance provider by its name."""
        return Aseguradora.query.filter_by(nombre=nombre).first()

    @staticmethod
    def create(data: dict) -> Aseguradora:
        """
        Create a new insurance provider.
        
        Args:
            data: Dictionary with aseguradora fields
            
        Returns:
            The created Aseguradora instance
        """
        aseguradora = Aseguradora(
            # Base fields
            nombre=data.get('nombre'),
            numeral_asistencia=data.get('numeral_asistencia'),
            correo_comercial=data.get('correo_comercial'),
            correo_reclamaciones=data.get('correo_reclamaciones'),
            direccion_oficina=data.get('direccion_oficina'),
            contacto_asignado=data.get('contacto_asignado'),
            ruta_logo=data.get('ruta_logo'),
            ruta_pais_logo=data.get('ruta_pais_logo'),
            respaldo_aseguradora=data.get('respaldo_aseguradora'),
            
            # Copropiedad - Asistencia
            cop_asistencia_area_comun=data.get('cop_asistencia_area_comun'),
            cop_asistencia_area_privada=data.get('cop_asistencia_area_privada'),
            
            # Copropiedad - Daños Materiales
            cop_dm_deducible_terremoto=data.get('cop_dm_deducible_terremoto'),
            cop_dm_deducible_inundacion=data.get('cop_dm_deducible_inundacion'),
            cop_dm_deducible_incendio=data.get('cop_dm_deducible_incendio'),
            cop_dm_deducible_amit=data.get('cop_dm_deducible_amit'),
            cop_dm_deducible_tuberia_vidrio=data.get('cop_dm_deducible_tuberia_vidrio'),
            
            # Copropiedad - Daños Internos
            cop_di_deducible_maq_equipo=data.get('cop_di_deducible_maq_equipo'),
            cop_di_deducible_equipo_electronico=data.get('cop_di_deducible_equipo_electronico'),
            
            # Copropiedad - Sustracción con Violencia
            cop_scv_deducible_maq_equipo=data.get('cop_scv_deducible_maq_equipo'),
            cop_scv_deducible_equipo_electronico=data.get('cop_scv_deducible_equipo_electronico'),
            cop_scv_deducible_dineros=data.get('cop_scv_deducible_dineros'),
            cop_scv_deducible_muebles=data.get('cop_scv_deducible_muebles'),
            
            # Copropiedad - Directores & Administradores
            cop_da_deducible_amparo_basico=data.get('cop_da_deducible_amparo_basico'),
            
            # Copropiedad - RCE Deducibles
            cop_rce_deducible_contratistas=data.get('cop_rce_deducible_contratistas'),
            cop_rce_deducible_cruzada=data.get('cop_rce_deducible_cruzada'),
            cop_rce_deducible_patronal=data.get('cop_rce_deducible_patronal'),
            cop_rce_deducible_parqueaderos=data.get('cop_rce_deducible_parqueaderos'),
            cop_rce_deducible_gastos_medicos=data.get('cop_rce_deducible_gastos_medicos'),
            
            # Copropiedad - RCE Sublimites
            cop_rce_sublimite_contratistas=data.get('cop_rce_sublimite_contratistas'),
            cop_rce_sublimite_cruzada=data.get('cop_rce_sublimite_cruzada'),
            cop_rce_sublimite_patronal=data.get('cop_rce_sublimite_patronal'),
            cop_rce_sublimite_parqueaderos=data.get('cop_rce_sublimite_parqueaderos'),
            cop_rce_sublimite_gastos_medicos=data.get('cop_rce_sublimite_gastos_medicos'),
            
            # Copropiedad - Manejo
            cop_manejo_deducible_amparo_basico=data.get('cop_manejo_deducible_amparo_basico'),
            
            # Copropiedad - Transporte de Valores
            cop_tv_deducible_amparo_basico=data.get('cop_tv_deducible_amparo_basico'),
            
            # Hogar - Deducibles
            hog_deducible_terremoto=data.get('hog_deducible_terremoto'),
            hog_deducible_amit=data.get('hog_deducible_amit'),
            hog_deducible_demas_eventos=data.get('hog_deducible_demas_eventos'),
            
            # Hogar - Hurto Contenidos Normales (CN)
            hog_hurto_cn_terremoto=data.get('hog_hurto_cn_terremoto'),
            hog_hurto_cn_demas_eventos=data.get('hog_hurto_cn_demas_eventos'),
            hog_hurto_cn_hurto=data.get('hog_hurto_cn_hurto'),
            
            # Hogar - Hurto Contenidos Especiales (CE) y Especialmente Especiales (EE)
            hog_hurto_ce_hurto=data.get('hog_hurto_ce_hurto'),
            hog_hurto_ee_hurto=data.get('hog_hurto_ee_hurto'),
            
            # Hogar - Coberturas Adicionales
            hog_cobertura_adicional_1=data.get('hog_cobertura_adicional_1'),
            hog_cobertura_adicional_2=data.get('hog_cobertura_adicional_2'),
            hog_cobertura_adicional_3=data.get('hog_cobertura_adicional_3'),
            
            # Hogar - Valores Asegurados
            hog_valor_asegurado_inmueble=data.get('hog_valor_asegurado_inmueble'),
            hog_valor_asegurado_contenidos_normales=data.get('hog_valor_asegurado_contenidos_normales'),
            hog_valor_asegurado_contenidos_especiales=data.get('hog_valor_asegurado_contenidos_especiales'),
            hog_valor_asegurado_equipo_electronico=data.get('hog_valor_asegurado_equipo_electronico'),
            
            # Vehículos - Valores Asegurados
            veh_valor_asegurado_vehiculo=data.get('veh_valor_asegurado_vehiculo'),
            veh_valor_asegurado_accesorios=data.get('veh_valor_asegurado_accesorios'),
            veh_valor_asegurado_rc=data.get('veh_valor_asegurado_rc'),
            
            # Vehículos - Deducibles Pérdida
            veh_deducible_perdida_parcial=data.get('veh_deducible_perdida_parcial'),
            veh_deducible_perdida_total=data.get('veh_deducible_perdida_total'),
            veh_deducible_terremoto=data.get('veh_deducible_terremoto'),
            
            # Vehículos - Deducibles Hurto
            veh_hurto_perdida_parcial=data.get('veh_hurto_perdida_parcial'),
            veh_hurto_perdida_total=data.get('veh_hurto_perdida_total'),
            
            # Vehículos - Deducible RC
            veh_deducible_rc=data.get('veh_deducible_rc'),
            
            # Vehículos - Sublímites RC
            veh_rc_sublimite_bienes_terceros=data.get('veh_rc_sublimite_bienes_terceros'),
            veh_rc_sublimite_amparo_patrimonial=data.get('veh_rc_sublimite_amparo_patrimonial'),
            veh_rc_sublimite_muerte_lesion_una=data.get('veh_rc_sublimite_muerte_lesion_una'),
            veh_rc_sublimite_muerte_lesion_dos_mas=data.get('veh_rc_sublimite_muerte_lesion_dos_mas'),
            
            # Vehículos - Coberturas Adicionales
            veh_cobertura_adicional_1=data.get('veh_cobertura_adicional_1'),
            veh_cobertura_adicional_2=data.get('veh_cobertura_adicional_2'),
            veh_cobertura_adicional_3=data.get('veh_cobertura_adicional_3'),
            veh_cobertura_adicional_4=data.get('veh_cobertura_adicional_4'),
            veh_cobertura_adicional_5=data.get('veh_cobertura_adicional_5'),
            veh_cobertura_adicional_6=data.get('veh_cobertura_adicional_6'),
            veh_cobertura_adicional_7=data.get('veh_cobertura_adicional_7'),
            
            # Otros - Valores Asegurados
            otr_valor_asegurado_inmueble=data.get('otr_valor_asegurado_inmueble'),
            otr_valor_asegurado_contenidos_normales=data.get('otr_valor_asegurado_contenidos_normales'),
            otr_valor_asegurado_contenidos_especiales=data.get('otr_valor_asegurado_contenidos_especiales'),
            otr_valor_asegurado_equipo_electronico=data.get('otr_valor_asegurado_equipo_electronico'),
            
            # Otros - Deducibles Daños
            otr_deducible_terremoto=data.get('otr_deducible_terremoto'),
            otr_deducible_amit=data.get('otr_deducible_amit'),
            otr_deducible_demas_eventos=data.get('otr_deducible_demas_eventos'),
            
            # Otros - Deducibles Hurto
            otr_hurto_cn_deducible=data.get('otr_hurto_cn_deducible'),
            otr_hurto_ce_deducible=data.get('otr_hurto_ce_deducible'),
            otr_hurto_ee_deducible=data.get('otr_hurto_ee_deducible'),
            
            # Otros - Coberturas Adicionales
            otr_cobertura_adicional_1=data.get('otr_cobertura_adicional_1'),
            otr_cobertura_adicional_2=data.get('otr_cobertura_adicional_2'),
            otr_cobertura_adicional_3=data.get('otr_cobertura_adicional_3'),
        )
        db.session.add(aseguradora)
        db.session.commit()
        return aseguradora

    @staticmethod
    def update(aseguradora: Aseguradora, data: dict) -> Aseguradora:
        """
        Update an existing insurance provider.
        
        Args:
            aseguradora: The Aseguradora instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated Aseguradora instance
        """
        updatable_fields = [
            # Base fields
            'nombre', 'numeral_asistencia', 'correo_comercial',
            'correo_reclamaciones', 'direccion_oficina', 'contacto_asignado',
            'ruta_logo', 'ruta_pais_logo', 'respaldo_aseguradora',
            # Copropiedad - Asistencia
            'cop_asistencia_area_comun', 'cop_asistencia_area_privada',
            # Copropiedad - Daños Materiales
            'cop_dm_deducible_terremoto', 'cop_dm_deducible_inundacion',
            'cop_dm_deducible_incendio', 'cop_dm_deducible_amit',
            'cop_dm_deducible_tuberia_vidrio',
            # Copropiedad - Daños Internos
            'cop_di_deducible_maq_equipo', 'cop_di_deducible_equipo_electronico',
            # Copropiedad - Sustracción con Violencia
            'cop_scv_deducible_maq_equipo', 'cop_scv_deducible_equipo_electronico',
            'cop_scv_deducible_dineros', 'cop_scv_deducible_muebles',
            # Copropiedad - Directores & Administradores
            'cop_da_deducible_amparo_basico',
            # Copropiedad - RCE Deducibles
            'cop_rce_deducible_contratistas', 'cop_rce_deducible_cruzada',
            'cop_rce_deducible_patronal', 'cop_rce_deducible_parqueaderos',
            'cop_rce_deducible_gastos_medicos',
            # Copropiedad - RCE Sublimites
            'cop_rce_sublimite_contratistas', 'cop_rce_sublimite_cruzada',
            'cop_rce_sublimite_patronal', 'cop_rce_sublimite_parqueaderos',
            'cop_rce_sublimite_gastos_medicos',
            # Copropiedad - Manejo
            'cop_manejo_deducible_amparo_basico',
            # Copropiedad - Transporte de Valores
            'cop_tv_deducible_amparo_basico',
            # Hogar - Deducibles
            'hog_deducible_terremoto', 'hog_deducible_amit', 'hog_deducible_demas_eventos',
            # Hogar - Hurto Contenidos Normales
            'hog_hurto_cn_terremoto', 'hog_hurto_cn_demas_eventos', 'hog_hurto_cn_hurto',
            # Hogar - Hurto CE y EE
            'hog_hurto_ce_hurto', 'hog_hurto_ee_hurto',
            # Hogar - Coberturas Adicionales
            'hog_cobertura_adicional_1', 'hog_cobertura_adicional_2', 'hog_cobertura_adicional_3',
            # Hogar - Valores Asegurados
            'hog_valor_asegurado_inmueble', 'hog_valor_asegurado_contenidos_normales',
            'hog_valor_asegurado_contenidos_especiales', 'hog_valor_asegurado_equipo_electronico',
            # Vehículos - Valores Asegurados
            'veh_valor_asegurado_vehiculo', 'veh_valor_asegurado_accesorios', 'veh_valor_asegurado_rc',
            # Vehículos - Deducibles Pérdida
            'veh_deducible_perdida_parcial', 'veh_deducible_perdida_total', 'veh_deducible_terremoto',
            # Vehículos - Deducibles Hurto
            'veh_hurto_perdida_parcial', 'veh_hurto_perdida_total',
            # Vehículos - Deducible RC
            'veh_deducible_rc',
            # Vehículos - Sublímites RC
            'veh_rc_sublimite_bienes_terceros', 'veh_rc_sublimite_amparo_patrimonial',
            'veh_rc_sublimite_muerte_lesion_una', 'veh_rc_sublimite_muerte_lesion_dos_mas',
            # Vehículos - Coberturas Adicionales
            'veh_cobertura_adicional_1', 'veh_cobertura_adicional_2', 'veh_cobertura_adicional_3',
            'veh_cobertura_adicional_4', 'veh_cobertura_adicional_5', 'veh_cobertura_adicional_6',
            'veh_cobertura_adicional_7',
            # Otros - Valores Asegurados
            'otr_valor_asegurado_inmueble', 'otr_valor_asegurado_contenidos_normales',
            'otr_valor_asegurado_contenidos_especiales', 'otr_valor_asegurado_equipo_electronico',
            # Otros - Deducibles Daños
            'otr_deducible_terremoto', 'otr_deducible_amit', 'otr_deducible_demas_eventos',
            # Otros - Deducibles Hurto
            'otr_hurto_cn_deducible', 'otr_hurto_ce_deducible', 'otr_hurto_ee_deducible',
            # Otros - Coberturas Adicionales
            'otr_cobertura_adicional_1', 'otr_cobertura_adicional_2', 'otr_cobertura_adicional_3',
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(aseguradora, field, data[field])
        
        db.session.commit()
        return aseguradora

    @staticmethod
    def delete(aseguradora: Aseguradora) -> bool:
        """
        Delete an insurance provider.
        
        Args:
            aseguradora: The Aseguradora instance to delete
            
        Returns:
            True if deletion was successful
        """
        db.session.delete(aseguradora)
        db.session.commit()
        return True
