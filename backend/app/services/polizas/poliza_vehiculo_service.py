"""Business logic service for PolizaVehiculo (Vehicle Insurance Policy) operations."""
from typing import Optional, List
from datetime import date
from app.models.polizas.poliza_vehiculo import PolizaVehiculo
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza
from app.repositories.polizas import poliza_vehiculo_repository
from app.repositories.bienes.vehiculo_repository import get_by_id as vehiculo_get_by_id
from app.repositories.aseguradora_repository import AseguradoraRepository


class PolizaVehiculoService:
    """
    Business Logic Layer for PolizaVehiculo operations.
    
    Orchestrates business rules and delegates data access to the repository.
    Handles consecutive generation, state validation, and policy lifecycle.
    """

    @staticmethod
    def get_all() -> List[dict]:
        """Get all vehicle insurance policies."""
        polizas = poliza_vehiculo_repository.get_all()
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_id(poliza_id: int) -> Optional[dict]:
        """Get a vehicle insurance policy by ID."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        return poliza.to_dict() if poliza else None

    @staticmethod
    def get_by_consecutivo(consecutivo: str) -> Optional[dict]:
        """Get a vehicle insurance policy by consecutive identifier."""
        poliza = poliza_vehiculo_repository.get_by_consecutivo(consecutivo)
        return poliza.to_dict() if poliza else None

    @staticmethod
    def get_by_vehiculo_id(vehiculo_id: int) -> List[dict]:
        """Get all policies for a specific vehicle asset."""
        polizas = poliza_vehiculo_repository.get_by_bien_id(vehiculo_id)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> List[dict]:
        """Get all vehicle policies for a specific user/client."""
        polizas = poliza_vehiculo_repository.get_by_usuario_id(usuario_id)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_placa(placa: str) -> List[dict]:
        """Get all policies for a vehicle by license plate."""
        polizas = poliza_vehiculo_repository.get_by_placa(placa)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_estado(estado: str) -> List[dict]:
        """Get all policies with a specific state."""
        polizas = poliza_vehiculo_repository.get_by_estado(estado)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_por_vencer(dias: int = 30) -> List[dict]:
        """Get policies that will expire within the specified days."""
        polizas = poliza_vehiculo_repository.get_por_vencer(dias)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new vehicle insurance policy.
        
        Args:
            data: Dictionary with policy fields including id_vehiculo
            
        Returns:
            Tuple of (created policy dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_vehiculo'):
            return {}, "Field 'id_vehiculo' is required"
        
        # Validate vehicle asset exists
        vehiculo = vehiculo_get_by_id(data['id_vehiculo'])
        if not vehiculo:
            return {}, f"Vehiculo with ID {data['id_vehiculo']} not found"
        
        # Get client ID from the vehicle asset
        cliente_id = vehiculo.id_usuario
        
        # Generate consecutive if not provided
        if not data.get('consecutivo'):
            fecha = data.get('fecha_consecutivo') or date.today()
            if isinstance(fecha, str):
                fecha = date.fromisoformat(fecha)
            consecutivo = BasePolizaMixin.generar_consecutivo(
                data['id_vehiculo'], 
                cliente_id, 
                fecha
            )
            
            # Check if consecutive already exists and generate unique one
            base_consecutivo = consecutivo
            counter = 1
            while poliza_vehiculo_repository.exists_consecutivo(consecutivo):
                consecutivo = f"{base_consecutivo}-{counter}"
                counter += 1
            
            data['consecutivo'] = consecutivo
        
        # Remove helper fields not in model
        data.pop('fecha_consecutivo', None)
        
        # Validate insurance providers exist if specified
        for i in range(1, 6):
            aseg_id = data.get(f'id_aseguradora_{i}')
            if aseg_id:
                aseguradora = AseguradoraRepository.get_by_id(aseg_id)
                if not aseguradora:
                    return {}, f"Aseguradora with ID {aseg_id} not found"
        
        # Set default state if not provided
        if not data.get('estado'):
            data['estado'] = EstadoPoliza.PROSPECTO.value
        
        # Validate state
        if data.get('estado') not in [e.value for e in EstadoPoliza]:
            return {}, f"Invalid estado. Must be one of: {[e.value for e in EstadoPoliza]}"
        
        poliza = poliza_vehiculo_repository.create(data)
        return poliza.to_dict(), None

    @staticmethod
    def update(poliza_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """Update an existing vehicle insurance policy."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaVehiculo with ID {poliza_id} not found"
        
        # Validate state transition if estado is being updated
        if 'estado' in data:
            is_valid, error = poliza.validar_estado(data['estado'])
            if not is_valid:
                return {}, error
        
        # Validate insurance providers exist if being updated
        for i in range(1, 6):
            field = f'id_aseguradora_{i}'
            if field in data and data[field]:
                aseguradora = AseguradoraRepository.get_by_id(data[field])
                if not aseguradora:
                    return {}, f"Aseguradora with ID {data[field]} not found"
        
        updated = poliza_vehiculo_repository.update(poliza, data)
        return updated.to_dict(), None

    @staticmethod
    def cambiar_estado(poliza_id: int, nuevo_estado: str, aseguradora_seleccionada: Optional[int] = None) -> tuple[dict, Optional[str]]:
        """Change the state of a policy."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaVehiculo with ID {poliza_id} not found"
        
        # If changing to VIGENTE, set the selected provider first
        if nuevo_estado == EstadoPoliza.VIGENTE.value:
            if aseguradora_seleccionada is None:
                return {}, "Debe especificar aseguradora_seleccionada para activar la póliza"
            poliza.aseguradora_seleccionada = aseguradora_seleccionada
        
        # Validate state transition
        is_valid, error = poliza.validar_estado(nuevo_estado)
        if not is_valid:
            return {}, error
        
        updated = poliza_vehiculo_repository.update_estado(poliza, nuevo_estado)
        return updated.to_dict(), None

    @staticmethod
    def validar_valores_asegurados(poliza_id: int) -> tuple[bool, List[str]]:
        """Validate that insured values don't exceed appraisal values."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return False, [f"PolizaVehiculo with ID {poliza_id} not found"]
        
        vehiculo = vehiculo_get_by_id(poliza.id_vehiculo)
        if not vehiculo:
            return False, ["Associated Vehiculo not found"]
        
        errores = poliza.validar_valores_asegurados(vehiculo)
        return len(errores) == 0, errores

    @staticmethod
    def entregar_poliza(poliza_id: int, datos_entrega: dict) -> tuple[dict, Optional[str]]:
        """Deliver a policy (transition from PROSPECTO to VIGENTE)."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaVehiculo with ID {poliza_id} not found"
        
        # Validate delivery data
        is_valid, error = poliza.validar_entrega_poliza(datos_entrega)
        if not is_valid:
            return {}, error
        
        # Auto-fill insurance provider data
        aseg_sel = datos_entrega['aseguradora_seleccionada']
        aseg_id = getattr(poliza, f'id_aseguradora_{aseg_sel}')
        aseguradora = AseguradoraRepository.get_by_id(aseg_id)
        if aseguradora:
            datos_entrega['nombre_aseguradora'] = aseguradora.nombre
            datos_entrega['numeral_asistencia'] = aseguradora.numeral_asistencia
        
        # Pre-fill valor_total_prima if not provided
        if 'valor_total_prima' not in datos_entrega:
            valor_prima_attr = f'valor_prima_aseg_{aseg_sel}'
            datos_entrega['valor_total_prima'] = getattr(poliza, valor_prima_attr)
        
        # Handle financing
        if datos_entrega.get('medio_pago') == 'financiera':
            num_cuotas = datos_entrega['financiacion_num_cuotas']
            valor_cuota_attr = f'valor_cuota_{num_cuotas}'
            datos_entrega['financiacion_valor_cuota'] = getattr(poliza, valor_cuota_attr)
            
            if 'financiacion_cuota_actual' not in datos_entrega:
                datos_entrega['financiacion_cuota_actual'] = 1
            if 'estado_cartera' not in datos_entrega:
                datos_entrega['estado_cartera'] = 'pendiente'
            if 'financiacion_periodicidad' not in datos_entrega:
                datos_entrega['financiacion_periodicidad'] = 'mensual'
        else:
            datos_entrega['financiacion_num_cuotas'] = None
            datos_entrega['financiacion_cuota_actual'] = None
            datos_entrega['financiacion_valor_cuota'] = None
            datos_entrega['financiacion_fecha_primera_cuota'] = None
        
        # Transition to VIGENTE
        datos_entrega['estado'] = EstadoPoliza.VIGENTE.value
        
        # Update policy
        updated = poliza_vehiculo_repository.update(poliza, datos_entrega)
        return updated.to_dict(), None

    @staticmethod
    def actualizar_entrega(poliza_id: int, datos_actualizacion: dict) -> tuple[dict, Optional[str]]:
        """Update delivery data for an existing delivered policy."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaVehiculo with ID {poliza_id} not found"
        
        # Validate cuota_actual doesn't exceed num_cuotas if both are present
        if 'financiacion_cuota_actual' in datos_actualizacion:
            num_cuotas = datos_actualizacion.get('financiacion_num_cuotas', poliza.financiacion_num_cuotas)
            if num_cuotas and datos_actualizacion['financiacion_cuota_actual'] > num_cuotas:
                return {}, "Cuota actual no puede exceder número total de cuotas"
        
        # Update policy
        updated = poliza_vehiculo_repository.update(poliza, datos_actualizacion)
        return updated.to_dict(), None

    @staticmethod
    def delete(poliza_id: int) -> tuple[bool, Optional[str]]:
        """Delete a vehicle insurance policy."""
        poliza = poliza_vehiculo_repository.get_by_id(poliza_id)
        if not poliza:
            return False, f"PolizaVehiculo with ID {poliza_id} not found"
        
        # Business rule: Cannot delete active policies
        if poliza.estado == EstadoPoliza.VIGENTE.value:
            return False, "No se puede eliminar una póliza vigente. Debe cancelarla primero."
        
        poliza_vehiculo_repository.delete(poliza)
        return True, None
