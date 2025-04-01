import mysql.connector
from rich.console import Console 
from rich.prompt import Prompt

# Configurar conexión a la BD
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Cambia por tu usuario de MySQL
            password="It38122961",  # Cambia por tu contraseña de MySQL
            database="Inventario"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Verificar credenciales de usuario
def verificar_credenciales(usuario, password, tipo_usuario):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        consulta = "SELECT * FROM usuario WHERE usuario = %s AND contrasena = %s AND rol = %s"
        cursor.execute(consulta, (usuario, password, tipo_usuario))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado is not None
    return False

# Inicializar consola con Rich
console = Console()

# Menú principal
def menu_principal():
    console.print("[bold purple]Bienvenido al Sistema[/bold purple]")
    console.print("[green]1.[/] Administrador")
    console.print("[green]2.[/] Empleado")
    console.print("[green]3.[/] Salir")

    rol = Prompt.ask("Seleccione la opción deseada")
    
    if rol in ["1", "2"]:
        usuario = Prompt.ask("Ingrese su usuario")
        password = Prompt.ask("Ingrese su contraseña", password=True)
        
        tipo_usuario = "Administrador" if rol == "1" else "Empleado"

        if verificar_credenciales(usuario, password, tipo_usuario):
            if rol == "1":
                menu_administrador()
            elif rol == "2":
                menu_empleado()
        else:
            console.print("[red]Usuario o contraseña incorrectos[/red]")
    elif rol == "3":
        console.print("[yellow]Saliendo del sistema...[/yellow]")
    else:
        console.print("[red]Opción inválida[/red]")

# Menú del Administrador
def menu_administrador():
    while True:
        console.print("\n[bold cyan]Menú Administrador[/bold cyan]")
        console.print("1. Ver inventario")
        console.print("2. Agregar producto")
        console.print("3. Salir")
        
        opcion = Prompt.ask("Seleccione una opción")
        
        if opcion == "1":
            ver_inventario()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            break
        else:
            console.print("[red]Opción inválida[/red]")

# Función para ver inventario desde la BD
def ver_inventario():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        consulta = """
            SELECT p.id_producto, p.nombre, i.cantidad, p.precio_unitario
            FROM producto p
            JOIN inventario i ON p.id_producto = i.id_producto
        """
        cursor.execute(consulta)
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        console.print("\n[bold magenta]Inventario[/bold magenta]")
        for producto in productos:
            console.print(f"[green]ID:[/] {producto[0]}, [yellow]Nombre:[/] {producto[1]}, [blue]Stock:[/] {producto[2]}, [red]Precio:[/] ${producto[3]}")

# Función para agregar un producto a la BD
def agregar_producto():
    conexion = conectar_bd()
    if conexion:
        nombre = Prompt.ask("Ingrese el nombre del producto")
        descripcion = Prompt.ask("Ingrese la descripción")
        precio = Prompt.ask("Ingrese el precio del producto")
        id_categoria = Prompt.ask("Ingrese el ID de la categoría")
        estado = "Activo"

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO producto (id_producto, nombre, descripcion, precio_unitario, id_categoria, estado) VALUES (UUID(), %s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, id_categoria, estado))
        
        id_producto = cursor.lastrowid  # Obtener el ID del producto recién insertado
        
        cantidad = Prompt.ask("Ingrese la cantidad inicial", default="0")
        cantidad_min = Prompt.ask("Ingrese la cantidad mínima")
        
        cursor.execute("INSERT INTO inventario (id_producto, cantidad, cantidad_min, estado) VALUES (%s, %s, %s, 'Activo')",
                       (id_producto, cantidad, cantidad_min))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        console.print("[green]Producto agregado correctamente[/green]")

# Menú del empleado (por desarrollar)
def menu_empleado():
    console.print("[yellow]Función en desarrollo...[/yellow]")

# Ejecutar el menú principal
menu_principal()