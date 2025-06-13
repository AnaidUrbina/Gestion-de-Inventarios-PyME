from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import DateTime
import datetime
from passlib.hash import bcrypt

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
    estado = Column(String, nullable=False)
    usuario = Column(String, nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    # Variables de enlace
    movimiento = relationship('Movimientos', back_populates = 'usuario')
    
    # Especificacion en atributos
    __table_args__ = (
        CheckConstraint("rol IN ('Administrador', 'Empleado')", name='check_rol_valido'),
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name='check_estado_valido'),
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
    compra = relationship("Compras", back_populates= "movimiento", uselist=False)
    venta = relationship("Ventas", back_populates="movimiento", uselist=False)


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
    usuario = Column(String, nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    # Variables de enlace
    ventas = relationship("Ventas", back_populates="cliente")

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
    cliente = relationship("Clientes", back_populates="ventas")

class Compras(Base):
    __tablename__ = 'compra'
    # Atributos de la tabla
    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey('movimiento.id_movimiento'), nullable=False)
    id_proveedor = Column(String, ForeignKey('proveedor.id_proveedor'), nullable=False)
    # Variables de enlace
    movimiento = relationship("Movimientos", back_populates= "compra")
    proveedor = relationship("Proveedores", back_populates= "compra")

class Auditorias(Base):
    __tablename__ = 'auditoria'

    id_auditoria = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(String, ForeignKey('usuario.id_usuario'), nullable=False)
    entidad = Column(String, nullable=False)  # Ej: 'Producto', 'Categoria'
    operacion = Column(String, nullable=False)  # Ej: 'Modificación', 'Eliminación', 'Creación'
    descripcion = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.now)
    
    usuario = relationship("Usuarios")


# Crear las tablas si no existen
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


session = SessionLocal()

# Insertar usuarios y clientes dentro de una misma sesión (con contraseña cifrada)
usuarios_data = [
    {"id_usuario": "USER_001", "nombres": "Itzel Anaid", "apellidos": "Cerón Urbina", "rol": "Administrador", "puesto": "Gerente", 
     "telefono": "5512345678", "salario": 5000.0,"estado":"Activo", "usuario": "itzelceron", "contraseña": "admin123"},
    {"id_usuario": "USER_002", "nombres": "Ernesto", "apellidos": "Rojas Pérez", "rol": "Administrador", "puesto": "Supervisor", 
     "telefono": "5536925814", "salario": 4500.0,"estado":"Activo", "usuario": "ernestorojas", "contraseña": "admin456"},
    {"id_usuario": "USER_003", "nombres": "Eduardo Arturo", "apellidos": "Campillo Lopez", "rol": "Empleado", "puesto": "Vendedor", 
     "telefono": "5514785236", "salario": 3000.0,"estado":"Activo", "usuario": "eduardocampillo", "contraseña": "emp123"},
    {"id_usuario": "USER_004", "nombres": "Paola Carolina", "apellidos": "González Pérez", "rol": "Empleado", "puesto": "Vendedora", 
     "telefono": "5578945612", "salario": 3200.0,"estado":"Activo", "usuario": "paolagonzalez", "contraseña": "emp456"},
]

nuevos_clientes = [
    Clientes(
        id_cliente="CLI_001",
        nombres="Público",
        apellidos="En General",
        telefono="0000000000",
        direccion="Sin dirección",
        email="publico.general@example.com",
        estado="Activo",
        usuario="publico_general",
        contraseña=bcrypt.hash("publico123")
    ),
    Clientes(
        id_cliente="CLI_002",
        nombres="Luis Alberto",
        apellidos="Ramírez Pérez",
        telefono="5598745632",
        direccion="Calle Falsa 123, Ciudad de México",
        email="luis.ramirez@example.com",
        estado="Activo",
        usuario="luiscliente",
        contraseña=bcrypt.hash("cli123")
    )
]
# Usar una sola sesión para todo
with SessionLocal() as session:
    # Insertar usuarios si no existen
    for data in usuarios_data:
        existente = session.query(Usuarios).filter_by(usuario=data["usuario"]).first()
        if not existente:
            data["contraseña"] = bcrypt.hash(data["contraseña"])  # <-- Aquí ciframos antes de guardar
            session.add(Usuarios(**data))
    # Insertar clientes si no existen
    for cliente in nuevos_clientes:
        existente = session.query(Clientes).filter_by(usuario=cliente.usuario).first()
        if not existente:
            session.add(cliente)
# Confirmar todos los cambios
    session.commit()
