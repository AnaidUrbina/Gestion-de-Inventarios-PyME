-- Insertar datos en la tabla usuario
INSERT INTO usuario (id_usuario, nombres, apellidos, rol, puesto, telefono, salario, usuario, contrasena) VALUES
('USER_01', 'Arturo', 'Cameras', 'Administrador', 'Gerente', '555-1234', 5000.0, 'arturocameras', 'admin123'),
('USER_02', 'Ana', 'López', 'Administrador', 'Supervisor', '555-5678', 4500.0, 'analopez', 'admin456'),
('USER_03', 'Carlos', 'Gómez', 'Empleado', 'Vendedor', '555-9101', 3000.0, 'carlosgomez', 'emp123'),
('USER_04', 'Laura', 'Martínez', 'Empleado', 'Vendedora', '555-1122', 3200.0, 'lauramartinez', 'emp456'),
('USER_05', 'Pedro', 'Gómez', 'Cliente', 'N/A', '555-2345', 0.0, 'pedrogomez', 'cliente123'),
('USER_06', 'María', 'Fernández', 'Cliente', 'N/A', '555-6789', 0.0, 'mariafernandez', 'cliente456'),
('USER_07', 'Juan', 'Pérez', 'Cliente', 'N/A', '555-7890', 0.0, 'juanperez', 'cliente789');

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
('CLI_01', 'Juan', 'Pérez', '555-7890', 'Calle 123', 'juanperez@email.com', 'Activo'),
('CLI_02', 'Pedro', 'Gómez', '555-2345', 'Avenida 456', 'pedrogomez@email.com', 'Activo'),
('CLI_03', 'María', 'Fernández', '555-6789', 'Calle 789', 'mariafernandez@email.com', 'Activo');
-- Insertar datos en la tabla proveedor
INSERT INTO proveedor (id_proveedor, nombres, apellidos, telefono, direccion, email, empresa, estado) VALUES
('PROV_01', 'Pedro', 'Ramírez', '555-6543', 'Avenida Central', 'pedroramirez@email.com', 'Juguetes S.A.', 'Activo');

-- Insertar datos en la tabla movimiento
INSERT INTO movimiento (id_usuario, id_producto, descripcion, cantidad, subtotal, impuesto, total, fecha, tipo, estado) VALUES
('USER_03', 'PROD_01', 'Venta de figura de acción', 2, 51.98, 8.32, 60.30, CURRENT_DATE, 'Venta', 'Activo');

-- Insertar datos en la tabla venta
INSERT INTO venta (id_movimiento, id_cliente) VALUES
(1, 'CLI_01');