from sqlalchemy import Column, Integer, String, ForeignKey
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