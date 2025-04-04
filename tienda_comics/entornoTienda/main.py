from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import models
from database import SessionLocal, engine
from pydantic import BaseModel
from typing import Optional


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

##################################################Productos###################################################################

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    id_categoria: Optional[int] = None
    precio: float

# Endpoint para obtener todos los productos
@app.get("/productos", tags=["Operaciones Productos"])
def leer_productos(db: Session = Depends(get_db)):
    productos = db.query(models.Productos).all()
    return JSONResponse(content=jsonable_encoder(productos))


#Endpoint para buscar un producto por ID
@app.get("/producto/buscar/{nombre}", tags=["Operaciones Productos"])
def buscar_producto(nombre: str, db: Session = Depends(get_db)):
    producto = db.query(models.Productos).filter(models.Productos.nombre == nombre).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return JSONResponse(content=jsonable_encoder(producto))


@app.post("/productos/agregar", tags=["Operaciones Productos"])
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):

    nuevo_producto = models.Productos(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        id_categoria=producto.id_categoria,
        precio=producto.precio  # Se incluye el precio
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return JSONResponse(content=jsonable_encoder(nuevo_producto))


#Endpoint para eliminar un producto
@app.delete("/productos/borrar/{id_producto}", tags=["Operaciones Productos"])
def eliminar_producto(id_producto: int, db: Session = Depends(get_db)):
    producto = db.query(models.Productos).filter(models.Productos.id_producto == id_producto).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return JSONResponse(content={"message": "Producto eliminado correctamente"})


#Endpoint para actualizar un producto
@app.put("/productos/actualizar/{id_producto}", tags=["Operaciones Productos"])
def actualizar_producto(id_producto: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    # Buscar el producto por ID
    producto_existente = db.query(models.Productos).filter(models.Productos.id_producto == id_producto).first()

    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Actualizar el producto con los nuevos valores
    producto_existente.nombre = producto.nombre
    producto_existente.descripcion = producto.descripcion
    producto_existente.id_categoria = producto.id_categoria
    producto_existente.precio = producto.precio  # Actualizar el precio

    db.commit()
    db.refresh(producto_existente)

    return JSONResponse(content=jsonable_encoder(producto_existente))

################################################Proveedores##################################################################
from pydantic import BaseModel

class ProveedorCreate(BaseModel):
    nombre: str
    contacto: str
    telefono: str
    correo: str

#Endpoint para ver todos los proveedores registrados
@app.get("/proveedores", tags=["Operaciones Proveedores"])
def leer_proveedores(db: Session = Depends(get_db)):
    proveedores = db.query(models.Proveedores).all()
    return JSONResponse(content=jsonable_encoder(proveedores))

#Endpoint para buscar proveedore por nombre
@app.get("/proveedor/buscar/{nombre}", tags=["Operaciones Proveedores"])
def buscar_proveedor(nombre: str, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedores).filter(models.Proveedores.nombre == nombre).first()

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return JSONResponse(content=jsonable_encoder(proveedor))

#Endpoint para agregar un proveedor
@app.post("/proveedores/agregar", tags=["Operaciones Proveedores"])
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    nuevo_proveedor = models.Proveedores(
        nombre=proveedor.nombre,
        contacto=proveedor.contacto,
        telefono=proveedor.telefono,
        correo=proveedor.correo
    )

    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)

    return JSONResponse(content=jsonable_encoder(nuevo_proveedor))

#Endpoint para borrar un proveedor
@app.delete("/proveedores/borrar/{id_proveedor}", tags=["Operaciones Proveedores"])
def eliminar_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedores).filter(models.Proveedores.id_proveedor == id_proveedor).first()

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    db.delete(proveedor)
    db.commit()

    return JSONResponse(content={"message": "Proveedor eliminado correctamente"})

#Endpoint para actualizar un proveedor
@app.put("/proveedores/actualizar/{id_proveedor}", tags=["Operaciones Proveedores"])
def actualizar_proveedor(id_proveedor: int, proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    proveedor_existente = db.query(models.Proveedores).filter(models.Proveedores.id_proveedor == id_proveedor).first()

    if not proveedor_existente:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    proveedor_existente.nombre = proveedor.nombre
    proveedor_existente.contacto = proveedor.contacto
    proveedor_existente.telefono = proveedor.telefono
    proveedor_existente.correo = proveedor.correo

    db.commit()
    db.refresh(proveedor_existente)

    return JSONResponse(content=jsonable_encoder(proveedor_existente))

