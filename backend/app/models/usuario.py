"""Usuario (User) domain model."""
from datetime import datetime
from app.models import db


class Usuario(db.Model):
    """
    Represents a user entity in the system.
    
    Supports two types of users:
    - PERSONA: Individual/natural person
    - EMPRESA: Company/legal entity
    
    User roles (tipo_usuario):
    - CLIENTE: Client user
    - AGENTE: Agent user  
    - ADMINISTRADOR: Administrator
    - SUPERADMIN: Super administrator
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_persona = db.Column(db.String(10), nullable=False)  # 'PERSONA' o 'EMPRESA'
    
    # =========================================================================
    # CAMPOS COMUNES Y DE LOGIN
    # =========================================================================
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono_movil = db.Column(db.String(20))
    correo = db.Column(db.String(100), unique=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    clave = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(15), nullable=False)  # 'AGENTE', 'CLIENTE', 'ADMINISTRADOR', 'SUPERADMIN'
    
    # =========================================================================
    # CAMPOS PARA PERSONA NATURAL (NULL si es empresa)
    # =========================================================================
    tipo_documento = db.Column(db.String(10))
    numero_documento = db.Column(db.String(20))
    nombre = db.Column(db.String(150))
    edad = db.Column(db.Integer)
    
    # =========================================================================
    # CAMPOS PARA EMPRESA (NULL si es persona)
    # =========================================================================
    nit = db.Column(db.String(20))
    razon_social = db.Column(db.String(255))
    nombre_rep_legal = db.Column(db.String(150))
    documento_rep_legal = db.Column(db.String(20))
    telefono_rep_legal = db.Column(db.String(20))
    correo_rep_legal = db.Column(db.String(100))
    contacto_alternativo = db.Column(db.String(255))
    
    # =========================================================================
    # TIMESTAMPS
    # =========================================================================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert model instance to dictionary representation."""
        base_dict = {
            'id': self.id,
            'tipo_persona': self.tipo_persona,
            # Campos comunes
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono_movil': self.telefono_movil,
            'correo': self.correo,
            'usuario': self.usuario,
            'tipo_usuario': self.tipo_usuario,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Campos para persona natural
        if self.tipo_persona == 'PERSONA':
            base_dict.update({
                'tipo_documento': self.tipo_documento,
                'numero_documento': self.numero_documento,
                'nombre': self.nombre,
                'edad': self.edad,
            })
        
        # Campos para empresa
        if self.tipo_persona == 'EMPRESA':
            base_dict.update({
                'nit': self.nit,
                'razon_social': self.razon_social,
                'nombre_rep_legal': self.nombre_rep_legal,
                'documento_rep_legal': self.documento_rep_legal,
                'telefono_rep_legal': self.telefono_rep_legal,
                'correo_rep_legal': self.correo_rep_legal,
                'contacto_alternativo': self.contacto_alternativo,
            })
        
        return base_dict

    def to_dict_full(self) -> dict:
        """Convert model instance to full dictionary (all fields)."""
        return {
            'id': self.id,
            'tipo_persona': self.tipo_persona,
            # Campos comunes
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono_movil': self.telefono_movil,
            'correo': self.correo,
            'usuario': self.usuario,
            'tipo_usuario': self.tipo_usuario,
            # Campos persona natural
            'tipo_documento': self.tipo_documento,
            'numero_documento': self.numero_documento,
            'nombre': self.nombre,
            'edad': self.edad,
            # Campos empresa
            'nit': self.nit,
            'razon_social': self.razon_social,
            'nombre_rep_legal': self.nombre_rep_legal,
            'documento_rep_legal': self.documento_rep_legal,
            'telefono_rep_legal': self.telefono_rep_legal,
            'correo_rep_legal': self.correo_rep_legal,
            'contacto_alternativo': self.contacto_alternativo,
            # Timestamps
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        display_name = self.nombre if self.tipo_persona == 'PERSONA' else self.razon_social
        return f'<Usuario {self.id}: {self.usuario} ({display_name})>'
