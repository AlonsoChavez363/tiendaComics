from sqlalchemy import Column, Integer, String, ForeignKey, TEXT, Enum, DateTime
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

# ENUM para el estado del pedido
class EstadoPedidoEnum(str, enum.Enum):
    pendiente = "pendiente"
    recibido = "recibido"
    cancelado = "cancelado"

# MODELOS

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)
    id_tipo_usuario = Column(Integer, ForeignKey("tipo_usuario.id_tipo_usuario"), nullable=True)
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")
    clientes = relationship("Cliente", back_populates="usuario")

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"

    id_tipo_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuarios = relationship("Usuario", back_populates="tipo_usuario")

class Productos(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(TEXT, nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    categorias = relationship("Categorias", back_populates="productos")

class Categorias(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  
    descripcion = Column(TEXT, nullable=False)   
    productos = relationship("Productos", back_populates="categorias")

class Proveedores(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    contacto = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(150), nullable=False)

    pedidos = relationship("PedidosProveedor", back_populates="proveedor")

class PedidosProveedor(Base):
    __tablename__ = "pedidos_provedor"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    fecha_compra = Column(DateTime, default=datetime.utcnow)
    estado = Column(Enum(EstadoPedidoEnum), default=EstadoPedidoEnum.pendiente)

    proveedor = relationship("Proveedores", back_populates="pedidos")

class Detalles_compra(Base):
    __tablename__ = "detalle_compra"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    id_clientes = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=True)

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(100), nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="clientes")
