from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_V3_1 import Categorias, Productos, Proveedores, Inventarios  # Importa el modelo de tu tabla Categorías

# Conexión a la base de datos
DATABASE_URL = "sqlite:///BaseDatos.db"  # Cambia esta línea según tu base de datos
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Insertar categorías
categorias = [
    Categorias(id_categoria="CAT_001", nombre="Juguetes Educativos", descripcion="Juguetes que fomentan el aprendizaje", estado="Activo"),
    Categorias(id_categoria="CAT_002", nombre="Muñecas y Peluches", descripcion="Muñecas, peluches y figuras de acción", estado="Activo"),
    Categorias(id_categoria="CAT_003", nombre="Juguetes de Construcción", descripcion="Bloques, piezas y sets de construcción", estado="Activo"),
    Categorias(id_categoria="CAT_004", nombre="Juguetes de Exterior", descripcion="Juguetes para actividades al aire libre", estado="Activo"),
    Categorias(id_categoria="CAT_005", nombre="Juguetes Electrónicos", descripcion="Juguetes con componentes electrónicos", estado="Activo")
]

# Añadir categorías a la sesión
session.add_all(categorias)
session.commit()

print("Categorías insertadas correctamente.")

#Insertar Proveedores
proveedores = [
    Proveedores(id_proveedor="PROV_001", nombres="Juan", apellidos="Pérez", telefono="123-456-7890", direccion="123 Calle Ficticia", email="contacto@toycompany.com", empresa="Toy Company", estado="Activo"),
    Proveedores(id_proveedor="PROV_002", nombres="Ana", apellidos="Gómez", telefono="234-567-8901", direccion="456 Avenida Principal", email="contacto@supertys.com", empresa="Super Toys", estado="Activo"),
    Proveedores(id_proveedor="PROV_003", nombres="Carlos", apellidos="Méndez", telefono="345-678-9012", direccion="789 Calle Real", email="contacto@playworld.com", empresa="PlayWorld", estado="Activo"),
    Proveedores(id_proveedor="PROV_004", nombres="Luisa", apellidos="Fernández", telefono="456-789-0123", direccion="101 Calle Creativa", email="contacto@funfactory.com", empresa="FunFactory", estado="Activo"),
    Proveedores(id_proveedor="PROV_005", nombres="Pedro", apellidos="Sánchez", telefono="567-890-1234", direccion="202 Calle Juguetona", email="contacto@xtremejuguetes.com", empresa="Juguetes Xtreme", estado="Activo")
]

# Añadir proveedores a la sesión
session.add_all(proveedores)
session.commit()

print("Proveedores insertados correctamente.")

# Insertar productos
productos = [
    Productos(id_producto="PROD_001", nombre="Set de bloques", descripcion="Juego de bloques para construir", precio_unitario=19.99, id_categoria="CAT_003", estado="Activo"),
    Productos(id_producto="PROD_002", nombre="Muñeca de peluche", descripcion="Muñeca de peluche suave", precio_unitario=14.99, id_categoria="CAT_002", estado="Activo"),
    Productos(id_producto="PROD_003", nombre="Juego de aprendizaje", descripcion="Juego de mesa educativo", precio_unitario=24.99, id_categoria="CAT_001", estado="Activo"),
    Productos(id_producto="PROD_004", nombre="Bicicleta para niños", descripcion="Bicicleta de 12 pulgadas", precio_unitario=79.99, id_categoria="CAT_004", estado="Activo"),
    Productos(id_producto="PROD_005", nombre="Robot interactivo", descripcion="Robot programable para niños", precio_unitario=49.99, id_categoria="CAT_005", estado="Activo")
]
inventarios = [
    Inventarios(id_producto="PROD_001", cantidad=50, cantidad_min=10, estado="Activo"),
    Inventarios(id_producto="PROD_002", cantidad=30, cantidad_min=5, estado="Activo"),
    Inventarios(id_producto="PROD_003", cantidad=40, cantidad_min=8, estado="Activo"),
    Inventarios(id_producto="PROD_004", cantidad=15, cantidad_min=3, estado="Activo"),
    Inventarios(id_producto="PROD_005", cantidad=20, cantidad_min=4, estado="Activo"),
]

session.add_all(inventarios)
session.commit()

# Añadir productos a la sesión
session.add_all(productos)
session.commit()

print("Productos insertados correctamente.")
session.close()
