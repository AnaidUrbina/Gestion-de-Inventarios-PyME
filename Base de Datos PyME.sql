CREATE DATABASE IF NOT EXISTS Inventario;
USE Inventario;

CREATE TABLE usuario (
    id_usuario VARCHAR(50) PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Empleado') NOT NULL,
    puesto VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    salario FLOAT NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL
);

CREATE TABLE categoria (
    id_categoria VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL
);

CREATE TABLE producto (
    id_producto VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio_unitario FLOAT NOT NULL,
    id_categoria VARCHAR(50) NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    id_producto VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL,
    cantidad_min INT NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE cliente (
    id_cliente VARCHAR(50) PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT NOT NULL,
    email VARCHAR(100) NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL
);

CREATE TABLE proveedor (
    id_proveedor VARCHAR(50) PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT NOT NULL,
    email VARCHAR(100) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL
);

CREATE TABLE movimiento (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario VARCHAR(50) NOT NULL,
    id_producto VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    cantidad INT NOT NULL,
    subtotal FLOAT NOT NULL,
    impuesto FLOAT NOT NULL,
    total FLOAT NOT NULL,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    tipo VARCHAR(50) NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_movimiento INT NOT NULL,
    id_cliente VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_movimiento) REFERENCES movimiento(id_movimiento),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE compra (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_movimiento INT NOT NULL,
    id_proveedor VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_movimiento) REFERENCES movimiento(id_movimiento),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);

-- Insertar datos en la tabla usuario
INSERT INTO usuario (id_usuario, nombres, apellidos, rol, puesto, telefono, salario, usuario, contrasena) VALUES
('USER_01', 'Arturo', 'Cameras', 'Administrador', 'Gerente', '555-1234', 5000.0, 'arturocameras', 'admin123'),
('USER_02', 'Ana', 'López', 'Administrador', 'Supervisor', '555-5678', 4500.0, 'analopez', 'admin456'),
('USER_03', 'Carlos', 'Gómez', 'Empleado', 'Vendedor', '555-9101', 3000.0, 'carlosgomez', 'emp123'),
('USER_04', 'Laura', 'Martínez', 'Empleado', 'Vendedora', '555-1122', 3200.0, 'lauramartinez', 'emp456');

-- Insertar datos en la tabla categoria
INSERT INTO categoria (id_categoria, nombre, descripcion, estado) VALUES
('CAT_01', 'Figuras de acción', 'Figuras coleccionables de personajes', 'Activo'),
('CAT_02', 'Juegos de mesa', 'Juegos de mesa familiares', 'Activo');

-- Insertar datos en la tabla producto
INSERT INTO producto (id_producto, nombre, descripcion, precio_unitario, id_categoria, estado) VALUES
('PROD_01', 'Batman Figura', 'Figura de acción de Batman', 25.99, 'CAT_01', 'Activo'),
('PROD_02', 'Monopoly', 'Juego de mesa Monopoly clásico', 19.99, 'CAT_02', 'Activo');

-- Insertar datos en la tabla inventario
INSERT INTO inventario (id_producto, cantidad, cantidad_min, estado) VALUES
('PROD_01', 50, 5, 'Activo'),
('PROD_02', 30, 3, 'Activo');

-- Insertar datos en la tabla cliente
INSERT INTO cliente (id_cliente, nombres, apellidos, telefono, direccion, email, estado) VALUES
('CLI_01', 'Juan', 'Pérez', '555-7890', 'Calle 123', 'juanperez@email.com', 'Activo');

-- Insertar datos en la tabla proveedor
INSERT INTO proveedor (id_proveedor, nombres, apellidos, telefono, direccion, email, empresa, estado) VALUES
('PROV_01', 'Pedro', 'Ramírez', '555-6543', 'Avenida Central', 'pedroramirez@email.com', 'Juguetes S.A.', 'Activo');

-- Insertar datos en la tabla movimiento
INSERT INTO movimiento (id_usuario, id_producto, descripcion, cantidad, subtotal, impuesto, total, fecha, tipo, estado) VALUES
('USER_03', 'PROD_01', 'Venta de figura de acción', 2, 51.98, 8.32, 60.30, CURRENT_DATE, 'Venta', 'Activo');

-- Insertar datos en la tabla venta
INSERT INTO venta (id_movimiento, id_cliente) VALUES
(1, 'CLI_01');