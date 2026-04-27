"""Base Poliza (Insurance Policy) abstract model with common fields."""
from datetime import datetime, date
from enum import Enum
from typing import Optional
from app.models import db


class EstadoPoliza(str, Enum):
    """Possible states for an insurance policy."""
    PROSPECTO = "PROSPECTO"
    VIGENTE = "VIGENTE"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"


class BasePolizaMixin:
    """
    Mixin class containing common fields for all policy types.
    
    This mixin provides:
    - Consecutive identifier (format: B{bien_id}C{cliente_id}F{date})
    - Policy state management
    - Validity period dates
    - Up to 5 insurance provider options with their premiums
    - Selected provider tracking
    - Financial fields for calculations
    """
    
    # Consecutive identifier: B{bien_id}C{cliente_id}F{YYYYMMDD}
    consecutivo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Policy state
    estado = db.Column(
        db.String(20), 
        nullable=False, 
        default=EstadoPoliza.PROSPECTO.value,
        index=True
    )
    
    # Validity period
    inicio_vigencia = db.Column(db.Date, nullable=True)
    fin_vigencia = db.Column(db.Date, nullable=True)
    
    # Insurance provider premium values (1-5 options)
    valor_prima_aseg_1 = db.Column(db.BigInteger, nullable=True)
    valor_prima_aseg_2 = db.Column(db.BigInteger, nullable=True)
    valor_prima_aseg_3 = db.Column(db.BigInteger, nullable=True)
    valor_prima_aseg_4 = db.Column(db.BigInteger, nullable=True)
    valor_prima_aseg_5 = db.Column(db.BigInteger, nullable=True)
    
    # Selected insurance provider (1-5) when policy is active
    aseguradora_seleccionada = db.Column(db.SmallInteger, nullable=True)
    
    # Policy number assigned by the insurance provider
    numero_poliza_aseguradora = db.Column(db.String(100), nullable=True)
    
    # Financial values for calculations (stored as integers)
    valor_prima_neta = db.Column(db.BigInteger, nullable=True)
    valor_otros_costos = db.Column(db.BigInteger, nullable=True)
    valor_iva = db.Column(db.BigInteger, nullable=True)
    ingreso_comision_percibido = db.Column(db.BigInteger, nullable=True)
    
    # =========================================================================
    # DELIVERY / ENTREGA FIELDS - Added for policy delivery process
    # =========================================================================
    
    # Selected insurance provider information (denormalized for performance)
    nombre_aseguradora = db.Column(db.String(255), nullable=True)
    numeral_asistencia = db.Column(db.String(100), nullable=True)
    
    # Total premium value (can be modified from valor_prima_aseg_X)
    valor_total_prima = db.Column(db.BigInteger, nullable=True)
    
    # Payment method and portfolio status
    medio_pago = db.Column(db.String(20), nullable=True)  # 'contado' or 'financiera'
    estado_cartera = db.Column(db.String(20), nullable=True)  # 'recaudado', 'pendiente', 'cancelado', 'en_solicitud'
    
    # =========================================================================
    # FINANCING FIELDS - For installment payment plans
    # =========================================================================
    
    # Installment plan details
    financiacion_num_cuotas = db.Column(db.SmallInteger, nullable=True)  # 3, 5, 8, or 11
    financiacion_cuota_actual = db.Column(db.SmallInteger, nullable=True)  # Current installment number
    financiacion_valor_cuota = db.Column(db.BigInteger, nullable=True)  # Value per installment
    financiacion_fecha_primera_cuota = db.Column(db.Date, nullable=True)  # First payment date
    financiacion_periodicidad = db.Column(db.String(20), default='mensual', nullable=True)  # 'mensual', 'bimestral', 'trimestral'
    
    # Pre-calculated installment values (saved when generating proposal)
    # These ensure consistency with the values shown to the client in the PDF
    valor_cuota_3 = db.Column(db.BigInteger, nullable=True)  # 3-installment plan value
    valor_cuota_5 = db.Column(db.BigInteger, nullable=True)  # 5-installment plan value
    valor_cuota_8 = db.Column(db.BigInteger, nullable=True)  # 8-installment plan value
    valor_cuota_11 = db.Column(db.BigInteger, nullable=True)  # 11-installment plan value
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def generar_consecutivo(bien_id: int, cliente_id: int, fecha: Optional[date] = None) -> str:
        """
        Generate the consecutive identifier for the policy.
        
        Format: B{bien_id}C{cliente_id}F{YYYYMMDD}
        Example: B1C1F20260130
        
        Args:
            bien_id: The asset ID
            cliente_id: The client/user ID
            fecha: Optional date, defaults to today
            
        Returns:
            Formatted consecutive string
        """
        if fecha is None:
            fecha = date.today()
        fecha_str = fecha.strftime("%Y%m%d")
        return f"B{bien_id}C{cliente_id}F{fecha_str}"

    def validar_estado(self, nuevo_estado: str) -> tuple[bool, Optional[str]]:
        """
        Validate if the state transition is allowed.
        
        Args:
            nuevo_estado: The new state to transition to
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        estados_validos = [e.value for e in EstadoPoliza]
        if nuevo_estado not in estados_validos:
            return False, f"Estado inválido. Estados permitidos: {estados_validos}"
        
        # Business rules for state transitions
        if self.estado == EstadoPoliza.CANCELADA.value:
            return False, "Una póliza cancelada no puede cambiar de estado"
        
        if nuevo_estado == EstadoPoliza.VIGENTE.value:
            if not self.aseguradora_seleccionada:
                return False, "Debe seleccionar una aseguradora para activar la póliza"
            if self.aseguradora_seleccionada < 1 or self.aseguradora_seleccionada > 5:
                return False, "La aseguradora seleccionada debe estar entre 1 y 5"
        
        return True, None

    def to_base_dict(self) -> dict:
        """Convert common policy fields to dictionary."""
        return {
            'consecutivo': self.consecutivo,
            'estado': self.estado,
            'inicio_vigencia': self.inicio_vigencia.isoformat() if self.inicio_vigencia else None,
            'fin_vigencia': self.fin_vigencia.isoformat() if self.fin_vigencia else None,
            'valor_prima_aseg_1': self.valor_prima_aseg_1,
            'valor_prima_aseg_2': self.valor_prima_aseg_2,
            'valor_prima_aseg_3': self.valor_prima_aseg_3,
            'valor_prima_aseg_4': self.valor_prima_aseg_4,
            'valor_prima_aseg_5': self.valor_prima_aseg_5,
            'id_aseguradora_1': self.id_aseguradora_1 if hasattr(self, 'id_aseguradora_1') else None,
            'id_aseguradora_2': self.id_aseguradora_2 if hasattr(self, 'id_aseguradora_2') else None,
            'id_aseguradora_3': self.id_aseguradora_3 if hasattr(self, 'id_aseguradora_3') else None,
            'id_aseguradora_4': self.id_aseguradora_4 if hasattr(self, 'id_aseguradora_4') else None,
            'id_aseguradora_5': self.id_aseguradora_5 if hasattr(self, 'id_aseguradora_5') else None,
            'aseguradora_seleccionada': self.aseguradora_seleccionada,
            'numero_poliza_aseguradora': self.numero_poliza_aseguradora,
            'valor_prima_neta': self.valor_prima_neta,
            'valor_otros_costos': self.valor_otros_costos,
            'valor_iva': self.valor_iva,
            'ingreso_comision_percibido': self.ingreso_comision_percibido,
            # Delivery / Entrega fields
            'nombre_aseguradora': self.nombre_aseguradora,
            'numeral_asistencia': self.numeral_asistencia,
            'valor_total_prima': self.valor_total_prima,
            'medio_pago': self.medio_pago,
            'estado_cartera': self.estado_cartera,
            # Financing fields
            'financiacion_num_cuotas': self.financiacion_num_cuotas,
            'financiacion_cuota_actual': self.financiacion_cuota_actual,
            'financiacion_valor_cuota': self.financiacion_valor_cuota,
            'financiacion_fecha_primera_cuota': self.financiacion_fecha_primera_cuota.isoformat() if self.financiacion_fecha_primera_cuota else None,
            'financiacion_periodicidad': self.financiacion_periodicidad,
            'valor_cuota_3': self.valor_cuota_3,
            'valor_cuota_5': self.valor_cuota_5,
            'valor_cuota_8': self.valor_cuota_8,
            'valor_cuota_11': self.valor_cuota_11,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def calcular_valor_cuota(valor_prima: int, tasa_mensual: float, num_cuotas: int) -> int:
        """
        Calculate installment value using constant amortization formula.
        
        Formula: cuota = prima * ((tasa * (1 + tasa)^n) / ((1 + tasa)^n - 1))
        
        Args:
            valor_prima: Premium value as integer
            tasa_mensual: Monthly effective rate as decimal (e.g., 0.023 for 2.3%)
            num_cuotas: Number of installments
            
        Returns:
            Installment value rounded to nearest integer
        """
        if not valor_prima or valor_prima <= 0 or num_cuotas <= 0:
            return 0
        
        # For zero interest (3 installments), simple division
        if tasa_mensual <= 0:
            return round(valor_prima / num_cuotas)
        
        # Amortization formula
        factor = (1 + tasa_mensual) ** num_cuotas
        cuota = valor_prima * ((tasa_mensual * factor) / (factor - 1))
        return round(cuota)

    def validar_entrega_poliza(self, datos_entrega: dict) -> tuple[bool, Optional[str]]:
        """
        Validate policy delivery data before transitioning to VIGENTE state.
        
        Args:
            datos_entrega: Dictionary with delivery data fields
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # 1. Required field validations
        if not datos_entrega.get('aseguradora_seleccionada'):
            return False, "Debe seleccionar una aseguradora"
        
        # Validate range 1-5
        aseg_sel = datos_entrega.get('aseguradora_seleccionada')
        if aseg_sel < 1 or aseg_sel > 5:
            return False, "La aseguradora seleccionada debe estar entre 1 y 5"
        
        # Validate that the selected aseguradora has an ID
        aseg_id_attr = f'id_aseguradora_{aseg_sel}'
        if hasattr(self, aseg_id_attr):
            aseg_id = getattr(self, aseg_id_attr)
            if not aseg_id:
                return False, f"La opción {aseg_sel} no tiene aseguradora asignada"
        
        if not datos_entrega.get('numero_poliza_aseguradora'):
            return False, "Debe ingresar el número de póliza"
        
        if not datos_entrega.get('inicio_vigencia'):
            return False, "Debe ingresar la fecha de inicio de vigencia"
        
        if not datos_entrega.get('medio_pago'):
            return False, "Debe seleccionar medio de pago"
        
        # 2. Conditional validations for financing
        medio_pago = datos_entrega.get('medio_pago')
        if medio_pago == 'financiera':
            if not datos_entrega.get('financiacion_num_cuotas'):
                return False, "Debe especificar número de cuotas para financiera"
            
            num_cuotas = datos_entrega.get('financiacion_num_cuotas')
            if num_cuotas not in [3, 5, 8, 11]:
                return False, "Número de cuotas debe ser 3, 5, 8 o 11"
            
            if not datos_entrega.get('financiacion_fecha_primera_cuota'):
                return False, "Debe especificar fecha de primera cuota"
            
            # Validate that pre-calculated installment values exist
            valor_cuota_attr = f'valor_cuota_{num_cuotas}'
            if hasattr(self, valor_cuota_attr):
                valor_cuota = getattr(self, valor_cuota_attr)
                if not valor_cuota:
                    return False, f"Debe generar propuesta antes de entregar con financiación ({num_cuotas} cuotas)"
        
        # 3. Validate cuota_actual doesn't exceed num_cuotas (if provided)
        if datos_entrega.get('financiacion_cuota_actual') and datos_entrega.get('financiacion_num_cuotas'):
            if datos_entrega['financiacion_cuota_actual'] > datos_entrega['financiacion_num_cuotas']:
                return False, "Cuota actual no puede exceder número total de cuotas"
        
        return True, None

