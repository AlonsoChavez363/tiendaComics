from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import models
from database import SessionLocal, engine
from pydantic import BaseModel


# Crear las tablas en la base de datos (Si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    contraseña: str
    id_tipo_usuario: int | None = None

#Obtener todos los usuarios
@app.get("/usuarios", tags=["Operaciones Usuario"])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

#Buscar usuario por ID
@app.get('/usuario/buscar/{id_usuario}', tags=["Operaciones Usuario"])
def buscar_uno(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return JSONResponse(content=jsonable_encoder(usuario))

#Ingresar un nuevo usuario
@app.post("/usuarios/agregar", tags=["Operaciones Usuario"])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=usuario.contraseña,  
        id_tipo_usuario=usuario.id_tipo_usuario
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return JSONResponse(content=jsonable_encoder(nuevo_usuario))


#Endpoint borrar un usuario
@app.delete("/usuarios/borrar/{id_usuario}", tags=["Operaciones Usuario"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    
    return JSONResponse(content={"message": "Usuario eliminado correctamente"})

#Endpoint para editar un usuario
@app.put("/usuarios/actualizar/{id_usuario}", tags=["Operaciones Usuario"])
def actualizar_usuario(id_usuario: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Buscar el usuario por ID
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()

    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if usuario.correo != usuario_existente.correo:
        usuario_correo_existente = db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
        if usuario_correo_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

    usuario_existente.nombre = usuario.nombre
    usuario_existente.correo = usuario.correo
    usuario_existente.contraseña = usuario.contraseña
    usuario_existente.id_tipo_usuario = usuario.id_tipo_usuario

    db.commit()
    db.refresh(usuario_existente)

    return JSONResponse(content=jsonable_encoder(usuario_existente))