from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
 
engine = create_engine('sqlite:///BaseDatos.db', echo=False)
Base = declarative_base()
 
class Usuarios(Base):
    __tablename__ = 'usuario'
    # Atributos de la tabla
    id_usuario = Column(String, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    puesto = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    usuario = Column(String, nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    # Variables de enlace
    movimiento = relationship('Movimientos', back_populates = 'usuario')
   
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("rol IN ('Administrador', 'Empleado')", name='check_rol_valido'),
    )
 
class Categorias(Base):
    __tablename__ = 'categoria'
    # Atributos de la tabla
    id_categoria = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    producto = relationship('Productos', back_populates= 'categoria')
   
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
    def __repr__(self):
        return(f"Categorias(id_categoria={self.id_categoria}, nombre={self.nombre}, descripcion={self.descripcion}, ",
               f"estado={self.estado})")
 
class Productos(Base):
    __tablename__ = 'producto'
    # Atributos de la tabla
    id_producto = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    id_categoria = Column(String, ForeignKey('categoria.id_categoria'), nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    movimiento = relationship('Movimientos', back_populates = 'producto')
    categoria = relationship('Categorias', back_populates= 'producto')
    inventario = relationship('Inventarios', back_populates= 'producto')
 
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
class Inventarios(Base):
    __tablename__ = 'inventario'
    # Atributos de la tabla
    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(String, ForeignKey('producto.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    cantidad_min = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    producto = relationship('Productos', back_populates= 'inventario')
 
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
class Movimientos(Base):
    __tablename__ = 'movimiento'
    # Atributos de la tabla
    id_movimiento = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(String, ForeignKey('usuario.id_usuario'), nullable=False)
    id_producto = Column(String, ForeignKey('producto.id_producto'), nullable=False)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    impuesto = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    usuario = relationship("Usuarios", back_populates= "movimiento")
    producto = relationship("Productos", back_populates= "movimiento")
    venta = relationship("Ventas", back_populates= "movimiento")
    compra = relationship("Compras", back_populates= "movimiento")
 
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
class Clientes(Base):
    __tablename__ = 'cliente'
    # Atributos de la tabla
    id_cliente = Column(String, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    email = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    venta = relationship("Ventas", back_populates= "cliente")
 
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
class Proveedores(Base):
    __tablename__ = 'proveedor'
    # Atributos de la tabla
    id_proveedor = Column(String, primary_key=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    email = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    # Variables de enlace
    compra = relationship("Compras", back_populates= "proveedor")
 
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
    )
 
class Ventas(Base):
    __tablename__ = 'venta'
    # Atributos de la tabla
    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey('movimiento.id_movimiento'), nullable=False)
    id_cliente = Column(String, ForeignKey('cliente.id_cliente'), nullable=False)
    # Variables de enlace
    movimiento = relationship("Movimientos", back_populates= "venta")
    cliente = relationship("Clientes", back_populates= "venta")
 
class Compras(Base):
    __tablename__ = 'compra'
    # Atributos de la tabla
    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey('movimiento.id_movimiento'), nullable=False)
    id_proveedor = Column(String, ForeignKey('proveedor.id_proveedor'), nullable=False)
    # Variables de enlace
    movimiento = relationship("Movimientos", back_populates= "compra")
    proveedor = relationship("Proveedores", back_populates= "compra")
 
 
# Crear las tablas si no existen
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
session = SessionLocal()
 
 
usuario1 = Usuarios(id_usuario="USER_01", nombres="Arturo", apellidos="Cameras", rol="Administrador", puesto="Gerente",
                   telefono="555-1234", salario=5000.0, usuario="arturocameras", contraseña="admin123")
usuario2 = Usuarios(id_usuario="USER_02", nombres="Ana", apellidos="López", rol="Administrador", puesto="Supervisor",
                   telefono="555-5678", salario=4500.0, usuario="analopez", contraseña="admin456")
usuario3 = Usuarios(id_usuario="USER_03", nombres="Carlos", apellidos="Gómez", rol="Empleado", puesto="Vendedor",
                   telefono="555-9101", salario=3000.0, usuario="carlosgomez", contraseña="emp123")
usuario4 = Usuarios(id_usuario="USER_04", nombres="Laura", apellidos="Martínez", rol="Empleado", puesto="Vendedora",
                   telefono="555-1122", salario=3200.0, usuario="lauramartinez", contraseña="emp456")
 
session.add(usuario1)
session.add(usuario2)
session.add(usuario3)
session.add(usuario4)
 
session.commit()
session.close()
 