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

