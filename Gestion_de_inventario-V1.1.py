import mysql.connector
import re
from rich.console import Console 
from rich.prompt import Prompt


# Inicializar consola con Rich
console = Console()

#Conexion con la base de datos
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
        console.print(f"[red]Error: {err}[/red]")
        return None
#Autenticacion de usuarios y contraseñas
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
#Menu principal (Falta funcion de cambio de contraseña)
def menu_principal():
    while True:
        console.print("[bold purple]Bienvenido al Sistema[/bold purple]")
        console.print("[green]1.[/] Administrador")
        console.print("[green]2.[/] Empleado")
        console.print("[green]3.[/] Cliente")
        console.print("[green]4.[/] Cambiar contraseña Empleado")
        console.print("[green]5.[/] Salir")
        
        rol = Prompt.ask("Seleccione la opción deseada")
        
        if rol in ["1", "2", "3"]:
            usuario = Prompt.ask("Ingrese su usuario")
            password = Prompt.ask("Ingrese su contraseña", password=True)
            
            tipo_usuario = "Administrador" if rol == "1" else "Empleado" if rol == "2" else "Cliente"
            
            if verificar_credenciales(usuario, password, tipo_usuario):
                if rol == "1":
                    menu_administrador()
                elif rol == "2":
                    menu_empleado()
                elif rol == "3":
                    menu_cliente()
            else:
                console.print("[red]Usuario o contraseña incorrectos[/red]")
        elif rol == "4":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif rol == "5":
            console.print("[yellow]Saliendo del sistema...[/yellow]")
            break
        else:
            console.print("[red]Opción inválida[/red]")
#Menu admin (Faltan consultas)
def menu_administrador():
    while True:
        console.print("\n[bold cyan]Menú Administrador[/bold cyan]")
        console.print("1. Comprar")
        console.print("2. Ver alertas de productos")
        console.print("3. Modificación de productos")
        console.print("4. Ver inventario")
        console.print("5. Ver reporte de ventas")
        console.print("6. Ver reportes de compras")
        console.print("7. Ver movimientos")
        console.print("8. Administrar Empleados")
        console.print("9. Salir")
        
        opcion = Prompt.ask("Seleccione una opción")
        
        if opcion == "3":
            modificacion_productos()
        elif opcion == "4":
            ver_inventario()
        elif opcion == "8":
            modificacion_empleados()
        elif opcion == "9":
            break
        else:
            console.print("[yellow]Función en desarrollo...[/yellow]")
#Ver inventario
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
#Modificar productos (agregar, eliminar, modificar)
def modificacion_productos():
    while True:
        console.print("\n[bold magenta]Modificación de Productos[/bold magenta]")
        console.print("1. Agregar producto")
        console.print("2. Eliminar producto")
        console.print("3. Modificar precio")
        console.print("4. Volver")
        
        opcion = Prompt.ask("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_producto()
        elif opcion in ["2", "3"]:
            respuesta = Prompt.ask("¿Está seguro de realizar esta operación?", choices=["si", "no"])
            if respuesta.lower() == "si":
                console.print("[green]Operación realizada con éxito[/green]")
            else:
                console.print("[red]Operación cancelada[/red]")
        elif opcion == "4":
            break
        else:
            console.print("[red]Opción inválida[/red]")
#Genera un id para los productos (se puede modificar para que genere otros id´s)
def generar_nuevo_id_producto(cursor):
    cursor.execute("SELECT id_producto FROM producto ORDER BY id_producto DESC LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        ultimo_id = resultado[0]  # Ejemplo: 'PROD_02'
        numero_actual = int(re.search(r'\d+', ultimo_id).group())  # Extrae '02' y lo convierte en entero
        nuevo_id = f"PROD_{numero_actual + 1:02d}"  # Genera 'PROD_03' si el último era 'PROD_02'
    else:
        nuevo_id = "PROD_01"  # Si no hay productos, empezamos desde PROD_01

    return nuevo_id
#Agrega productos y tiene la pregunta de autorizacion
def agregar_producto():
    conexion = conectar_bd()
    
    if conexion:
        cursor = conexion.cursor()

        # Generar el nuevo ID para el producto
        id_producto = generar_nuevo_id_producto(cursor)
    
        nombre = Prompt.ask("Ingrese el nombre del producto")
        descripcion = Prompt.ask("Ingrese la descripción")
        precio = Prompt.ask("Ingrese el precio del producto")
        id_categoria = Prompt.ask("Ingrese el ID de la categoría")
        estado = "Activo"
        
        cantidad = Prompt.ask("Ingrese la cantidad inicial", default="0")
        cantidad_min = Prompt.ask("Ingrese la cantidad mínima")
        
        respuesta = Prompt.ask("¿Está seguro de realizar esta operación?", choices=["si", "no"])
        if respuesta.lower() == "si":
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO producto (id_producto, nombre, descripcion, precio_unitario, id_categoria, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                       (id_producto, nombre, descripcion, precio, id_categoria, estado))
            
            
            cursor.execute("INSERT INTO inventario (id_producto, cantidad, cantidad_min, estado) VALUES (%s, %s, %s, 'Activo')",
                           (id_producto, cantidad, cantidad_min))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            console.print("[green]Operación realizada con éxito[/green]")
        else:
            console.print("[red]Operación cancelada[/red]")
#Menu de modificacion de empleados (En proceso)
def modificacion_empleados():
    while True:
        console.print("\n[bold]Administración de Empleados[/bold]", style="color(162)")
        console.print("1. Ver Empleados")
        console.print("2. Agregar Empleado")
        console.print("3. Eliminar Empleado")
        console.print("4. Modificar datos del Empleado")
        console.print("5. Volver")
        
        opcion = Prompt.ask("Seleccione una opción: ")
        
        if opcion == "1":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion in ["2", "3", "4"]:
            respuesta = Prompt.ask("¿Está seguro de realizar esta operación?", choices=["si", "no"])
            if respuesta.lower() == "si":
                console.print("[green]Operación realizada con éxito[/green]")
            else:
                console.print("[red]Operación cancelada[/red]")
        elif opcion == "5":
            break
        else:
            console.print("[red]Opción inválida[/red]")
#Menú de empleado (Faltan consultas y funciones)
def menu_empleado():
    while True:
        console.print("\n[bold cyan]Menú Empleado[/bold cyan]")
        console.print("1. Ventas")
        console.print("2. Ver reportes de ventas")
        console.print("3. Ver inventario")
        console.print("4. Salir")
        
        opcion = Prompt.ask("Seleccione una opción")
        
        if opcion == "3":
            ver_inventario()
        elif opcion == "4":
            break
        else:
            console.print("[yellow]Función en desarrollo...[/yellow]")
#Menu cliente (Faltan funciones)
def menu_cliente():
    while True:
        console.print("\n[bold cyan]Menú Cliente[/bold cyan]")
        console.print("1. Comprar")
        console.print("2. Ver mis compras")
        console.print("3. Salir")
        
        choice = Prompt.ask("Seleccione una opción")
        
        if choice == "3":
            break
        else:
            console.print("[yellow]Función en desarrollo...[/yellow]")

menu_principal()
