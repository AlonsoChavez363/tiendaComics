from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)
    id_tipo_usuario = Column(Integer, ForeignKey("tipo_usuario.id_tipo_usuario"), nullable=True)
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")

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
    precio = Column(DECIMAL(10, 2), nullable=False)  # Cambié 'nullblade' por 'nullable'
    categorias = relationship("Categorias", back_populates="productos")

class Categorias(Base):
    __tablename__ = "categorias"
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  
    descripcion = Column(TEXT, nullable=False)   
    productos = relationship("Productos", back_populates="categorias")
