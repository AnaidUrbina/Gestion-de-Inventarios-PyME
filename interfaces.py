#Importar biblioteca rich las funciones que se ocuparan
#rich es para dar diferentes formatos o estilos al texto de la terminal (SALIDA)
from rich.console import Console 
from rich.prompt import Prompt

#Se crea una clase de tipo Console, permite imprimir en pantalla con diferentes estilos usando la biblioteca rich
#El nombre de la clase lo podemos cambiar
console = Console()

#Menu principal: permite iniciar sesion con los diferentes roles y cambiar contraseña de empleado
#Se puede crear una opcion más que sea para salir del programa
def menu_principal():
    console.print("[bold purple]Bienvenido al Sistema[/bold purple]")
    console.print("[green]1.[/] Administrador")
    console.print("[green]2.[/] Empleado")
    console.print("[green]3.[/] Cliente")
    console.print("[green]4.[/] Cambiar contraseña Empleado")
    rol = Prompt.ask("Seleccione la opcion deseada") #Se usa "prompt.ask" para que registre la respuesta a una pregunta como un string
    
    
    #Serie de condiciones para abrir el menu correspondiente al rol
    #Se pone el usuario y contraseña en cada condicion para que pueda manejar la opcion de "Opcion invalida"
    #Falta agregar el manejo de exepciones (Try-Except) puede que no sea necesario ya que se registra la respuesta como string
    if rol == "1":
        usuario = Prompt.ask("Ingrese su usuario")
        #Se usa "password = True" para ocultrar la contraseña a la vista
        password = Prompt.ask("Ingrese su contraseña", password = True)
        menu_administrador()
    elif rol == "2":
        usuario = Prompt.ask("Ingrese su usuario")
        #Se usa "password = True" para ocultrar la contraseña a la vista
        password = Prompt.ask("Ingrese su contraseña", password = True)
        menu_empleado()
    elif rol == "3":
        usuario = Prompt.ask("Ingrese su usuario")
        #Se usa "password = True" para ocultrar la contraseña a la vista
        password = Prompt.ask("Ingrese su contraseña", password = True)
        menu_cliente()
    elif rol == "4":
        console.print("[yellow]Función en desarrollo...[/yellow]")
    else:
       #Cuando entra aqui sale el mensaje y termina el programa
        console.print("[red]Opción inválida[/red]")
        #Si se le adjunta la llamada al menu principal sale em mensaje y vuelve a aparecer el menú hasta escoger una opcion valida
        #menu_principal()
#Menú del administrador
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
        console.print("8. Administar Empleados")
        console.print("9. Salir")
        opcion = Prompt.ask("Seleccione una opción")
    #Condiciones para entrar a los submenus del administrador (o cualquier otra opcion dentro)    
        if opcion == "1":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "2":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "3":
            modificacion_productos()
        elif opcion == "4":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "5":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "6":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "7":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "8":
            modificacion_empleados()
        elif opcion == "9":
            break
        else:
            console.print("[red]Opcion Invalida[/red]")
#Menú modificacion de productos (solo hay acceso desde el menu de admin)
def modificacion_productos():
    while True:
        console.print("\n[bold magenta]Modificación de Productos[/bold magenta]")
        console.print("1. Agregar producto")
        console.print("2. Eliminar producto")
        console.print("3. Modificar precio")
        console.print("4. Volver")
        opcion = Prompt.ask("Seleccione una opción: ")
    #Se va a cambiar la estructura de las condiciones para agregar la funcion correspondiente a cada una
        if opcion in ["1", "2", "3"]:
            #Preguntas de confirmacion/Autorizacion de realizar el cambio
            respuesta = Prompt.ask("¿Está seguro de realizar esta operacion?", choices=["si", "no"])
            #Se puede cambiar a que no tenga opciones predefinidas para que el mensaje salga en español (mensaje personalizado)
            #o se puede buscar la forma de personalizar el mensaje de esta funcion (es de la biblioteca rich)
            if respuesta.lower() == "si":
                console.print("[green]Operacion realizada con éxito[/green]")
            else:
                console.print("[red]Operacion cancelada[/red]")
        elif opcion == "4":
            break
        else:
            console.print("[red]Opcion Invalida[/red]")
#Menú modificacion de empleados (solo hay acceso desde el menu de admin)
def modificacion_empleados():
    while True:
        console.print("\n[bold]Administración de Empleados[/bold]", style="color(162)")
        console.print("1. Ver Empleados")
        console.print("2. Agregar Empleado")
        console.print("3. Eliminar Empleado")
        console.print("4. Modificar datos del Empleado")
        console.print("5. Volver")
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            console.print("[yellow]Funcion en desarrollo...[/yellow]")
        elif opcion in [2, 3, 4]:
            if opcion in ["1", "2", "3"]:
                #Preguntas de confirmacion/Autorizacion de realizar el cambio
                respuesta = Prompt.ask("¿Está seguro de realizar esta operacion?", choices=["si", "no"])
                if respuesta.lower() == "si":
                    console.print("[green]Operacion realizada con éxito[/green]")
                else:
                    console.print("[red]Operacion cancelada[/red]")
        elif opcion == "5":
            break
        else:
            console.print("[red]Opcion Invalida[/red]")
#Menú de empleado
def menu_empleado():
    while True:
        console.print("\n[bold cyan]Menú Empleado[/bold cyan]")
        console.print("1. Ventas")
        console.print("2. Ver reportes de ventas")
        console.print("3. Ver inventario")
        console.print("4. Salir")
        opcion = Prompt.ask("Seleccione una opción")
        if opcion == "1":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "2":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "3":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif opcion == "4":
            break
        else:
            console.print("[yellow]Función en desarrollo...[/yellow]")
#Menú del cliente
def menu_cliente():
    while True:
        console.print("\n[bold cyan]Menú Cliente[/bold cyan]")
        console.print("1. Comprar")
        console.print("2. Ver mis compras")
        console.print("3. Salir")
        choice = Prompt.ask("Seleccione una opción")
        if choice == "1":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif choice == "2":
            console.print("[yellow]Función en desarrollo...[/yellow]")
        elif choice == "3":
            break
        else:
            console.print("[red]Opcion Invalida[/red]")
            

#Manda a llamar a la funcion principal 
menu_principal()