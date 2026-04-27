"""Business logic service for PolizaHogar (Home Insurance Policy) operations."""
from typing import Optional, List
from datetime import date
from app.models.polizas.poliza_hogar import PolizaHogar
from app.models.polizas.base_poliza import BasePolizaMixin, EstadoPoliza
from app.repositories.polizas import poliza_hogar_repository
from app.repositories.bienes.hogar_repository import get_by_id as hogar_get_by_id
from app.repositories.aseguradora_repository import AseguradoraRepository


class PolizaHogarService:
    """
    Business Logic Layer for PolizaHogar operations.
    
    Orchestrates business rules and delegates data access to the repository.
    Handles consecutive generation, state validation, and policy lifecycle.
    """

    @staticmethod
    def get_all() -> List[dict]:
        """
        Get all home insurance policies.
        
        Returns:
            List of policies as dictionaries
        """
        polizas = poliza_hogar_repository.get_all()
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_id(poliza_id: int) -> Optional[dict]:
        """
        Get a home insurance policy by ID.
        
        Args:
            poliza_id: The unique identifier
            
        Returns:
            Policy as dictionary or None if not found
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        return poliza.to_dict() if poliza else None

    @staticmethod
    def get_by_consecutivo(consecutivo: str) -> Optional[dict]:
        """
        Get a home insurance policy by consecutive identifier.
        
        Args:
            consecutivo: The consecutive identifier (e.g., B1C1F20260130)
            
        Returns:
            Policy as dictionary or None if not found
        """
        poliza = poliza_hogar_repository.get_by_consecutivo(consecutivo)
        return poliza.to_dict() if poliza else None

    @staticmethod
    def get_by_hogar_id(hogar_id: int) -> List[dict]:
        """
        Get all policies for a specific home asset.
        
        Args:
            hogar_id: The home asset's unique identifier
            
        Returns:
            List of policies as dictionaries
        """
        polizas = poliza_hogar_repository.get_by_bien_id(hogar_id)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> List[dict]:
        """
        Get all home policies for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of policies as dictionaries
        """
        polizas = poliza_hogar_repository.get_by_usuario_id(usuario_id)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_by_estado(estado: str) -> List[dict]:
        """
        Get all policies with a specific state.
        
        Args:
            estado: The policy state (PROSPECTO, VIGENTE, VENCIDA, CANCELADA)
            
        Returns:
            List of policies as dictionaries
        """
        polizas = poliza_hogar_repository.get_by_estado(estado)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def get_por_vencer(dias: int = 30) -> List[dict]:
        """
        Get policies that will expire within the specified days.
        
        Args:
            dias: Number of days to check for expiration
            
        Returns:
            List of policies about to expire
        """
        polizas = poliza_hogar_repository.get_por_vencer(dias)
        return [p.to_dict() for p in polizas]

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new home insurance policy.
        
        Args:
            data: Dictionary with policy fields including id_hogar
            
        Returns:
            Tuple of (created policy dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_hogar'):
            return {}, "Field 'id_hogar' is required"
        
        # Validate home asset exists
        hogar = hogar_get_by_id(data['id_hogar'])
        if not hogar:
            return {}, f"Hogar with ID {data['id_hogar']} not found"
        
        # Get client ID from the home asset
        cliente_id = hogar.id_usuario
        
        # Generate consecutive if not provided
        if not data.get('consecutivo'):
            fecha = data.get('fecha_consecutivo') or date.today()
            if isinstance(fecha, str):
                fecha = date.fromisoformat(fecha)
            consecutivo = BasePolizaMixin.generar_consecutivo(
                data['id_hogar'], 
                cliente_id, 
                fecha
            )
            
            # Check if consecutive already exists and generate unique one
            base_consecutivo = consecutivo
            counter = 1
            while poliza_hogar_repository.exists_consecutivo(consecutivo):
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
        
        poliza = poliza_hogar_repository.create(data)
        return poliza.to_dict(), None

    @staticmethod
    def update(poliza_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing home insurance policy.
        
        Args:
            poliza_id: The ID of the policy to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated policy dict, error message or None)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaHogar with ID {poliza_id} not found"
        
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
        
        updated = poliza_hogar_repository.update(poliza, data)
        return updated.to_dict(), None

    @staticmethod
    def cambiar_estado(poliza_id: int, nuevo_estado: str, aseguradora_seleccionada: Optional[int] = None) -> tuple[dict, Optional[str]]:
        """
        Change the state of a policy.
        
        Args:
            poliza_id: The ID of the policy
            nuevo_estado: The new state
            aseguradora_seleccionada: Required when changing to VIGENTE (1-5)
            
        Returns:
            Tuple of (updated policy dict, error message or None)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaHogar with ID {poliza_id} not found"
        
        # If changing to VIGENTE, set the selected provider first
        if nuevo_estado == EstadoPoliza.VIGENTE.value:
            if aseguradora_seleccionada is None:
                return {}, "Debe especificar aseguradora_seleccionada para activar la póliza"
            poliza.aseguradora_seleccionada = aseguradora_seleccionada
        
        # Validate state transition
        is_valid, error = poliza.validar_estado(nuevo_estado)
        if not is_valid:
            return {}, error
        
        updated = poliza_hogar_repository.update_estado(poliza, nuevo_estado)
        return updated.to_dict(), None

    @staticmethod
    def validar_valores_asegurados(poliza_id: int) -> tuple[bool, List[str]]:
        """
        Validate that insured values don't exceed appraisal values.
        
        Args:
            poliza_id: The policy ID
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return False, [f"PolizaHogar with ID {poliza_id} not found"]
        
        hogar = hogar_get_by_id(poliza.id_hogar)
        if not hogar:
            return False, ["Associated Hogar not found"]
        
        errores = poliza.validar_valores_asegurados(hogar)
        return len(errores) == 0, errores

    @staticmethod
    def entregar_poliza(poliza_id: int, datos_entrega: dict) -> tuple[dict, Optional[str]]:
        """
        Deliver a policy (transition from PROSPECTO to VIGENTE).
        
        This method:
        1. Validates delivery data using validar_entrega_poliza()
        2. Auto-fills insurance provider data (nombre_aseguradora, numeral_asistencia)
        3. Pre-fills valor_total_prima from valor_prima_aseg_X
        4. Copies pre-calculated installment value to financiacion_valor_cuota
        5. Initializes financing fields if medio_pago='financiera'
        6. Transitions state to VIGENTE
        
        Args:
            poliza_id: The ID of the policy to deliver
            datos_entrega: Dictionary with delivery data including:
                - aseguradora_seleccionada (1-5, required)
                - numero_poliza_aseguradora (required)
                - inicio_vigencia (required)
                - fin_vigencia (optional)
                - valor_total_prima (optional, pre-filled if not provided)
                - valor_prima_neta (optional)
                - valor_otros_costos (optional)
                - valor_iva (optional)
                - medio_pago ('contado' or 'financiera', required)
                - estado_cartera (optional)
                - financiacion_num_cuotas (required if medio_pago='financiera')
                - financiacion_fecha_primera_cuota (required if medio_pago='financiera')
                - ingreso_comision_percibido (optional)
            
        Returns:
            Tuple of (updated policy dict, error message or None)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaHogar with ID {poliza_id} not found"
        
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
            # Copy pre-calculated installment value
            valor_cuota_attr = f'valor_cuota_{num_cuotas}'
            datos_entrega['financiacion_valor_cuota'] = getattr(poliza, valor_cuota_attr)
            
            # Initialize cuota_actual and estado_cartera if not provided
            if 'financiacion_cuota_actual' not in datos_entrega:
                datos_entrega['financiacion_cuota_actual'] = 1
            if 'estado_cartera' not in datos_entrega:
                datos_entrega['estado_cartera'] = 'pendiente'
            if 'financiacion_periodicidad' not in datos_entrega:
                datos_entrega['financiacion_periodicidad'] = 'mensual'
        else:
            # Clear financing fields for 'contado'
            datos_entrega['financiacion_num_cuotas'] = None
            datos_entrega['financiacion_cuota_actual'] = None
            datos_entrega['financiacion_valor_cuota'] = None
            datos_entrega['financiacion_fecha_primera_cuota'] = None
        
        # Transition to VIGENTE
        datos_entrega['estado'] = EstadoPoliza.VIGENTE.value
        
        # Update policy
        updated = poliza_hogar_repository.update(poliza, datos_entrega)
        
        # TODO: Add audit logging here
        # logger.info(f"Policy {poliza_id} delivered by user {current_user_id}")
        
        return updated.to_dict(), None

    @staticmethod
    def actualizar_entrega(poliza_id: int, datos_actualizacion: dict) -> tuple[dict, Optional[str]]:
        """
        Update delivery data for an existing delivered policy.
        
        This is a lighter validation than entregar_poliza - it allows updating
        fields without re-validating the full delivery process. Useful for
        manual management of estado_cartera, financiacion_cuota_actual, etc.
        
        Args:
            poliza_id: The ID of the policy
            datos_actualizacion: Dictionary with fields to update
            
        Returns:
            Tuple of (updated policy dict, error message or None)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaHogar with ID {poliza_id} not found"
        
        # Validate cuota_actual doesn't exceed num_cuotas if both are present
        if 'financiacion_cuota_actual' in datos_actualizacion:
            num_cuotas = datos_actualizacion.get('financiacion_num_cuotas', poliza.financiacion_num_cuotas)
            if num_cuotas and datos_actualizacion['financiacion_cuota_actual'] > num_cuotas:
                return {}, "Cuota actual no puede exceder número total de cuotas"
        
        # Update policy
        updated = poliza_hogar_repository.update(poliza, datos_actualizacion)
        return updated.to_dict(), None

    @staticmethod
    def delete(poliza_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a home insurance policy.
        
        Args:
            poliza_id: The ID of the policy to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return False, f"PolizaHogar with ID {poliza_id} not found"
        
        # Business rule: Cannot delete active policies
        if poliza.estado == EstadoPoliza.VIGENTE.value:
            return False, "No se puede eliminar una póliza vigente. Debe cancelarla primero."
        
        poliza_hogar_repository.delete(poliza)
        return True, None
