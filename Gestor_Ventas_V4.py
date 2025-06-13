# || LIBRERIAS PARA MANUPULACIÓN DE DATOS ||
from contextlib import contextmanager
from  database_V4 import SessionLocal, Usuarios, Categorias, Productos, Inventarios, Movimientos, Clientes, Proveedores, Ventas, Compras, Auditorias
# || LIBRERIAS DE DISEÑO Y ESTRUCTURACIÓN VISUAL ||
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.table import Table
# || LIBRERIAS DE AUXILIARES ||
import re
from datetime import datetime
from passlib.hash import bcrypt

# << TEMAS DE ESTILOS >>
# [1] TEMA PARA MENSAJE DE ADVERTENCIAS
# [ANOTACIÓN]
    # Se define un objeto "tema_advertencia" de la clase "Console" de la librería "rich", utilizando un tema personalizado con distintos estilos de texto. 
    # El tema se configura con colores y formatos específicos para cada tipo de mensaje: "info" (información), "advice" (advertencia), "success" (éxito) y 
    # "error" (error), asignando un estilo en negrita y un color distinto para cada uno. Posteriormente, cuando queramos imprimir un mensaje con uno de estos
    # estilos, utilizamos "tema_advertencia.print()" y especificamos el tipo de estilo a aplicar mediante el parámetro "style".
tema_advertencia = Console(theme=Theme({
    "info": "bold #59AAF2",
    "advice": "bold #F9F953",
    "success": "bold #7CCA62",
    "error": "bold #EF675D"
}))

# <<< FUNCIONES AUXILIARES >>>
# [1] Función para generar el ID automático en cualquier tabla respetando que sea de tipo VARCHAR
def generar_nuevo_id(session, modelo, campo_id: str, prefijo: str, separador="_", ceros=3):
    cantidad = session.query(modelo).count()
    nuevo_num = cantidad + 1
    nuevo_id = f"{prefijo}{separador}{nuevo_num:0{ceros}d}"
    return nuevo_id

# [2] Función para guardar las auditorias de forma automática
def registrar_auditoria(db, id_usuario, entidad, operacion, descripcion):
    nueva_auditoria = Auditorias(
        id_usuario=id_usuario,
        entidad=entidad,
        operacion=operacion,
        descripcion=descripcion
    )
    db.add(nueva_auditoria)
    db.commit()

# [3] Función para mostrar las auditorias
def mostrar_auditorias(auditorias):
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("ID")
    table.add_column("Operación")
    table.add_column("Entidad")
    table.add_column("Descripción", overflow="fold")
    table.add_column("Fecha")
    table.add_column("ID Usuario")

    if not auditorias:
        print("[italic yellow]No se encontraron registros.[/]")
        return

    for a in auditorias:
        table.add_row(
            str(a.id_auditoria),
            a.operacion,
            a.entidad,
            a.descripcion,
            a.fecha.strftime("%Y-%m-%d"),
            a.id_usuario
        )

    print(table)

# [4] Función para mostrar las categorias
def lista_cat(categorias_lista):
    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
                    
    table.add_column("Id Categoria")
    table.add_column("Nombre")
    table.add_column("Descripción")
    table.add_column("Estado")
                    
    for categoria in categorias_lista:
        table.add_row(categoria.id_categoria, categoria.nombre, categoria.descripcion, categoria.estado)
    return table

#[5] Función para mostrar los productos
def lista_prod(db, productos_lista):
    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
    table.add_column("Id Producto")
    table.add_column("Nombre")
    table.add_column("Descripción")
    table.add_column("Precio unitario")
    table.add_column("Categoria")
    table.add_column("Estado")

    for producto in productos_lista:
        id_categoria = producto.id_categoria 
        categoria = db.query(Categorias).filter(Categorias.id_categoria == id_categoria).first()
        table.add_row(producto.id_producto, producto.nombre, producto.descripcion, str(producto.precio_unitario), categoria.nombre, producto.estado)
    return table 

#[6] Función para mostrar los proveedores
def lista_prov(proveedores_lista):
    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
    table.add_column("Id Proveedor")
    table.add_column("Empresa")
    table.add_column("Nombre")
    table.add_column("Apellido")
    table.add_column("Correo electrónico")
    table.add_column("Teléfono")

    for proveedor in proveedores_lista: 
        table.add_row(proveedor.id_proveedor, proveedor.empresa, proveedor.nombres, proveedor.apellidos, proveedor.email, proveedor.telefono)
    return table

#[7] Función para mostrar los empleados
def lista_emp(empleados):
    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
    table.add_column("ID Empleado")
    table.add_column("Nombres")
    table.add_column("Apellidos")
    table.add_column("Puesto")

    for emp in empleados:
        table.add_row(emp.id_usuario, emp.nombres, emp.apellidos, emp.puesto)
    return table

#[8] Función para mostrar los administradores
def lista_admin(administradores):
    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
    table.add_column("ID Administrador")
    table.add_column("Nombres")
    table.add_column("Apellidos")
    table.add_column("Puesto")

    for admin in administradores:
        table.add_row(admin.id_usuario, admin.nombres, admin.apellidos, admin.puesto)
    return table

#[9] Funcion para validar email
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

#[10] Función para mostrar los usuarios
def lista_usuarios(lista_usuarios):
    tabla = Table(title="Lista de Empleados", show_lines=True, style="cyan")
    tabla.add_column("ID_empleado", style="bold white", justify="center")
    tabla.add_column("Nombre", style="bold white")
    tabla.add_column("Apellido", style="bold white")
    tabla.add_column("Rol", style="bold white")
    tabla.add_column("Puesto", style="bold white")
    tabla.add_column("Salario", style="bold white", justify="right")
    tabla.add_column("Estado", style="bold white", justify="center")

    for usuario in lista_usuarios:
        tabla.add_row(
            str(usuario.id_usuario),
            usuario.nombres,
            usuario.apellidos,
            usuario.rol,
            usuario.puesto,
            f"${usuario.salario:.2f}",
            usuario.estado
        )

    return tabla

#[11] Función para Validar las contraseñas con bcrypt
def validar_contraseña(contraseña_ingresada, contraseña_guardada):
    try:
        return bcrypt.verify(contraseña_ingresada, contraseña_guardada)
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False

# <<<<<<<<<<<<<< MENUS >>>>>>>>>>>>>>
# [1] MENÚ DE INICIO DE SESIÓN
menu_login = Panel(""
"\n"
"[1] [white]Iniciar sesión como administrador[/]\n"
"[2] [white]Iniciar sesión como empleado[/]\n"
"[3] [white]Iniciar sesión como cliente[/]\n"
"[4] [white]Registro de Cliente[/]\n"
"[5] [white]Salir de la aplicación[/]\n", 
title="[bold #0F6FC6][ GESTOR DE VENTAS ][/]", subtitle="Inicio de sesión", style="#0F6FC6", width=50)

# [2] MENÚ DE ADMINISTRADOR
def adm_menu(ID, NAME, LAST_NAME, ROL, WORKSTATION):
    # [ANOTACION] 
        # Creamos el menú dentro de un panel (propiedad de la librería "Rich") para mejorar su formato visual. 
        # Luego, usamos un "print" dentro de una estructura de control para mostrar el menú del administrador.
    menu_adm = Panel(f"""
    [bold]Información del usuario:[/]
      • Nombre: [white]{NAME} {LAST_NAME}[/]
      • Puesto: [white]{ROL} - {WORKSTATION}[/]

    [bold]Compra y gestión de productos[/]
      [1] [white]Comprar productos[/]
      [2] [white]Gestión de productos[/]
      [3] [white]Gestión de categorías[/]
    [bold]Estado del inventario[/]
      [4] [white]Consultar inventario[/]
      [5] [white]Consultar alertas[/]
    [bold]Análisis de compras y ventas[/]
      [6] [white]Revisar movimientos[/]
      [7] [white]Consultar reporte de ventas[/]
      [8] [white]Consultar reporte de compras[/]
    [bold]Administración de empleados y roles[/]
      [9] [white]Gestión de empleados[/]
    [bold]Ajustes de cuenta[/]
      [10] [white]Editar perfil[/]
      [11] [white]Cerrar sesión[/]
    """, 
    title="[bold #009DD9][ PLATAFORMA DE ADMINISTRADOR ][/]", subtitle="Gestor de ventas", style="#009DD9", width=50)
    while True:
        print("\n")
        print(menu_adm)
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1': adm_submenu_compra(ID)
        elif opcion == '2': adm_submenu_producto(ID)
        elif opcion == '3': adm_submenu_categoria(ID)
        elif opcion == '4': show_inventary()
        elif opcion == '5': adm_submenu_alerta(ID)
        elif opcion == '6': adm_submenu_movimientos(ID)
        elif opcion == '7': adm_submenu_reporteVen()
        elif opcion == '8': adm_submenu_reporteCom()
        elif opcion == '9': adm_submenu_empleado(ID)
        elif opcion == '10': adm_submenu_perfil(ID)
        elif opcion == '11':
            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha cerrado sesión correctamente \n", style="success")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente", style="error")

# [3] MENÚ DE EMPLEADO
def emp_menu(ID, NAME, LAST_NAME, ROL, WORKSTATION):
    # [ANOTACION] 
        # Creamos el menú dentro de un panel (propiedad de la librería "Rich") para mejorar su formato visual. 
        # Luego, usamos un "print" dentro de una estructura de control para mostrar el menú del administrador.
    menu_emp = Panel(f"""
    [bold]Información del usuario:[/]
      • Nombre: [white]{NAME} {LAST_NAME}[/]
      • Puesto: [white]{ROL} - {WORKSTATION}[/]

    [bold]Gestión de productos[/]
      [1] [white]Venta de productos[/]
      [2] [white]Consultar inventario[/]
    [bold]Mis movimientos[/]
      [3] [white]Consultar reporte de ventas[/]
    [bold]Ajustes de cuenta[/]
      [4] [white]Editar perfil[/]
      [5] [white]Cerrar sesión[/]
    """,
    title="[bold #009DD9][ PLATAFORMA DE EMPLEADO ][/]", subtitle="Gestor de ventas", style="#009DD9", width=50)
    while True:
        print("\n")
        print(menu_emp)
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1': menu_venta_empleado(ID)
        elif opcion == '2': show_inventary()
        elif opcion == '3': reporte_ventas_empleado (ID)
        elif opcion == '4': editar_perfil_empleado (ID)
        elif opcion == '5':
            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha cerrado sesión correctamente \n", style="success")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente", style="error")

# [4] REGISTRO DE CLIENTES EN EL MENÚ PRINCIPAL
def registrar_cliente():
    title = Panel("REGISTRO DE NUEVO CLIENTE", style="bold #7CCA62", width=50)
    print(title)

    with obtener_session() as db:
        id_cliente = generar_nuevo_id(db, Clientes, "id_cliente", "CLI", ceros=3)
        tema_advertencia.print(f"[INFO \u2139 ] ID generado automáticamente", style="info")

        # Validar nombre
        while True:
            nombres = Prompt.ask("  [#7CCA62]>[/] [white]Nombre(s)[/]").strip()
            if not nombres:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] El nombre no puede estar vacío.\n", style="error")
            else:
                break

        # Validar apellido
        while True:
            apellidos = Prompt.ask("  [#7CCA62]>[/] [white]Apellido(s)[/]").strip()
            if not apellidos:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] El apellido no puede estar vacío.\n", style="error")
            else:
                break

        # Validar teléfono: solo números y 10 dígitos
        while True:
            telefono = Prompt.ask("  [#7CCA62]>[/] [white]Teléfono (10 dígitos)[/]").strip()
            if not telefono:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] El teléfono no puede estar vacío.\n", style="error")
            elif not telefono.isdigit():
                tema_advertencia.print("[FORMATO INVÁLIDO ❌ ] El teléfono debe contener solo números.\n", style="error")
            elif len(telefono) != 10:
                tema_advertencia.print("[LONGITUD INCORRECTA ❌ ] El teléfono debe tener exactamente 10 dígitos.\n", style="error")
            else:
                break

        # Validar dirección
        while True:
            direccion = Prompt.ask("  [#7CCA62]>[/] [white]Dirección[/]").strip()
            if not direccion:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] La dirección no puede estar vacía.\n", style="error")
            else:
                break

        # Validar correo
        while True:
            correo = Prompt.ask("  [#7CCA62]>[/] [white]Correo electrónico[/]").strip()
            if not correo:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] El correo no puede estar vacío.\n", style="error")
                continue
            if not validar_email(correo):
                tema_advertencia.print("[FORMATO INVÁLIDO ❌ ] Ingrese un correo electrónico válido.\n", style="error")
                continue
            cliente_existente = db.query(Clientes).filter(Clientes.email == correo).first()
            if cliente_existente:
                tema_advertencia.print("[CORREO YA REGISTRADO ❌ ] Intente con otro correo.\n", style="error")
            else:
                break

        # Validar usuario
        while True:
            usuario = Prompt.ask("  [#7CCA62]>[/] [white]Usuario: [/]").strip()
            if not usuario:
                tema_advertencia.print("[CAMPO VACÍO ❌ ] El nombre de usuario no puede estar vacío.\n", style="error")
                continue
            usuario_existente = db.query(Clientes).filter(Clientes.usuario == usuario).first()
            if usuario_existente:
                tema_advertencia.print("[USUARIO NO DISPONIBLE ❌ ] Intente con otro nombre de usuario.\n", style="error")
            else:
                break

        # Validar contraseña
        while True:
            contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Cree una contraseña[/]", password=True).strip()
            confirmar = Prompt.ask("  [#7CCA62]>[/] [white]Confirme su contraseña[/]", password=True).strip()
            if not contraseña or not confirmar:
                tema_advertencia.print("[CONTRASEÑA VACÍA ❌ ] La contraseña no puede estar vacía.\n", style="error")
                continue
            if contraseña != confirmar:
                tema_advertencia.print("[CONTRASEÑAS NO COINCIDEN ❌ ] Intente de nuevo.\n", style="error")
            else:
                break

        # Guardar cliente
        nuevo_cliente = Clientes(
            id_cliente=id_cliente,
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            direccion=direccion,
            email=correo,
            usuario=usuario,
            contraseña=bcrypt.hash(contraseña),
            estado="Activo"
        )
        db.add(nuevo_cliente)
        db.commit()

        registrar_auditoria(
            db,
            id_cliente,
            'Clientes',
            'Registro de Cliente',
            f'Se dio de alta el cliente {id_cliente}'
        )

        tema_advertencia.print("[REGISTRO EXITOSO \u2714 ] Cliente registrado correctamente.\n", style="success")


# << SUBMENÚS DEL MENÚ DE ADMINISTRADOR >>
# [1] SUBMENÚ ADM. COMPRA DE PRODUCTOS
def adm_submenu_compra(ID):    
    submenu_compra = Panel(""
    "\n"
    "[1] [white]Registrar compra de productos[/]\n"
    "[2] [white]Registrar proveedor[/]\n"
    "[3] [white]Listado de proveedores[/]\n"
    "[4] [white]Gestión de proveedores[/]\n"
    "[5] [white]Regresar[/]\n", 
    title="[bold #0BD0D9][ COMPRAR PRODUCTOS ][/]", subtitle="Compra y gestión de productos", style="#0BD0D9", width=50)
    while True:
        print(submenu_compra)
        opcion = input("\nSeleccione una opción: ")
        if opcion == '1':
            title = Panel("REGISTRAR COMPRA DE PRODUCTO", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                productos_lista = db.query(Productos).filter(Productos.estado == "Activo").all()
                proveedores_lista = db.query(Proveedores).filter(Proveedores.estado =="Activo").all()

                if usuario:
                    user_id = usuario.id_usuario
                    contraseña = usuario.contraseña
                    print(title)

                    # (COMPROBACIÓN) Solicitamos el ingreso del id_producto, el cual ya debió registrarse anteriormente.
                    while True:
                        producto_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el identificador del producto.[/] [#7CCA62](Para consultar lista de productos oprima '?')[/]")
                        productos_ids = {producto.id_producto for producto in productos_lista}

                        if producto_id == '?':
                            table = lista_prod(db, productos_lista)
                            print (table)
                        elif producto_id not in productos_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ningún producto asociado a ese ID. Intenta de nuevo.\n", style="error")
                        else:
                            break
                    
                    description = Prompt.ask("  [#7CCA62]>[/] [white]Descripción del movimiento[/]")
                    quantity = int(Prompt.ask("  [#7CCA62]>[/] [white]Cantidad de productos comprados[/]"))

                    # (TABLA) Definición de tabla que enliste los proveedores registrados en la base de datos para su consulta
                    table = lista_prov(proveedores_lista)

                    # (COMPROBACIÓN) Solicitamos el ingreso del id_proveedor, el cual ya debió registrarse anteriormente.
                    while True:
                        proveedor_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el identificador del proveedor.[/] [#7CCA62](Para consultar lista de proveedores oprima '?')[/]")
                        proveedor_ids = {proveedor.id_proveedor for proveedor in proveedores_lista}

                        if proveedor_id == '?':
                            print(table)
                        elif proveedor_id not in proveedor_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ningún proveedor asociado a ese ID. Intenta de nuevo.\n", style="error")
                        else:
                            break

                    # (COMPROBACIÓN) Revisión de los datos ingresados, asegurando el ingreso de un dato flotante
                    while True:
                        try:
                            Subtotal = float(Prompt.ask("  [#7CCA62]>[/] [white]Subtotal[/]"))
                            break
                        except ValueError:
                            tema_advertencia.print("[ERROR \u274C ] El subtotal debe ser un número válido. Intente nuevamente.\n", style="error")
                    
                    while True:
                        try:
                            tax = float(Prompt.ask("  [#7CCA62]>[/] [white]Impuesto (%) (ej. 15 para 15%)[/]"))
                            break
                        except ValueError:
                            tema_advertencia.print("[ERROR \u274C ] El impuesto debe ser un número válido. Intente nuevamente.\n", style="error")
                    
                    Total = Subtotal + (Subtotal * (tax / 100))
                    Tipo = "Compra"
                    State = "Activo"

                    #(ADVERTENCIA) Se advierte al administrador si desea realizar cambios en la base de datos
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea realizar la compra? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            movimiento_nuevo = Movimientos(
                                id_usuario = user_id,
                                id_producto = producto_id,
                                descripcion = description,
                                cantidad = quantity,
                                subtotal = Subtotal,
                                impuesto = tax,
                                total = Total,
                                tipo = Tipo,
                                estado = State
                            )
                            db.add(movimiento_nuevo)
                            db.commit()

                            id_movimiento_nuevo = movimiento_nuevo.id_movimiento
                            compra_nueva = Compras(
                                id_movimiento = id_movimiento_nuevo,
                                id_proveedor = proveedor_id        
                            )
                            db.add(compra_nueva)
                            db.commit()

                            producto_en_inventario = db.query(Inventarios).filter(Inventarios.id_producto == producto_id).first()
                            if producto_en_inventario:
                                producto_en_inventario.cantidad += quantity
                                db.commit()
                            else:
                                tema_advertencia.print("[ERROR \u274C ] El producto no está registrado en el inventario.\n", style="error")

                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] La compra ha sido realizada.\n", style="success")

                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")
                    
                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")

                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")
        elif opcion == '2':
            title = Panel("REGISTRAR NUEVO PROVEEDOR", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                if usuario:
                    contraseña = usuario.contraseña
                    print(title)

                    #Generación automática del ID del proveedor
                    id = generar_nuevo_id(db, Proveedores, 'id_proveedor', 'PROV', ceros= 3)
                    tema_advertencia.print(f"[INFO \u2139 ] ID generado automáticamente: {id}", style="advice")

                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre(s)[/]")
                    last_name = Prompt.ask("  [#7CCA62]>[/] [white]Apellido(s)[/]")
                    phone = Prompt.ask("  [#7CCA62]>[/] [white]Telefono[/]")
                    address = Prompt.ask("  [#7CCA62]>[/] [white]Dirección de la empresa[/]")
                    # Correo electrónico y validación
                    while True:
                        mail = Prompt.ask("  [#7CCA62]>[/] [white]Correo electrónico[/]")
                        if validar_email(mail):
                            break
                        else:
                            tema_advertencia.print("[CORREO INVÁLIDO \u274C ] Ingrese un correo electrónico válido (ej. usuario@dominio.com).\n", style="error")
                    business = Prompt.ask("  [#7CCA62]>[/] [white]Nombre de la empresa a la que esta asociado[/]")

                    #(COMPROBACIÓN) Revisión de datos ingresados a partir de una verificación de valores
                    while True:
                        state = Prompt.ask("  [#7CCA62]>[/] [white]Estado[/]")
                        if state not in ['Activo', 'Inactivo']:
                            tema_advertencia.print("[ESTADO INVÁLIDO \u274C ] Debe ser 'Activo' o 'Inactivo'.\n", style="error")
                        else: break

                    #(ADVERTENCIA) Se advierte al administrador si desea realizar cambios en la base de datos
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea dar de alta al proveedor en el sistema? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            with obtener_session() as db:
                                proveedor_nuevo = Proveedores(
                                    id_proveedor=id,
                                    nombres=name,
                                    apellidos=last_name,
                                    telefono=phone,
                                    direccion=address,
                                    email=mail,
                                    empresa=business,
                                    estado=state,
                                )
                                db.add(proveedor_nuevo)
                                db.commit()
                                tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se dado de alta al nuevo proveedor.\n", style="success")
                                # Registrar auditoría
                                registrar_auditoria(
                                    db=db,
                                    operacion="Alta",
                                    entidad="proveedor",
                                    id_usuario=ID,
                                    descripcion=f"Se dio de Alta el nuevo proveedor '{proveedor_nuevo.nombres}': ID='{proveedor_nuevo.id_proveedor}', Empresa='{proveedor_nuevo.empresa}', Teléfono={proveedor_nuevo.telefono}, estado='{proveedor_nuevo.estado}'."
                                )

                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")
                    
                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")
                
                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")
        elif opcion == '3':
            title = Panel("LISTA DE PROVEEDORES", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                #Se filtran los proveedores que estan activos, a menos que se muestre el estado de cada proveedor
                #se quita el filtro y se agrega el estado a la tabla que se imprime en pantalla
                proveedores_lista = db.query(Proveedores).filter(Proveedores.estado == "Activo").all()
                if proveedores_lista:
                    table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")
                    #Se llena la cabecera de la tabla
                    table.add_column("Id Proveedor")
                    table.add_column("Empresa")
                    table.add_column("Nombre")
                    table.add_column("Apellido")
                    table.add_column("Correo electrónico")
                    table.add_column("Teléfono")

                    # Instrucción para llenar las filas de la tabla
                    for proveedor in proveedores_lista: 
                        table.add_row(proveedor.id_proveedor, proveedor.empresa, proveedor.nombres, proveedor.apellidos, proveedor.email, proveedor.telefono)
            
                    print(title)
                    print(table)
                    print("\n")
                    
                else: tema_advertencia.print("[ERROR \u274C ] Aún no se han incluido proveedores en el sistema.\n", style="error")
        elif opcion == '4':
            menu = Panel(""
            "\n"
            "  [1] [white]Dar de baja proveedor[/]\n"
            "  [2] [white]Dar de alta proveedor[/]\n"
            "  [3] [white]Regresar[/]",
            title="[bold #7CCA62]SUBMENÚ DE ESTADO DE PROVEEDORES[/]",
            subtitle="Administración de alta y baja", style="#7CCA62", width=60
            )

            while True:
                print(menu)
                opcion = input("\nSeleccione una opción: ")

                if opcion == "1":
                    title = Panel("BAJA DE PROVEEDOR", style="bold #FF5555", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        proveedores_lista = db.query(Proveedores).filter(Proveedores.estado == "Activo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)

                            table = lista_prov(proveedores_lista)
                            while True:
                                proveedor_id = Prompt.ask("  [red]>[/] [white]Ingrese el ID del proveedor a dar de baja[/] [red](‘?’ para ver lista)[/]")
                                if proveedor_id == '?':
                                    print(table)
                                    continue

                                proveedor = db.query(Proveedores).filter(Proveedores.id_proveedor == proveedor_id, Proveedores.estado == "Activo").first()
                                if not proveedor:
                                    tema_advertencia.print("[ERROR \u274C ] No se encontró un proveedor activo con ese ID. Intenta nuevamente.\n", style="error")
                                else:
                                    break

                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Está seguro de que desea dar de baja este proveedor? S/N", style="advice")
                            opcion = input("Opción: ").upper()

                            if opcion == 'S':
                                adm_contraseña = Prompt.ask("  [red]>[/] [white]Confirme su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    proveedor.estado = "Inactivo"
                                    db.commit()

                                    registrar_auditoria(
                                        db=db,
                                        operacion="Baja",
                                        entidad="Proveedor",
                                        id_usuario=ID,
                                        descripcion=f"Se dio de baja al proveedor '{proveedor.id_proveedor}' ({proveedor.nombres})."
                                    )

                                    tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El proveedor fue dado de baja correctamente.\n", style="success")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta de nuevo.\n", style="error")
                            elif opcion == 'N':
                                tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error") 
                        else:
                                tema_advertencia.print("[ERROR \u274C ] Usuario no encontrado en la base de datos.\n", style="error")
                elif opcion == "2":
                    title = Panel("REACTIVAR PROVEEDOR", style="bold #7CCA62", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        proveedores_inactivos = db.query(Proveedores).filter(Proveedores.estado == "Inactivo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)

                            table= lista_prov(proveedores_inactivos)

                            while True:
                                proveedor_id = Prompt.ask("  [green]>[/] [white]Ingrese el ID del proveedor a reactivar[/] [green](‘?’ para ver lista)[/]")
                                if proveedor_id == '?':
                                    print(table)
                                    continue

                                proveedor = db.query(Proveedores).filter(Proveedores.id_proveedor == proveedor_id, Proveedores.estado == "Inactivo").first()
                                if not proveedor:
                                    tema_advertencia.print("[ERROR \u274C ] No se encontró un proveedor inactivo con ese ID. Intenta nuevamente.\n", style="error")
                                else:
                                    break

                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea reactivar este proveedor? S/N", style="advice")
                            opcion = input("Opción: ").upper()

                            if opcion == 'S':
                                adm_contraseña = Prompt.ask("  [green]>[/] [white]Confirme su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    proveedor.estado = "Activo"
                                    db.commit()

                                    registrar_auditoria(
                                        db=db,
                                        operacion="Alta",
                                        entidad="Proveedor",
                                        id_usuario=ID,
                                        descripcion=f"Reactivó al proveedor '{proveedor.id_proveedor}' ({proveedor.nombres})."
                                    )

                                    tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El proveedor fue reactivado correctamente.\n", style="success")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta de nuevo.\n", style="error")
                            elif opcion == 'N':
                                tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")

                        else:
                            tema_advertencia.print("[ERROR \u274C ] Usuario no encontrado en la base de datos.\n", style="error")
                elif opcion == "3":
                    tema_advertencia.print("Regresando al menú principal...\n", style="advice")
                    break
        elif opcion == '5':
            tema_advertencia.print("Regresando el menú principal... \n", style="advice")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# [2] SUBMENÚ ADM. GESTIÓN DE PRODUCTOS
def adm_submenu_producto(ID):
    submenu_producto = Panel(""
    "\n"
    "[1] [white]Agregar producto[/]\n"
    "[2] [white]Modificar producto[/]\n"
    "[3] [white]Modificar precio de producto[/]\n"
    "[4] [white]Cambiar estado producto[/]\n"
    "[5] [white]Listado de productos[/]\n"
    "[6] [white]Regresar[/]\n",
    title="[bold #0BD0D9][ GESTIÓN DE PRODUCTOS ][/]", subtitle="Compra y gestión de productos", style="#0BD0D9", width=50)
    while True:
        print(submenu_producto)
        opcion = input("\nSeleccione una opción: ")
        #Agregar producto nuevo
        if opcion == '1':
            title = Panel("AGREGAR PRODUCTO", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                categorias_lista = db.query(Categorias).all()

                if usuario:
                    contraseña = usuario.contraseña
                    print(title)

                    #Generación automática del ID del proveedor
                    id = generar_nuevo_id(db, Productos, "id_producto", prefijo="PROD", ceros=3)
                    tema_advertencia.print(f"[INFO \u2139 ] ID generado automáticamente: {id}\n", style="info")

                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre[/]")
                    description = Prompt.ask("  [#7CCA62]>[/] [white]Descripción[/]")

                    while True:
                        try:
                            unit_price = float(Prompt.ask("  [#7CCA62]>[/] [white]Precio unitario[/]"))
                            break
                        except ValueError:
                            tema_advertencia.print("[ERROR \u274C ] El precio unitario debe ser un número válido. Intente nuevamente.\n", style="error")
                

                    # Se evalua si el ID categoria es válido
                    while True:
                        categoria_ids = [categoria.id_categoria for categoria in categorias_lista]
                        
                        id_category = Prompt.ask("  [#7CCA62]>[/] [white]Id categoria a la que pertenece el producto.[/] [#7CCA62](Para consultar lista de caegorias oprima '?')[/]")
                        if id_category == "?":
                            table= lista_cat(categorias_lista)
                            print(table)
                        elif id_category not in categoria_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ninguna categoría asociada a ese ID. Intenta de nuevo.\n", style="error")
                        else: break

                    while True:
                        state = Prompt.ask("  [#7CCA62]>[/] [white]Estado[/]")
                        if state not in ['Activo', 'Inactivo']:
                            tema_advertencia.print("[ESTADO INVÁLIDO \u274C ] Debe ser 'Activo' o 'Inactivo'.\n", style="error")
                        else: break
                    
                    min_quantity = int(Prompt.ask("  [#7CCA62]>[/] [white]¿Qué cantidad mínima debe haber del producto en stock?[/]"))
                    estado_inventario = state

                    #(ADVERTENCIA) Se advierte al administrador si desea realizar cambios en la base de datos
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea dar de alta este producto en el sistema? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            with obtener_session() as db:
                                producto_nuevo = Productos(
                                    id_producto=id,
                                    nombre=name,
                                    descripcion=description,
                                    precio_unitario=unit_price,
                                    id_categoria=id_category,
                                    estado=state,
                                )
                                db.add(producto_nuevo)
                                db.commit()

                                inventario_nuevo = Inventarios(
                                    id_producto = id,
                                    cantidad = 0,
                                    cantidad_min = min_quantity,
                                    estado=estado_inventario
                                )

                                db.add(inventario_nuevo)
                                db.commit()
                                tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha dado de alta un nuevo producto.\n", style="success")
                                # Aquí podrías registrar en tabla de auditoría:
                                registrar_auditoria(
                                    db=db,
                                    operacion="Alta",
                                    entidad="Producto",
                                    id_usuario=ID,
                                    descripcion=f"Agregó el producto '{producto_nuevo.nombre}' con id '{producto_nuevo.id_producto}', con precio ${producto_nuevo.precio_unitario:.2f} y categoría '{producto_nuevo.id_categoria}'."
                                )
                           
                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")
                        

                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")

                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")
        #Modificar producto existente
        elif opcion == '2':
            title = Panel("MODIFICAR DE PRODUCTO", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                productos_lista = db.query(Productos).all()
                categorias_lista = db.query(Categorias).all()

                if usuario:
                    contraseña = usuario.contraseña
                    print(title)

                    while True:
                        producto_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el identificador del producto.[/] [#7CCA62](Para consultar lista de productos oprima '?')[/]")
                        
                        productos_ids = {producto.id_producto for producto in productos_lista}
                        if producto_id == '?':
                            table = lista_prod(db, productos_lista)
                            print (table)
                        elif producto_id not in productos_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ningún producto asociado a ese ID. Intenta de nuevo.\n", style="error")
                        else:
                            producto = db.query(Productos).filter_by(id_producto=producto_id).first()
                            break

                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre[/]")
                    description = Prompt.ask("  [#7CCA62]>[/] [white]Descripción[/]")
                    
                    while True:
                        try:
                            unit_price = float(Prompt.ask("  [#7CCA62]>[/] [white]Precio unitario[/]"))
                            break
                        except ValueError:
                            tema_advertencia.print("[ERROR \u274C ] El precio unitario debe ser un número válido. Intente nuevamente.\n", style="error")
                    
                    # Se define la tabla de categorias para facilitar al usuario la eleccion de categoria del producto nuevo
                    table = lista_cat(categorias_lista)

                    # Se evalua si el ID categoria es válido
                    while True:
                        categoria_ids = [categoria.id_categoria for categoria in categorias_lista]
                        
                        id_category = Prompt.ask("  [#7CCA62]>[/] [white]Id de la categoria a la que pertenece el producto.[/] [#7CCA62](Para consultar lista de caegorias oprima '?')[/]")
                        if id_category == "?":
                            print(table)

                        elif id_category not in categoria_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ninguna categoría asociada a ese ID. Intenta de nuevo.\n", style="error")
                        else: 
                            break

                    while True:
                        state = Prompt.ask("  [#7CCA62]>[/] [white]Estado[/]")
                        if state not in ['Activo', 'Inactivo']:
                            tema_advertencia.print("[ESTADO INVÁLIDO \u274C ] Debe ser 'Activo' o 'Inactivo'.\n", style="error")
                        else: 
                            break

                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea dar de alta este producto en el sistema? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            producto.nombre = name if name else producto.nombre
                            producto.descripcion = description if description else producto.descripcion
                            producto.precio_unitario = unit_price if unit_price else producto.precio_unitario
                            producto.id_categoria = id_category if id_category else producto.id_categoria
                            producto.estado = state if state else producto.estado
                            db.commit()
                            # Registrar auditoría
                            registrar_auditoria(
                                db=db,
                                operacion="Modificación",
                                entidad="Producto",
                                id_usuario=ID,
                                descripcion=f"Modificó el producto '{producto.id_producto}': nombre='{producto.nombre}', descripción='{producto.descripcion}', precio=${producto.precio_unitario}, categoría='{producto.id_categoria}', estado='{producto.estado}'."
                            )

                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha actualizado los datos del producto", style="success")

                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")

                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")

                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")
        #Modificar el precio de un producto existente
        elif opcion == '3':
            title = Panel("MODIFICAR PRECIO DE PRODUCTO", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                productos_lista = db.query(Productos).filter(Productos.estado == "Activo").all()
                if usuario:
                    contraseña = usuario.contraseña
                    print(title)

                    # (TABLA) Definición de tabla que enliste los productos registrados en la base de datos para su consulta
                    table = lista_prod (db,productos_lista)
                    # Solicitar ID del Producto
                    while True:
                        productos_id = Prompt.ask("  [red]>[/] [white]Ingrese el ID del producto que desea modificar[/] [red](oprima '?' para ver lista)[/]")
                        productos_ids = {c.id_producto for c in productos_lista}

                        if productos_id == '?':
                            print(table)
                        elif productos_id not in productos_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe un producto activo con ese ID. Intente de nuevo.\n", style="error")
                        else:
                            producto = db.query(Productos).filter_by(id_producto=productos_id).first()
                            break
                    print(f"Producto seleccionado: [bold]{producto.nombre}[/] - Precio actual: [green]${producto.precio_unitario:.2f}[/]")
                    nuevo_precio = float(Prompt.ask("Ingrese el nuevo precio"))

                    confirmacion = Prompt.ask(f"¿Confirmas cambiar el precio de '{producto.nombre}' a ${nuevo_precio:.2f}? (S/N)").upper()

                    if confirmacion == "S":
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            precio_anterior = producto.precio_unitario
                            producto.precio_unitario = nuevo_precio
                            db.commit()
                            tema_advertencia.print(f"Precio actualizado de ${precio_anterior:.2f} a ${nuevo_precio:.2f} ✅", style="success")

                        # Aquí podrías registrar en tabla de auditoría:
                        registrar_auditoria(
                            db=db,
                            operacion="Modificación",
                            entidad="Producto",
                            id_usuario=ID, 
                            descripcion=f"Modificó el precio del producto '{producto.nombre}' de ${precio_anterior:.2f} a ${nuevo_precio:.2f}."
                        )
                    else:
                        tema_advertencia.print("Operación cancelada.", style="info")
        #Gestión de productos (Alta y Baja)
        elif opcion == '4':
            menu = Panel(
                "[bold green]Gestión de Productos[/]\n"
                "\n"
                "  [1] [white]Dar de baja producto[/]\n"
                "  [2] [white]Dar de alta producto[/]\n"
                "  [3] [white]Regresar al menú principal[/]",
                title="[bold #7CCA62]SUBMENÚ DE ESTADO DE PRODUCTOS[/]",
                subtitle="Administración de alta y baja", style="#7CCA62", width=60
            )

            while True:
                print(menu)
                opcion = input("\nSeleccione una opción: ")

                if opcion == "1":
                    title = Panel("BAJA DE PRODUCTO", style="bold #FF5555", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        productos_lista = db.query(Productos).filter(Productos.estado == "Activo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)

                            while True:
                                productos_id = Prompt.ask("  [red]>[/] [white]Ingrese el ID del producto que desea desactivar[/] [red](oprima '?' para ver lista)[/]")
                                productos_ids = {c.id_producto for c in productos_lista}

                                if productos_id == '?':
                                    table = lista_prod(db,productos_lista)
                                    print(table)
                                elif productos_id not in productos_ids:
                                    tema_advertencia.print("[ERROR \u274C ] No existe un producto activo con ese ID. Intente de nuevo.\n", style="error")
                                else:
                                    break

                            # Confirmación
                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea desactivar este producto? S/N", style="advice")
                            opcion = input("Opcion: ").upper()
                            if opcion == 'S':
                                adm_contraseña = Prompt.ask("  [red]>[/] [white]Digite su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    producto = db.query(Productos).filter(Productos.id_producto == productos_id).first()
                                    inventario = db.query(Inventarios).filter_by(id_producto=productos_id).first()
                                    if producto:
                                        producto.estado = "Inactivo"
                                        inventario.estado = "Inactivo"
                                        db.commit()

                                        # Auditoría
                                        registrar_auditoria(
                                            db=db,
                                            id_usuario=ID,
                                            operacion="Baja",
                                            entidad="Producto",
                                            descripcion=f"Se desactivó el producto '{producto.nombre}'"
                                        )
                                        db.commit()
                                        tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El producto ha sido desactivada.\n", style="success")
                                    else:
                                        tema_advertencia.print("[ERROR \u274C ] No se encontró el producto seleccionado.\n", style="error")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")

                            elif opcion == 'N':
                                tema_advertencia.print("\n[INFORMACIÓN \u2139] Se canceló la operación.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")
                        else:
                            tema_advertencia.print("[ERROR \u274C ] No se encontró el usuario.\n", style="error")

                elif opcion == "2":
                    title = Panel("REACTIVAR PRODUCTO", style="bold #7CCA62", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        productos_inactivos = db.query(Productos).filter(Productos.estado == "Inactivo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)
                        # (TABLA) Definición de tabla que enliste los productos registrados en la base de datos para su consulta
                            table = lista_prod(db,productos_inactivos)
                            while True:
                                productos_id = Prompt.ask("  [green]>[/] [white]Ingrese el ID del producto que desea reactivar[/] [green](oprima '?' para ver lista)[/]")
                                productos_ids = {c.id_producto for c in productos_inactivos}

                                if productos_id == '?':
                                    print(table)
                                elif productos_id not in productos_ids:
                                    tema_advertencia.print("[ERROR \u274C ] No existe un producto inactivo con ese ID. Intente de nuevo.\n", style="error")
                                else:
                                    producto = db.query(Productos).filter_by(id_producto=productos_id).first()
                                    inventario = db.query(Inventarios).filter_by(id_producto=productos_id).first()
                                    break
                            
                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea reactivar este producto? S/N", style="advice")
                            confirm = input("Opción: ").upper()

                            if confirm == 'S':
                                adm_contraseña = Prompt.ask("  [green]>[/] [white]Confirme su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    producto.estado = "Activo"
                                    inventario.estado= "Activo"
                                    db.commit()

                                    registrar_auditoria(
                                        db=db,
                                        operacion="Alta",
                                        entidad="Producto",
                                        id_usuario=ID,
                                        descripcion=f"Reactivó el producto '{producto.id_producto}' ({producto.nombre})."
                                    )

                                    tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El producto fue reactivado correctamente.\n", style="success")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta de nuevo.\n", style="error")
                            elif confirm == 'N':
                                tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")
                        else:
                            tema_advertencia.print("[ERROR \u274C ] No se encontró el usuario.\n", style="error")
                
                elif opcion == '3':
                    break
                else:
                    tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")
        #Lista de productos               
        elif opcion == '5':
            title = Panel("LISTA DE PRODUCTOS", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                productos_lista = db.query(Productos).all()
                if productos_lista:
                    table = lista_prod(db, productos_lista)
                    
                    print(title)
                    print(table)
                    print("\n")
                    
                else: tema_advertencia.print("[ERROR \u274C ] Aún no se han incluido productos en el sistema.\n", style="error")
        #Regresa al menú principal
        elif opcion == '6':
            tema_advertencia.print("Regresando el menú principal... \n", style="advice")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")  
        
# [3] SUBMENÚ ADM. GESTIÓN DE CATEGORÍAS
def adm_submenu_categoria(ID):
    submenu_categoria = Panel(""
    "\n"
    "[1] [white]Agregar categoría[/]\n"
    "[2] [white]Modificar categoría[/]\n"
    "[3] [white]Cambiar estado de categoría[/]\n"
    "[4] [white]Listar categorías[/]\n"
    "[5] [white]Regresar[/]\n",
    title="[bold #0BD0D9][ GESTIÓN DE CATEGORÍAS ][/]", subtitle="Compra y gestión de productos", style="#0BD0D9", width=50)
    while True:
        print(submenu_categoria)
        opcion = input("\nSeleccione una opción: ")
        if opcion == '1':
            title = Panel("AGREGAR CATEGORÍA", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                if usuario:
                    contraseña = usuario.contraseña
                    print(title)

                    # Generacion automática de ID
                    id = generar_nuevo_id(db, Categorias, "id_categoria", prefijo="CAT", ceros=3)
                    tema_advertencia.print(f"[INFO \u2139 ] ID generado automáticamente: {id}\n", style="info")


                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre[/]")
                    description = Prompt.ask("  [#7CCA62]>[/] [white]Descripción[/]")

                    # (COMPROBACIÓN) Revisión de variable estado acordado con los parámetros de valores permitidos
                    while True:
                        state = Prompt.ask("  [#7CCA62]>[/] [white]Estado[/]")
                        if state not in ['Activo', 'Inactivo']:
                            tema_advertencia.print("[ESTADO INVÁLIDO \u274C ] Debe ser 'Activo' o 'Inactivo'.\n", style="error")
                        else: break

                    #(ADVERTENCIA) Se advierte al administrador si desea realizar cambios en la base de datos
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea dar de alta esta categoría en el sistema? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            with obtener_session() as db:
                                categoria_nueva = Categorias(
                                    id_categoria=id,
                                    nombre=name,
                                    descripcion=description,
                                    estado=state,
                                )
                                db.add(categoria_nueva)
                                db.commit()

                                registrar_auditoria(
                                    db,
                                    id_usuario=ID,
                                    entidad="Categoría",
                                    operacion="Alta",
                                    descripcion=f"Alta de categoría '{Categorias.id_categoria}': nombre='{name}', descripción='{description}', estado='{state}'"
                                )
                                db.commit()
                                tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha dado de alta una nueva categoría.\n", style="success")
                        
                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")

                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")

                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")

        elif opcion == '2':
            title = Panel("MODIFICAR CATEGORÍA", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                categorias_lista = db.query(Categorias).all()

                if usuario:
                    contraseña = usuario.contraseña
                    print(title)
                    
                    
                    # (COMPROBACIÓN) Revisión del identificador ingresado, se segura que se seleccione uno de los ya ingresados.
                    while True:
                        categoria_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el identificador de la categoría.[/] [#7CCA62](Para consultar lista de categorías oprima '?')[/]")
                        categorias_ids = {categoria.id_categoria for categoria in categorias_lista}
                        if categoria_id == '?':
                            table= lista_cat(categorias_lista)
                            print(table)
                        elif categoria_id not in categorias_ids:
                            tema_advertencia.print("[ERROR \u274C ] No existe ninguna categoria asociada a ese ID. Intenta de nuevo.\n", style="error")
                        else:
                            break
                    categoria = db.query(Categorias).filter(Categorias.id_categoria == categoria_id).first()
                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre[/]")
                    description = Prompt.ask("  [#7CCA62]>[/] [white]Descripción[/]")

                    # (COMPROBACIÓN) Revisión de variable estado acordado con los parámetros de valores permitidos
                    while True:
                        state = Prompt.ask("  [#7CCA62]>[/] [white]Estado[/]")
                        if state not in ['Activo', 'Inactivo']:
                            tema_advertencia.print("[ESTADO INVÁLIDO \u274C ] Debe ser 'Activo' o 'Inactivo'.\n", style="error")
                        else: break

                    #(ADVERTENCIA) Se advierte al administrador si desea realizar cambios en la base de datos
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea dar de alta esta categoría en el sistema? S/N", style="advice")
                    opcion = input("Opcion: ").upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            categoria.nombre = name if name else categoria.nombre
                            categoria.descripcion = description if description else categoria.descripcion
                            categoria.estado = state if state else categoria.estado
                            db.commit()

                            registrar_auditoria(
                                db,
                                id_usuario=ID,
                                entidad="Categoría",
                                operacion="Modificación",
                                descripcion=f"Actualización de categoría '{Categorias.id_categoria}': nombre='{name}', descripción='{description}', estado='{state}'"
                            )
                            db.commit()
                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha modificado la categoría correctamente.\n", style="success")
                        
                        else: tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")

                    elif opcion == 'N': tema_advertencia.print("\n[INFORMACIÓN \u2139] Se interrumpio la operación.\n", style="info")

                    else:tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")

                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")

        elif opcion == '3':
            menu = Panel(
                "[bold green]Gestión de Categorías[/]\n"
                "\n"
                "  [1] [white]Desactivar categoría[/]\n"
                "  [2] [white]Reactivar categoría[/]\n"
                "  [3] [white]Regresar al menú principal[/]",
                title="[bold #7CCA62]SUBMENÚ DE ESTADO DE CATEGORÍAS[/]",
                subtitle="Administración de alta y baja", style="#7CCA62", width=60
            )

            while True:
                print(menu)
                opcion = input("\nSeleccione una opción: ")

                if opcion == "1":
                    title = Panel("DESACTIVAR CATEGORÍA", style="bold red", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        categorias_lista = db.query(Categorias).filter(Categorias.estado == "Activo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)

                            while True:
                                categoria_id = Prompt.ask("  [red]>[/] [white]Ingrese el ID de la categoría que desea desactivar[/] [red](‘?’ para ver lista)[/]")
                                if categoria_id == '?':
                                    table= lista_cat(categorias_lista)
                                    print(table)
                                    continue

                                categoria = db.query(Categorias).filter(Categorias.id_categoria == categoria_id, Categorias.estado == "Activo").first()
                                if not categoria:
                                    tema_advertencia.print("[ERROR \u274C ] No existe una categoría activa con ese ID. Intente de nuevo.\n", style="error")
                                else:
                                    break

                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea desactivar esta categoría? S/N", style="advice")
                            confirmar = input("Opcion: ").upper()
                            if confirmar == 'S':
                                adm_contraseña = Prompt.ask("  [red]>[/] [white]Digite su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    categoria.estado = "Inactivo"
                                    db.commit()

                                    # Auditoría
                                    registrar_auditoria(
                                        db,
                                        id_usuario=ID,
                                        entidad="Categoría",
                                        operacion="Baja",
                                        descripcion=f"Desactivación de la categoría '{categoria.id_categoria}': nombre='{categoria.nombre}', descripción='{categoria.descripcion}', estado='{categoria.estado}'"
                                    )
                                    db.commit()

                                    tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] La categoría ha sido desactivada.\n", style="success")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")
                            elif confirmar == 'N':
                                tema_advertencia.print("\n[INFORMACIÓN \u2139] Se canceló la operación.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente.\n", style="error")
                        else:
                            tema_advertencia.print("[ERROR \u274C ] No se encontró el usuario.\n", style="error")

                elif opcion == "2":
                    title = Panel("REACTIVAR CATEGORÍA", style="bold #7CCA62", width=50)
                    with obtener_session() as db:
                        usuario = informacion_usuario(db, ID)
                        categorias_lista = db.query(Categorias).filter(Categorias.estado == "Inactivo").all()

                        if usuario:
                            contraseña = usuario.contraseña
                            print(title)

                            
                            while True:
                                categoria_id = Prompt.ask("  [green]>[/] [white]Ingrese el ID de la categoría a reactivar[/] [green](‘?’ para ver lista)[/]")
                                if categoria_id == '?':
                                    table= lista_cat(categorias_lista)
                                    print(table)
                                    continue

                                categoria = db.query(Categorias).filter(Categorias.id_categoria == categoria_id, Categorias.estado == "Inactivo").first()
                                if not categoria:
                                    tema_advertencia.print("[ERROR \u274C ] No se encontró una categoría inactiva con ese ID. Intenta nuevamente.\n", style="error")
                                else:
                                    break

                            tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea reactivar esta categoría? S/N", style="advice")
                            confirmar = input("Opción: ").upper()

                            if confirmar == 'S':
                                adm_contraseña = Prompt.ask("  [green]>[/] [white]Confirme su contraseña[/]", password=True)
                                if validar_contraseña(adm_contraseña, contraseña):
                                    categoria.estado = "Activo"
                                    db.commit()

                                    # Auditoría
                                    registrar_auditoria(
                                        db,
                                        id_usuario=ID,
                                        entidad="Categoría",
                                        operacion="Alta",
                                        descripcion=f"Reactivación de la categoría '{categoria.id_categoria}': nombre='{categoria.nombre}', descripción='{categoria.descripcion}', estado='{categoria.estado}'"
                                    )
                                    db.commit()

                                    tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] La categoría fue reactivada correctamente.\n", style="success")
                                else:
                                    tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intente de nuevo.\n", style="error")
                            elif confirmar == 'N':
                                tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                            else:
                                tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")
                        else:
                            tema_advertencia.print("[ERROR \u274C ] Usuario no encontrado en la base de datos.\n", style="error")

                elif opcion == "3":
                    break
                else:
                    tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Seleccione una opción válida.\n", style="error")

        elif opcion == '4':
            title = Panel("LISTA DE CATEGORÍAS", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                categorias_lista = db.query(Categorias).all()
                if categorias_lista:
                    table= lista_cat(categorias_lista)                    
                    print(title)
                    print(table)
                    print("\n")
                    
                else: tema_advertencia.print("[ERROR \u274C ] Aún no se han incluido categorias en el sistema.\n", style="error")
       
        elif opcion == '5':
            tema_advertencia.print("Regresando el menú principal... \n", style="advice")
            break

        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")   

# [4] FUNCIÓN ADM. MOSTRAR INVENTARIO DE PRODUCTOS
def show_inventary():
    title = Panel("INVENTARIO", style="bold #7CCA62", width=50)
    with obtener_session() as db:
        inventario = db.query(Inventarios).all()
        if inventario:
            table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")

            # Se definen las cabeceras de la tabla
            table.add_column("No.")
            table.add_column("Id Producto")
            table.add_column("Nombre")
            table.add_column("Categoria")
            table.add_column("Cantidad")
            table.add_column("Cantidad minima")
            table.add_column("Estado")

            # Instrucción para llenar las filas de la tabla
            for inv in inventario:
                id_producto = inv.id_producto
                producto = db.query(Productos).filter(Productos.id_producto == id_producto).first()
                id_categoria = producto.id_categoria 
                categoria = db.query(Categorias).filter(Categorias.id_categoria == id_categoria).first()

                table.add_row(str(inv.id_inventario), producto.id_producto, producto.nombre, categoria.nombre, str(inv.cantidad), str(inv.cantidad_min), inv.estado)
            
            print(title)
            print(table)
            print("\n")
            
        else: tema_advertencia.print("[ERROR \u274C ] Aún no se han incluido productos en el sistema.\n", style="error")

# [5] SUBMENÚ ADM. CONSULTAR ALERTAS
def adm_submenu_alerta(ID):
    title = Panel("PRODUCTOS CON STOCK BAJO", style="bold #7CCA62", width=50)
    with obtener_session() as db:
        inventario = db.query(Inventarios).all()
        if inventario:
            table = Table(show_header=True, header_style="bold #7CCA62", border_style="#7CCA62")

            # Se definen las cabeceras de la tabla
            table.add_column("No.")
            table.add_column("Id Producto")
            table.add_column("Nombre")
            table.add_column("Categoria")
            table.add_column("Cantidad")
            table.add_column("Cantidad minima")
            table.add_column("Estado")

            # Bandera para que no se repita el mensaje de advertencia la misma cantidad de veces que productos que hay en el inventario
            hay_stock_bajo = False  
            # Instrucción para llenar las filas de la tabla
            for inv in inventario:
                if inv.cantidad < inv.cantidad_min:
                    hay_stock_bajo = True  # Al menos un producto con stock bajo
                    id_producto = inv.id_producto
                    producto = db.query(Productos).filter(Productos.id_producto == id_producto).first()
                    id_categoria = producto.id_categoria 
                    categoria = db.query(Categorias).filter(Categorias.id_categoria == id_categoria).first()

                    table.add_row(str(inv.id_inventario), producto.id_producto, producto.nombre, categoria.nombre, str(inv.cantidad), str(inv.cantidad_min), inv.estado)
                    print(title)
                    print(table)
            if not hay_stock_bajo:
                tema_advertencia.print("\n[ADVERTENCIA ⚠ ] No hay productos por debajo del stock\n", style="advice")
            
            print("\n")
            
        else: tema_advertencia.print("[ERROR \u274C ] Aún no se han incluido productos en el sistema.\n", style="error")

# [6] SUBMENÚ ADM. REVISAR MOVIMIENTOS
def adm_submenu_movimientos(ID):
    submenu_movimientos = Panel(""
        "\n"
        "[bold]Movimientos[/]\n"
        "  [1] [white]Movimientos generales[/]\n"
        "  [2] [white]Movimientos por administrador[/]\n"
        "[bold]Modificaciones[/]\n"
        "  [3] [white]Modificaciones de Productos[/]\n"
        "  [4] [white]Modificaciones de Categorías[/]\n"
        "  [5] [white]Modificaciones de Proveedores[/]\n"
        "  [6] [white]Modificaciones de Empleados[/]\n"
        "  [7] [white]Regresar[/]\n",
        title="[bold #0BD0D9][ REVISAR MOVIMIENTOS ][/]", subtitle="Análisis de compras y ventas", style="#0BD0D9", width=50)

    while True:
        print(submenu_movimientos)
        opcion = input("\nSeleccione una opción: ")

        with obtener_session() as db:
            if opcion == '1' :
                auditorias = db.query(Auditorias).all()
                mostrar_auditorias(auditorias)

            elif opcion == '2':
                # Obtener la lista de administradores
                administradores = db.query(Usuarios).filter(Usuarios.rol == "Administrador").all()

                # (TABLA) Mostrar tabla de administradores
                table = lista_admin(administradores)
                
                while True:
                    admin_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el ID del administrador[/] [#7CCA62](oprima '?' para consultar lista)[/]")
                    if admin_id == "?":
                        print(table)
                    elif admin_id not in [admin.id_usuario for admin in administradores]:
                        tema_advertencia.print("[ERROR \u274C ] No existe ningún administrador con ese ID. Intente de nuevo.\n", style="error")
                    else:
                        break

                auditorias = db.query(Auditorias).filter(Auditorias.id_usuario == admin_id).all()
                mostrar_auditorias(auditorias)

            elif opcion == '3':
                auditorias = db.query(Auditorias).filter(Auditorias.entidad == "Producto").all()
                mostrar_auditorias(auditorias)

            elif opcion == '4':
                auditorias = db.query(Auditorias).filter(Auditorias.entidad == "Categoría").all()
                mostrar_auditorias(auditorias)

            elif opcion == '5':
                auditorias = db.query(Auditorias).filter(Auditorias.entidad == "Proveedor").all()
                mostrar_auditorias(auditorias)

            elif opcion == '6':
                auditorias = db.query(Auditorias).filter(Auditorias.entidad == "Empleado").all()
                mostrar_auditorias(auditorias)

            elif opcion == '7':
                tema_advertencia.print("Regresando al menú principal...\n", style="advice")
                break

            else:
                tema_advertencia.print("[OPCIÓN INCORRECTA ❌] Intenta nuevamente\n", style="error")

# [7] SUBMENÚ ADM. CONSULTAR REPORTE DE VENTAS
def adm_submenu_reporteVen():    
    submenu_reporteVen = Panel(""
        "\n"
        "[1] [white]Reporte general[/]\n"
        "[2] [white]Reporte por empleado[/]\n"
        "[3] [white]Regresar[/]\n",
        title="[bold #0BD0D9][ CONSULTAR REPORTE DE VENTAS ][/]", subtitle="Análisis de compras y ventas", style="#0BD0D9", width=50)

    while True:
        print(submenu_reporteVen)
        opcion = input("\nSeleccione una opción: ")

        with obtener_session() as db:
            if opcion == "1":
                ventas = db.query(Ventas).join(Ventas.movimiento).all()
                if ventas:
                    table = Table(title="Reporte general de Ventas", show_header=True, header_style="bold cyan")
                    table.add_column("ID Venta")
                    table.add_column("ID Empleado")
                    table.add_column("Fecha")
                    table.add_column("Total")

                    for venta in ventas:
                        table.add_row(
                            str(venta.id_venta),
                            str(venta.movimiento.id_usuario),
                            str(venta.movimiento.fecha),
                            f"${venta.movimiento.total:.2f}"
                        )

                    print(table)
                else:
                    tema_advertencia.print("No hay ventas registradas.\n", style="info")

            elif opcion == "2":
                empleados = db.query(Usuarios).filter(Usuarios.rol == "Empleado").all()

                table = lista_emp(empleados)

                while True:
                    emp_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el ID del empleado[/] [#7CCA62](oprima '?' para consultar lista)[/]")
                    if emp_id == "?":
                        print(table)
                    elif emp_id not in [emp.id_usuario for emp in empleados]:
                        tema_advertencia.print("[ERROR \u274C ] No existe ningún empleado con ese ID. Intente de nuevo.\n", style="error")
                    else:
                        break

                ventas = db.query(Ventas).join(Ventas.movimiento).filter(Movimientos.id_usuario == emp_id).all()

                if ventas:
                    table = Table(title=f"Reporte de ventas por empleado {emp_id}", show_header=True, header_style="bold yellow")
                    table.add_column("ID Venta")
                    table.add_column("Fecha")
                    table.add_column("Total")

                    for venta in ventas:
                        table.add_row(
                            str(venta.id_venta),
                            str(venta.movimiento.fecha),
                            f"${venta.movimiento.total:.2f}"
                        )

                    print(table)
                else:
                    tema_advertencia.print("No se encontraron ventas para ese empleado.\n", style="info")

            elif opcion == "3":
                tema_advertencia.print("Regresando al menú principal...\n", style="advice")
                break

            else:
                tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# [8] SUBMENÚ ADM. CONSULTAR REPORTE DE COMPRAS
def adm_submenu_reporteCom():
    submenu_reporteCom = Panel(""
        "\n"
        "[1] [white]Reporte general[/]\n"
        "[2] [white]Reporte por administrador[/]\n"
        "[3] [white]Regresar[/]\n",
        title="[bold #0BD0D9][ CONSULTAR REPORTE DE COMPRAS ][/]", subtitle="Análisis de compras y ventas", style="#0BD0D9", width=50)
    
    while True:
        print(submenu_reporteCom)
        opcion = input("\nSeleccione una opción: ")

        with obtener_session() as db:
            if opcion == "1":
                compras = db.query(Compras).join(Compras.movimiento).join(Compras.proveedor).all()
                
                if compras:
                    table = Table(title="Reporte General de Compras", show_header=True, header_style="bold magenta")
                    table.add_column("ID Compra")
                    table.add_column("ID Admin")
                    table.add_column("Fecha")
                    table.add_column("Total")
                    table.add_column("ID Producto")
                    table.add_column("Empresa Proveedor")

                    for compra in compras:
                        table.add_row(
                            str(compra.id_compra),
                            str(compra.movimiento.id_usuario),
                            str(compra.movimiento.fecha),
                            f"${compra.movimiento.total:.2f}",
                            str(compra.movimiento.id_producto),
                            compra.proveedor.empresa
                        )

                    print(table)
                else:
                    tema_advertencia.print("No hay compras registradas.\n", style="info")

            elif opcion == "2":
                administradores = db.query(Usuarios).filter(Usuarios.rol == "Administrador").all()

                table = lista_admin(administradores)
                while True:
                    admin_id = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el ID del administrador[/] [#7CCA62](oprima '?' para consultar lista)[/]")
                    if admin_id == "?":
                        print(table)
                    elif admin_id not in [admin.id_usuario for admin in administradores]:
                        tema_advertencia.print("[ERROR \u274C ] No existe ningún administrador con ese ID. Intente de nuevo.\n", style="error")
                    else:
                        break

                compras = db.query(Compras).join(Compras.movimiento).join(Compras.proveedor).filter(Movimientos.id_usuario == admin_id).all()

                if compras:
                    table = Table(title=f"Reporte de Compras por Administrador {admin_id}", show_header=True, header_style="bold green")
                    table.add_column("ID Compra")
                    table.add_column("Fecha")
                    table.add_column("Total")
                    table.add_column("ID Producto")
                    table.add_column("Empresa Proveedor")

                    for compra in compras:
                        table.add_row(
                            str(compra.id_compra),
                            str(compra.movimiento.fecha),
                            f"${compra.movimiento.total:.2f}",
                            str(compra.movimiento.id_producto),
                            compra.proveedor.empresa
                        )

                    print(table)
                else:
                    tema_advertencia.print("No se encontraron compras para ese administrador.\n", style="info")

            elif opcion == "3":
                tema_advertencia.print("Regresando al menú principal...\n", style="advice")
                break

            else:
                tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# [9] SUBMENÚ ADM. GESTIÓN DE EMPLEADOS
def adm_submenu_empleado(ID):
    submenu_empleado = Panel(""
    "\n"
    "[1] [white]Agregar empleado[/]\n"
    "[2] [white]Modificar rol del empleado[/]\n"
    "[3] [white]Cambiar estado de empleados[/]\n"
    "[4] [white]Listar empleados[/]\n"
    "[5] [white]Regresar[/]\n",
    title="[bold #0BD0D9][ GESTIÓN DE EMPLEADOS ][/]", subtitle="Administración de empleados y roles", style="#0BD0D9", width=50)
    while True:
        print(submenu_empleado)
        opcion = input("\nSeleccione una opción: ")
        if opcion == '1':
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                if usuario:
                    contraseña = usuario.contraseña
                    title = Panel("AGREGAR EMPLEADO", style="bold #7CCA62", width=50)
                    print(title)

                    # Generación automática de ID
                    id = generar_nuevo_id(db, Usuarios, "id_usuario", prefijo="USER", ceros=3)
                    tema_advertencia.print(f"[INFO \u2139 ] ID generado automáticamente: {id}\n", style="info")

                    # === VALIDACIONES DE CAMPOS ===
                    while True:
                        name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre(s)[/]").strip()
                        if not name:
                            tema_advertencia.print("[CAMPO VACÍO ❌ ] El nombre no puede estar vacío.\n", style="error")
                        elif any(char.isdigit() for char in name):
                            tema_advertencia.print("[ERROR ❌ ] El nombre no debe contener números.\n", style="error")
                        else:
                            break

                    while True:
                        last_name = Prompt.ask("  [#7CCA62]>[/] [white]Apellido(s)[/]").strip()
                        if not last_name:
                            tema_advertencia.print("[CAMPO VACÍO ❌ ] El apellido no puede estar vacío.\n", style="error")
                        elif any(char.isdigit() for char in last_name):
                            tema_advertencia.print("[ERROR ❌ ] El apellido no debe contener números.\n", style="error")
                        else:
                            break

                    while True:
                        rol = Prompt.ask("  [#7CCA62]>[/] [white]Rol ('Administrador' o 'Empleado')[/]").strip().capitalize()
                        if rol not in ['Administrador', 'Empleado']:
                            tema_advertencia.print("[ROL INVÁLIDO ❌ ] Debe ser 'Administrador' o 'Empleado'.\n", style="error")
                        else:
                            break

                    while True:
                        workstation = Prompt.ask("  [#7CCA62]>[/] [white]Puesto[/]").strip()
                        if not workstation:
                            tema_advertencia.print("[CAMPO VACÍO ❌ ] El puesto no puede estar vacío.\n", style="error")
                        else:
                            break

                    while True:
                        phone = Prompt.ask("  [#7CCA62]>[/] [white]Teléfono (10 dígitos)[/]").strip()
                        if not phone:
                            tema_advertencia.print("[CAMPO VACÍO ❌ ] El teléfono no puede estar vacío.\n", style="error")
                        elif not phone.isdigit():
                            tema_advertencia.print("[FORMATO INVÁLIDO ❌ ] El teléfono debe contener solo números.\n", style="error")
                        elif len(phone) != 10:
                            tema_advertencia.print("[LONGITUD INCORRECTA ❌ ] El teléfono debe tener exactamente 10 dígitos.\n", style="error")
                        else:
                            break

                    while True:
                        try:
                            salary = float(Prompt.ask("  [#7CCA62]>[/] [white]Salario[/]").strip())
                            if salary < 0:
                                tema_advertencia.print("[VALOR INVÁLIDO ❌ ] El salario no puede ser negativo.\n", style="error")
                            else:
                                break
                        except ValueError:
                            tema_advertencia.print("[ERROR ❌ ] El salario debe ser un número válido.\n", style="error")

                    while True:
                        user = Prompt.ask("  [#7CCA62]>[/] [white]Usuario[/]").strip()
                        if not user:
                            tema_advertencia.print("[CAMPO VACÍO ❌ ] El usuario no puede estar vacío.\n", style="error")
                            continue
                        user_existente = db.query(Usuarios).filter(Usuarios.usuario == user).first()
                        if user_existente:
                            tema_advertencia.print("[USUARIO NO DISPONIBLE ❌ ] El usuario ya está en uso. Pruebe de nuevo.\n", style="error")
                        else:
                            break

                    while True:
                        password = Prompt.ask("  [#7CCA62]>[/] [white]Contraseña[/]", password=True).strip()
                        if not password:
                            tema_advertencia.print("[CONTRASEÑA VACÍA ❌ ] La contraseña no puede estar vacía.\n", style="error")
                        elif len(password) < 4:
                            tema_advertencia.print("[CONTRASEÑA DÉBIL ❌ ] Debe contener al menos 4 caracteres.\n", style="error")
                        else:
                            break

                    tema_advertencia.print("\n[ADVERTENCIA ⚠ ] ¿Desea dar de alta al nuevo usuario? S/N", style="advice")
                    opcion = input("Opcion: ").strip().upper()
                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password=True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            with obtener_session() as db:
                                usuario_nuevo = Usuarios(
                                    id_usuario=id,
                                    nombres=name,
                                    apellidos=last_name,
                                    rol=rol,
                                    puesto=workstation,
                                    telefono=phone,
                                    salario=salary,
                                    usuario=user,
                                    contraseña=bcrypt.hash(password),
                                    estado="Activo"
                                )
                                db.add(usuario_nuevo)
                                db.commit()
                                registrar_auditoria(
                                    db=db,
                                    operacion="Alta",
                                    entidad="Empleado",
                                    id_usuario=ID,
                                    descripcion=f"Se dio de alta al empleado '{usuario_nuevo.nombres} {usuario_nuevo.apellidos}' con puesto '{usuario_nuevo.puesto}' y salario ${usuario_nuevo.salario:.2f}."
                                )
                                tema_advertencia.print("[OPERACIÓN EXITOSA ✅ ] Se dio de alta al nuevo usuario.\n", style="success")
                        else:
                            tema_advertencia.print("[CREDENCIALES INCORRECTAS ❌ ] Intente de nuevo.\n", style="error")
                    elif opcion == 'N':
                        tema_advertencia.print("[OPERACIÓN CANCELADA ℹ ] Se interrumpió la operación.\n", style="info")
                    else:
                        tema_advertencia.print("[OPCIÓN INCORRECTA ❌ ] Intente nuevamente.\n", style="error")
                else:
                    tema_advertencia.print("[ERROR ❌ ] No existe el usuario en la base de datos.\n", style="error")

        elif opcion == '2':
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                if usuario:
                    id_usuario = usuario.id_usuario
                    contraseña = usuario.contraseña
                    title = Panel("MODIFICAR ROL DE EMPLEADO", style="bold #7CCA62", width=50)
                    print(title)
                    
                    # (COMPROBACIÓN) Se comprueba si el usuario existe en la base de datos y si el id no es el mismo del que esta en sesión
                    while True:
                        id_user = Prompt.ask("  [#7CCA62]>[/] [white]Ingrese el identificador del empleado[/]")
                        datos_usuario = informacion_usuario(db, id_user)
                        if datos_usuario == None:
                            tema_advertencia.print("[ID INVÁLIDO \u274C ] No existe un usuario con ese identificador. Intenta nuevamente.\n", style="error")
                            continue
                        elif id_user == id_usuario:
                            tema_advertencia.print("[ID INVÁLIDO \u274C ] No puedes cambiar tu propio rol. Otro administrador debe hacerlo.\n", style="error")
                            continue
                        break
                    # ( COMPROBACIÓN) Revisa si el rol ingresado cumple con los parametros establecidos 'Empleado' o 'Administrador'
                    while True:
                        Rol = Prompt.ask("  [#7CCA62]>[/] [white]Rol[/]")
                        if Rol not in ['Administrador', 'Empleado']:
                            tema_advertencia.print("[ROL INVÁLIDO \u274C ] Debe ser 'Administrador' o 'Empleado'.\n", style="error")
                        else: break
                    
                    Puesto = Prompt.ask("  [#7CCA62]>[/] [white]Puesto[/]")
                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea modificar el rol del usuario? S/N", style="advice")
                    opcion = input("Opcion: ").upper()

                    if opcion == 'S':
                        adm_contraseña = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(adm_contraseña, contraseña):
                            datos_usuario.rol = Rol if Rol else datos_usuario.rol
                            datos_usuario.puesto = Puesto if Puesto else datos_usuario.puesto
                            db.commit()
                            # Después de agregar el nuevo empleado y hacer commit en la sesión
                            registrar_auditoria(
                                db=db,
                                operacion="Modificación",
                                entidad="Empleado",
                                id_usuario=ID,  # ID del usuario que hace la modificación (ej. el administrador logueado)
                                descripcion=f"Se modificó el rol del empleado '{datos_usuario.nombres} {datos_usuario.apellidos}' a Rol: '{datos_usuario.rol}', Puesto: '{datos_usuario.puesto}'."
                            )


                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha actualizado el rol del usuario\n", style="success")
                        else:
                            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] No se han realizado cambios.\n", style="error")
                    
                    elif opcion == 'N':tema_advertencia.print("[INFORMACIÓN \u2139] La actualización de datos ha sido cancelada.\n", style="info")
                    
                    else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente\n", style="error")
                      
                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos.\n", style="error")
        elif opcion == '3':
            with obtener_session() as db:
                usuario = informacion_usuario(db,ID)
                if usuario:
                    id_usuario = usuario.id_usuario
                    contraseña = usuario.contraseña
                    menu = Panel(
                        "[bold green]Gestión de Empleados[/]\n"
                        "\n"
                        "  [1] [white]Dar de baja empleado[/]\n"
                        "  [2] [white]Dar de alta empleado[/]\n"
                        "  [3] [white]Regresar al menú principal[/]",
                        title="[bold #7CCA62]SUBMENÚ DE ESTADO DE EMPLEADOS[/]",
                        subtitle="Administración de alta y baja", style="#7CCA62", width=60
                    )

                    while True:
                        print(menu)
                        opcion = input("\nSeleccione una opción: ")

                        if opcion == "1":
                            title = Panel("BAJA DE EMPLEADO", style="bold #FF5555", width=50)
                            with obtener_session() as db:
                                admin = informacion_usuario(db, ID)
                                empleados_activos = db.query(Usuarios).filter(Usuarios.estado == "Activo").all()

                                if admin:
                                    contraseña = admin.contraseña
                                    print(title)

                                    while True:
                                        id_emp = Prompt.ask("  [red]>[/] [white]Ingrese el ID del empleado a desactivar[/] [red](oprima '?' para ver lista)[/]")
                                        empleados_ids = {u.id_usuario for u in empleados_activos}

                                        if id_emp == '?':
                                            print(lista_usuarios(empleados_activos))
                                        elif id_emp == ID:
                                            tema_advertencia.print("[ID INVÁLIDO \u274C ] No puedes darte de baja a ti mismo.\n", style="error")
                                        elif id_emp not in empleados_ids:
                                            tema_advertencia.print("[ERROR \u274C ] No existe un usuario activo con ese ID.\n", style="error")
                                        else:
                                            break

                                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea desactivar este empleado? S/N", style="advice")
                                    confirm = input("Opción: ").upper()

                                    if confirm == 'S':
                                        adm_contraseña = Prompt.ask("  [red]>[/] [white]Confirme su contraseña[/]", password=True)
                                        if validar_contraseña(adm_contraseña, contraseña):
                                            empleado = db.query(Usuarios).filter(Usuarios.id_usuario == id_emp).first()
                                            empleado.estado = "Inactivo"
                                            db.commit()

                                            registrar_auditoria(
                                                db=db,
                                                operacion="Baja",
                                                entidad="Empleado",
                                                id_usuario=ID,
                                                descripcion=f"Se dio de baja al empleado '{empleado.nombres} {empleado.apellidos}' con puesto '{empleado.puesto}' y salario ${empleado.salario:.2f}."
                                            )

                                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El empleado ha sido desactivado correctamente.\n", style="success")
                                        else:
                                            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta de nuevo.\n", style="error")
                                    elif confirm == 'N':
                                        tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                                    else:
                                        tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")
                                else:
                                    tema_advertencia.print("[ERROR \u274C ] No se encontró el usuario.\n", style="error")

                        elif opcion == "2":
                            title = Panel("REACTIVAR EMPLEADO", style="bold #7CCA62", width=50)
                            with obtener_session() as db:
                                admin = informacion_usuario(db, ID)
                                empleados_inactivos = db.query(Usuarios).filter(Usuarios.estado == "Inactivo").all()

                                if admin:
                                    contraseña = admin.contraseña
                                    print(title)
                                    table = lista_usuarios(empleados_inactivos)

                                    while True:
                                        id_emp = Prompt.ask("  [green]>[/] [white]Ingrese el ID del empleado a reactivar[/] [green](oprima '?' para ver lista)[/]")
                                        empleados_ids = {u.id_usuario for u in empleados_inactivos}

                                        if id_emp == '?':
                                            print(table)
                                        elif id_emp not in empleados_ids:
                                            tema_advertencia.print("[ERROR \u274C ] No existe un usuario inactivo con ese ID.\n", style="error")
                                        else:
                                            break

                                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Desea reactivar este empleado? S/N", style="advice")
                                    confirm = input("Opción: ").upper()

                                    if confirm == 'S':
                                        adm_contraseña = Prompt.ask("  [green]>[/] [white]Confirme su contraseña[/]", password=True)
                                        if validar_contraseña(adm_contraseña, contraseña):
                                            empleado = db.query(Usuarios).filter(Usuarios.id_usuario == id_emp).first()
                                            empleado.estado = "Activo"
                                            db.commit()

                                            registrar_auditoria(
                                                db=db,
                                                operacion="Alta",
                                                entidad="Empleado",
                                                id_usuario=ID,
                                                descripcion=f"Se dio de alta al empleado '{empleado.nombres} {empleado.apellidos}' con puesto '{empleado.puesto}' y salario ${empleado.salario:.2f}."
                                            )

                                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] El empleado fue reactivado correctamente.\n", style="success")
                                        else:
                                            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta de nuevo.\n", style="error")
                                    elif confirm == 'N':
                                        tema_advertencia.print("\n[OPERACIÓN CANCELADA \u2139] No se realizaron cambios.\n", style="info")
                                    else:
                                        tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Intente nuevamente.\n", style="error")
                                else:
                                    tema_advertencia.print("[ERROR \u274C ] No se encontró el usuario.\n", style="error")

                        elif opcion == "3":
                            tema_advertencia.print("\n[INFORMACIÓN \u2139] Regresando al menú principal...\n", style="info")
                            break
                        else:
                            tema_advertencia.print("[OPCIÓN INVÁLIDA \u274C ] Seleccione una opción válida.\n", style="error")
        elif opcion == '4':
            title = Panel("LISTA DE EMPLEADOS", style="bold #7CCA62", width=50)
            with obtener_session() as db:
                usuarios_lista = db.query(Usuarios).filter(Usuarios.estado == "Activo").all()
                if usuarios_lista:
                    table = lista_usuarios(usuarios_lista)
                    print(title)
                    print(table)
                    print("\n")
                
                else: 
                    tema_advertencia.print("[ERROR \u274C ] No existe ningún usuario en la base de datos.\n", style="error")
        elif opcion == '5':
            tema_advertencia.print("Regresando el menú principal... \n", style="advice")
            break
        else: 
            tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# [10] SUBMENÚ ADM. EDITAR PERFIL
def adm_submenu_perfil(ID):
    submenu_perfil = Panel(""
    "\n"
    "[1] [white]Modificar datos personales[/]\n"
    "[2] [white]Cambiar usuario y contraseña[/]\n"
    "[3] [white]Regresar[/]\n",
    title="[bold #0BD0D9][ EDITAR PERFIL ][/]", subtitle="Ajustes de cuenta", style="#0BD0D9", width=50)
    while True:
        print(submenu_perfil)
        opcion = input("\nSeleccione una opción: ")
        if opcion == '1':
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                if usuario:
                    contraseña = usuario.contraseña
                    title = Panel("MODIFICAR DATOS PERSONALES", style="bold #7CCA62", width=50)
                    print(title)
                    name = Prompt.ask("  [#7CCA62]>[/] [white]Nombre(s)[/]")
                    last_name = Prompt.ask("  [#7CCA62]>[/] [white]Apellidos(s)[/]")
                    phone = Prompt.ask("  [#7CCA62]>[/] [white]Telefono[/]")

                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Está seguro de que desea actualizar los datos de su perfil? S/N", style="advice")
                    opcion = input("Opcion: ").upper()

                    if opcion == 'S':
                        password = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(password, contraseña):
                            usuario.nombres = name if name else usuario.nombres
                            usuario.apellidos = last_name if last_name else usuario.apellidos
                            usuario.telefono = phone if phone else usuario.telefono
                            db.commit()
                            registrar_auditoria(db,ID,'Empleado', 'Modificación',f'Se cambiaron los datos personales del usuario {usuario.id_usuario} ({usuario.nombres})')
                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha actualizado tu perfil", style="success")
                        else:
                            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] No se han realizado cambios.", style="error")
                    elif opcion == 'N':
                        tema_advertencia.print("[INFORMACIÓN \u2139] La actualización de datos ha sido cancelada.", style="info")
                    else:
                        tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente", style="error")
                else:
                    tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos", style="error")

        elif opcion == '2':
            with obtener_session() as db:
                usuario = informacion_usuario(db, ID)
                if usuario:
                    contraseña = usuario.contraseña
                    title = Panel("CAMBIAR USUARIO Y CONTRASEÑA", style="bold #7CCA62", width=50)
                    print(title)
                    user = Prompt.ask("  [#7CCA62]>[/] [white]Nuevo usuario[/]")
                    new_password = Prompt.ask("  [#7CCA62]>[/] [white]Nueva contraseña[/]")

                    tema_advertencia.print("\n[ADVERTENCIA \u26A0 ] ¿Está seguro de que desea actualizar los datos de su perfil? S/N", style="advice")
                    opcion = input("Opcion: ").upper()

                    if opcion == 'S':
                        password = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password = True)
                        if validar_contraseña(password, contraseña):
                            usuario.usuario = user if user else usuario.usuario
                            usuario.contraseña = new_password if new_password else usuario.contraseña
                            db.commit()
                            registrar_auditoria(db,ID,'Empleado', 'Modificación',f'Se cambio el usuario y contraseña del usuario {usuario.id_usuario} ({usuario.nombres})')
                            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Se ha actualizado tu perfil", style="success")
                        else:
                            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] No se han realizado cambios.", style="error")
                    elif opcion == 'N':
                        tema_advertencia.print("[INFORMACIÓN \u2139] La actualización de datos ha sido cancelada.", style="info")
                    else:
                        tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intente nuevamente", style="error")
                else: tema_advertencia.print("[ERROR \u274C ] No existe el usuario en la base de datos", style="error")

        elif opcion == '3':
            tema_advertencia.print("Regresando el menú principal... \n", style="advice")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# << SUBMENÚS DEL MENÚ DE EMPLEADO >>
# [1] SUBMENÚ EMP. HACER VENTAS
def menu_venta_empleado(ID_empleado):
    carrito = []
    total_venta = 0

    while True:
        with SessionLocal() as db:
            id_producto = Prompt.ask("[bold cyan]Ingresa el ID del producto ('?' para ver inventario)[/]").strip()
            if id_producto == "?":
                show_inventary()
                continue

            producto = db.query(Productos).filter(Productos.id_producto == id_producto, Productos.estado == "Activo").first()
            if not producto:
                print("[bold red]Producto no encontrado o inactivo.[/]")
                continue

            inventario = db.query(Inventarios).filter(Inventarios.id_producto == id_producto).first()
            if not inventario or inventario.cantidad <= 0:
                print("[bold red]No hay stock disponible para este producto.[/]")
                continue

            while True:
                try:
                    cantidad = int(Prompt.ask(f"[bold cyan]¿Cuántas unidades quieres vender? (Disponible: {inventario.cantidad})[/]"))
                    if 0 < cantidad <= inventario.cantidad:
                        break
                    else:
                        print("[bold red]Cantidad inválida.[/]")
                except ValueError:
                    print("[bold red]Ingresa un número válido.[/]")

            subtotal = cantidad * producto.precio_unitario
            total_venta += subtotal
            carrito.append({
                'id_producto': id_producto,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio_unitario': producto.precio_unitario,
                'subtotal': subtotal
            })

            respuesta = Prompt.ask("[bold yellow]¿Deseas agregar otro producto? (S/N)[/]").strip().upper()
            if respuesta == "S":
                continue
            elif respuesta == "N":
                break
            else:
                print("[bold red]Respuesta inválida. Volviendo al menú principal...[/]")
                return

    # Mostrar resumen
    table = Table(title="[bold green]Resumen de Venta[/]", show_lines=True)
    table.add_column("Producto", style="cyan")
    table.add_column("Cantidad", style="magenta")
    table.add_column("Precio Unitario", style="green")
    table.add_column("Subtotal", style="yellow")

    for item in carrito:
        table.add_row(item['nombre'], str(item['cantidad']), f"${item['precio_unitario']:.2f}", f"${item['subtotal']:.2f}")

    print(table)
    print(f"[bold green]Total de la venta: ${total_venta:.2f}[/]")

    confirmar = Prompt.ask("[bold cyan]¿Deseas realizar esta venta? (S/N)[/]").strip().upper()
    if confirmar == "S":
        pass
    elif confirmar == "N":
        print("[bold yellow]Venta cancelada. Regresando al menú principal...[/]")
        return
    else:
        print("[bold red]Respuesta inválida. Regresando al menú principal...[/]")
        return

    contraseña = Prompt.ask("[bold cyan]Confirma tu contraseña[/]", password=True)

    with SessionLocal() as db:
        usuario = db.query(Usuarios).filter(Usuarios.id_usuario == ID_empleado).first()
        if usuario and bcrypt.verify(contraseña,usuario.contraseña):
            # Obtener cliente
            clientes_lista = db.query(Clientes).filter(Clientes.estado == "Activo").all()
            cliente_ids = {cliente.id_cliente for cliente in clientes_lista}

            # Mostrar tabla si el usuario ingresa '?'
            while True:
                id_cliente = Prompt.ask("[bold cyan]Ingresa el ID del cliente (CLI_001 si es público en general, '?' para ver clientes)[/]").strip()
                
                if not id_cliente:
                    id_cliente = "CLI_001"
                    break

                elif id_cliente == '?':
                    # Mostrar tabla de clientes
                    table = Table(title="Clientes Registrados", style="cyan")
                    table.add_column("ID Cliente", style="bold white")
                    table.add_column("Nombres", style="bold green")
                    table.add_column("Apellidos", style="bold green")

                    for cliente in clientes_lista:
                        table.add_row(cliente.id_cliente, cliente.nombres, cliente.apellidos)

                    print(table)

                elif id_cliente not in cliente_ids:
                    tema_advertencia.print("[ERROR \u274C ] No existe ningún cliente con ese ID. Intente de nuevo o ingrese '?'\n", style="error")

                else:
                    break

            for item in carrito:
                movimiento = Movimientos(
                    id_usuario=ID_empleado,
                    id_producto=item['id_producto'],
                    descripcion="Venta de producto",
                    cantidad=item['cantidad'],
                    subtotal=item['subtotal'],
                    impuesto=round(item['subtotal'] * 0.16, 2),
                    total=round(item['subtotal'] * 1.16, 2),
                    fecha=datetime.now(),
                    tipo="Venta",
                    estado="Activo"
                )
                db.add(movimiento)
                db.commit()
                db.refresh(movimiento)

                venta = Ventas(
                    id_movimiento=movimiento.id_movimiento,
                    id_cliente=id_cliente
                )
                db.add(venta)

                inventario = db.query(Inventarios).filter(Inventarios.id_producto == item['id_producto']).first()
                if inventario:
                    inventario.cantidad -= item['cantidad']

            db.commit()
            print("[bold green]¡Venta realizada exitosamente![/]")
        else:
            print("[bold red]Contraseña incorrecta. Venta cancelada.[/]")
            return

        

# [2] SUBMENÚ EMP. REPORTE DE VENTAS
def reporte_ventas_empleado(ID_empleado):
    with obtener_session() as db:
        # Buscar los movimientos de tipo 'Venta' realizados por el empleado
        movimientos = db.query(Movimientos).filter(
            Movimientos.id_usuario == ID_empleado,
            Movimientos.tipo == 'Venta'
        ).all()

        if not movimientos:
            print("[bold yellow]No has realizado ventas aún.[/]")
            return

        table = Table(title="[bold green]Reporte de Ventas - Mis Ventas[/]", show_lines=True)
        table.add_column("ID Venta", style="cyan", justify="center")
        table.add_column("Fecha", style="magenta", justify="center")
        table.add_column("Cliente", style="yellow", justify="center")
        table.add_column("Total", style="green", justify="center")

        total_general = 0

        for movimiento in movimientos:
            venta = movimiento.venta
            if venta:  # Confirmar que existe una venta ligada al movimiento
                fecha_formateada = movimiento.fecha.strftime("%d/%m/%Y")
                nombre_cliente = venta.cliente.nombres + " " + venta.cliente.apellidos
                table.add_row(
                    str(venta.id_venta),
                    fecha_formateada,
                    nombre_cliente,
                    f"${movimiento.total:.2f}"
                )
                total_general += movimiento.total

        print(table)
        print(f"[bold green]Total acumulado de ventas: ${total_general:.2f}[/]")

# [3] SUBMENÚ EMP. EDITAR PERFIL
def editar_perfil_empleado(ID_empleado):
    submenu_perfil = Panel(""
    "\n"
    "[1] [white]Modificar usuario[/]\n"
    "[2] [white]Modificar teléfono[/]\n"
    "[3] [white]Cambiar contraseña[/]\n"
    "[4] [white]Regresar[/]", title="[bold #0BD0D9][ EDITAR PERFIL ][/]", subtitle="Ajustes de cuenta", style="#0BD0D9", width=50)

    while True:
        print(submenu_perfil)
        opcion = input("\nSeleccione una opción: ")

        with obtener_session() as db:
            usuario = informacion_usuario(db, ID_empleado)
            if not usuario:
                tema_advertencia.print("[ERROR ❌ ] No existe el usuario en la base de datos", style="error")
                return

            contraseña = usuario.contraseña

            if opcion in ['1', '2']:
                if opcion == '1':
                    nuevo_dato = Prompt.ask("  [#7CCA62]>[/] [white]Nuevo usuario[/]")
                    atributo = 'usuario'
                elif opcion == '2':
                    nuevo_dato = Prompt.ask("  [#7CCA62]>[/] [white]Nuevo número de teléfono[/]")
                    atributo = 'telefono'

                tema_advertencia.print("\n[ADVERTENCIA ⚠ ] ¿Está seguro de que desea realizar el cambio? S/N", style="advice")
                confirmar = input("Opcion: ").upper()

                if confirmar == 'S':
                    password = Prompt.ask("  [#7CCA62]>[/] [white]Digite su contraseña[/]", password=True)
                    if validar_contraseña(password, contraseña):
                        dato_anterior = getattr(usuario, atributo)
                        setattr(usuario, atributo, nuevo_dato if nuevo_dato else dato_anterior)
                        db.commit()
                        # Registro en auditoría
                        registrar_auditoria(db, ID_empleado, "Usuarios", f"Modificación de {atributo}", f"{atributo} antes: {dato_anterior}, después: {nuevo_dato}")
                        tema_advertencia.print("[OPERACIÓN EXITOSA ✔ ] Se han actualizado los datos", style="success")
                    else:
                        tema_advertencia.print("[CREDENCIALES INCORRECTAS ❌ ] No se han realizado cambios.", style="error")
                elif confirmar == 'N':
                    tema_advertencia.print("[INFORMACIÓN ℹ] La actualización fue cancelada.", style="info")
                else:
                    tema_advertencia.print("[OPCIÓN INCORRECTA ❌ ] Intente nuevamente.", style="error")

            elif opcion == '3':
                tema_advertencia.print("\n[ADVERTENCIA ⚠ ] ¿Está seguro de que desea cambiar la contraseña? S/N", style="advice")
                confirmar = input("Opcion: ").upper()

                if confirmar == 'S':
                    actual = Prompt.ask("  [#7CCA62]>[/] [white]Contraseña actual[/]", password=True)
                    if validar_contraseña(actual, contraseña):
                        nueva = Prompt.ask("  [#7CCA62]>[/] [white]Nueva contraseña[/]", password=True)
                        repetir = Prompt.ask("  [#7CCA62]>[/] [white]Repite la nueva contraseña[/]", password=True)
                        if nueva == repetir:
                            usuario.contraseña = nueva
                            db.commit()

                            # Registro en auditoría
                            registrar_auditoria(db, ID_empleado, "Usuarios", "Cambio de contraseña", "El usuario actualizó su contraseña")
                            tema_advertencia.print("[OPERACIÓN EXITOSA ✔ ] Contraseña actualizada.", style="success")
                        else:
                            tema_advertencia.print("[ERROR ❌ ] Las contraseñas no coinciden. No se realizaron cambios.", style="error")
                    else:
                        tema_advertencia.print("[CREDENCIALES INCORRECTAS ❌ ] Contraseña incorrecta.", style="error")
                elif confirmar == 'N':
                    tema_advertencia.print("[INFORMACIÓN ℹ] El cambio de contraseña fue cancelado.", style="info")
                else:
                    tema_advertencia.print("[OPCIÓN INCORRECTA ❌ ] Intente nuevamente.", style="error")

            elif opcion == '4':
                tema_advertencia.print("Regresando al menú principal... \n", style="advice")
                break
            else:
                tema_advertencia.print("[OPCIÓN INCORRECTA ❌ ] Intenta nuevamente \n", style="error")


# << FUNCIONES CON LA BASE DE DATOS >>
# [A] CONEXIÓN CON LA BASE DE DATOS
# [ANOTACIÓN]
    # La función "obtener_session" se utiliza para gestionar la conexión con la base de datos. Utiliza un context manager para garantizar 
    # que la sesión se inicie y cierre correctamente. Al entrar en el contexto, se crea una nueva sesión con "SessionLocal". Al salir del 
    # contexto, se asegura que la sesión se cierre correctamente, incluso si ocurre un error durante su uso.
@contextmanager
def obtener_session():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# [B] FUNCIÓN PARA VALIDAR LA SESIÓN
# [ANOTACIÓN]
    #La función "validar_sesion" recibe como parámetros la base de datos, el nombre de usuario, la contraseña y el rol. Realiza una consulta 
    # a la tabla "Usuarios" para verificar si existe un usuario que coincida con los tres parámetros (usuario, contraseña y rol). 
    # Si encuentra una coincidencia, devuelve el objeto del usuario; de lo contrario, devuelve None.
def validar_sesion(db, usuario_input, contraseña_input, rol_requerido, estado_requerido="Activo"):
    # Buscar por nombre de usuario únicamente
    usuario = db.query(Usuarios).filter(
        Usuarios.usuario == usuario_input,
        Usuarios.rol == rol_requerido,
        Usuarios.estado == estado_requerido
    ).first()

    # Verificar contraseña si encontró el usuario
    if usuario and bcrypt.verify(contraseña_input, usuario.contraseña):
        return usuario
    else:
        return None
# [C] FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO
# [ANOTACIÓN]
    #La función "informacion_usuario" recibe como parámetros la base de datos y el id. Realiza una consulta a la tabla "Usuarios" para verificar 
    # si existe un usuario que coincida con los parámetros. Si encuentra una coincidencia, devuelve el objeto del usuario; de lo contrario, devuelve None.
def informacion_usuario(db, id):
    usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id).first()
    return usuario

# << FUNCIONES DE INICIO DE SESION >>
# [A] FUNCIÓN PARA MOSTRAR EL MENÚ DE INICIO DE SESIÓN
def login_menu():
    while True:
        print(menu_login)
        opcion = input("\nSeleccione una opción: ")
        if opcion == '1':
            adm_session()
            continue
        elif opcion == '2':
            emp_session()
            continue
        elif opcion == '3':
            cli_session()
            continue
        elif opcion == '4':
            registrar_cliente()
            continue
        elif opcion == '5':
            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Ha salido de la aplicación \n", style="success")
            break
        else: tema_advertencia.print("[OPCIÓN INCORRECTA \u274C ] Intenta nuevamente \n", style="error")

# [B] FUNCIÓN PARA OBTENER LA SESION DEL ADMINISTRADOR Y MOSTRAR SU MENÚ
def adm_session():
    # [ANOTACIÓN]
        # Se crea un panel utilizando la librería "rich", y luego se imprime en consola junto con dos sentencias "Prompt.ask", que son funciones de dicha 
        # librería para solicitar al usuario el ingreso de datos. Estas sentencias también permiten diseñar el mensaje que se muestra en consola, indicando 
        # qué tipo de información debe ingresar el usuario. Se emplea un valor de "True" para ocultar la contraseña durante el ingreso de datos.
    title = Panel("INICIO DE SESIÓN", style="bold #7CCA62", width=50)
    print(title)
    usuario = Prompt.ask("   [#7CCA62]>[/] [white]Usuario[/]")
    contraseña = Prompt.ask("   [#7CCA62]>[/] [white]Contraseña[/]", password=True)

    with obtener_session() as db:
      # [ANOTACIÓN] 
            # La variable "inicio_de_sesion" almacena la información del usuario al momento de iniciar sesión. Primero, la función "validar_sesion" verifica 
            # si el usuario existe en el sistema. Si la validación es exitosa, los datos del usuario se guardan en la variable. En caso contrario, se muestra 
            # un mensaje de error indicando que la autenticación ha fallado.
        
        inicio_sesion = validar_sesion(db, usuario, contraseña, "Administrador", "Activo")
        
        if inicio_sesion:
            id = inicio_sesion.id_usuario
            nombre = inicio_sesion.nombres
            apellido = inicio_sesion.apellidos
            rol = inicio_sesion.rol
            puesto = inicio_sesion.puesto
            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Ha iniciado sesión correctamente \n", style="success")
            adm_menu(id,nombre,apellido,rol,puesto)
            return True
        else:
            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta nuevamente \n", style="error")
            return False

# [C] FUNCIÓN PARA OBTENER LA SESION DEL EMPLEADO Y MOSTRAR SU MENÚ
def emp_session():
    # [ANOTACIÓN]
        # Se crea un panel utilizando la librería "rich", y luego se imprime en consola junto con dos sentencias "Prompt.ask", que son funciones de dicha 
        # librería para solicitar al usuario el ingreso de datos. Estas sentencias también permiten diseñar el mensaje que se muestra en consola, indicando 
        # qué tipo de información debe ingresar el usuario. Se emplea un valor de "True" para ocultar la contraseña durante el ingreso de datos.
    title = Panel("INICIO DE SESIÓN", style="bold #7CCA62", width=50)
    print(title)
    usuario = Prompt.ask("   [#7CCA62]>[/] [white]Usuario[/]")
    contraseña = Prompt.ask("   [#7CCA62]>[/] [white]Contraseña[/]", password=True)
    with obtener_session() as db:
        # [ANOTACIÓN] 
            # La variable "inicio_de_sesion" almacena la información del usuario al momento de iniciar sesión. Primero, la función "validar_sesion" verifica 
            # si el usuario existe en el sistema. Si la validación es exitosa, los datos del usuario se guardan en la variable. En caso contrario, se muestra 
            # un mensaje de error indicando que la autenticación ha fallado.
        inicio_sesion = validar_sesion(db, usuario, contraseña, "Empleado", "Activo")
        
        if inicio_sesion:
            id = inicio_sesion.id_usuario
            nombre = inicio_sesion.nombres
            apellido = inicio_sesion.apellidos
            rol = inicio_sesion.rol
            puesto = inicio_sesion.puesto
            tema_advertencia.print("[OPERACIÓN EXITOSA \u2714 ] Ha iniciado sesión correctamente \n", style="success")
            emp_menu(id,nombre,apellido,rol,puesto)
            return True
        else:
            tema_advertencia.print("[CREDENCIALES INCORRECTAS \u274C ] Intenta nuevamente \n", style="error")
            return False

# [D] FUNCIÓN PARA OBTENER LA SESION DEL CLIENTE Y MOSTRAR SU MENÚ
# ============================= SUBMENÚ CLIENTE ============================= #
def cli_session():
    title = Panel("INICIAR SESIÓN CLIENTE", style="bold #0BD0D9", width=50)
    print(title)
    with obtener_session() as db:
        usuario = Prompt.ask("  [#0BD0D9]>[/] [white]Ingresa tu usuario[/]")
        contraseña = Prompt.ask("  [#0BD0D9]>[/] [white]Ingresa tu contraseña[/]", password=True)
        clientes = db.query(Clientes).filter_by(usuario=usuario).first()

        if clientes and bcrypt.verify(contraseña,clientes.contraseña):
            tema_advertencia.print(f"\n[OPERACIÓN EXITOSA \u2714 ] ¡Bienvenido {clientes.nombres}!\n", style="success")
            cliente_menu(clientes)
        else:
            tema_advertencia.print("\n[ERROR \u274C ] Cliente no encontrado. Intenta de nuevo.\n", style="error")
# Función que contiene el menú del cliente
def cliente_menu(cliente):
    carrito = []
    while True:
        menu_cliente = Panel("""       
        [1] Comprar productos
        [2] Ver mis pedidos
        [3] Ver perfil
        [4] Cerrar sesión
        """, title="[bold cyan]MENÚ DEL CLIENTE[/bold cyan]", subtitle="Gestor de ventas", style="#0BD0D9", width=50)
        print("\n")
        print(menu_cliente)
        opcion = Prompt.ask("Selecciona una opción")

        if opcion == "1": cliente_comprar(cliente, carrito)
        elif opcion == "2": cliente_ver_pedidos(cliente)
        elif opcion == "3": cliente_ver_perfil(cliente)
        elif opcion == "4":
            tema_advertencia.print("Se ha cerrado sesión correctamente.\n", style="success")
            break
        else:
            tema_advertencia.print("Opcion incorrecta, Intenta de nuevo\n", style="error")


# ============================= FUNCIONES CLIENTE =============================

# [1] Función para comprar desde el perfil de cliente
def cliente_comprar(cliente, carrito):
    total_compra = 0

    while True:
        with obtener_session() as db:
            termino = Prompt.ask("\n  [#0BD0D9]>[/] [white]Buscar producto por nombre (o escribe '?' para ver todo el inventario)[/]").strip()
            if termino == "?":
                productos = db.query(Productos).filter(Productos.estado == "Activo").all()
            else:
                productos = db.query(Productos).filter(Productos.nombre.ilike(f"%{termino}%"), Productos.estado == "Activo").all()

            if not productos:
                tema_advertencia.print("No se encontraron productos.", style="error")
                continue

            table = Table(title="[bold green]Productos Encontrados[/]", show_header=True, header_style="bold cyan")
            table.add_column("ID", style="magenta")
            table.add_column("Nombre", style="white")
            table.add_column("Precio", justify="right", style="green")
            table.add_column("Stock", justify="right", style="yellow")

            for p in productos:
                inv = db.query(Inventarios).filter_by(id_producto=p.id_producto).first()
                stock = inv.cantidad if inv else 0
                table.add_row(p.id_producto, p.nombre, f"${p.precio_unitario:.2f}", str(stock))

            print(table)

            respuesta = Prompt.ask("[bold yellow]¿Deseas agregar un producto al carrito? (S/N)[/]").strip().upper()
            if respuesta == "S":
                pass  # continúa con el flujo
            elif respuesta == "N":
                tema_advertencia.print("Operación cancelada. Volviendo al menú principal...", style="warning")
                return
            else:
                tema_advertencia.print("Respuesta inválida. Regresando al menú principal.", style="error")
                return

            id_prod = Prompt.ask("ID del producto").strip()
            prod = db.query(Productos).filter_by(id_producto=id_prod, estado="Activo").first()
            inv = db.query(Inventarios).filter_by(id_producto=id_prod).first()

            if not prod or not inv or inv.cantidad <= 0:
                tema_advertencia.print("Producto inválido o sin stock.", style="error")
                continue

            while True:
                try:
                    cantidad = int(Prompt.ask(f"¿Cuántas unidades deseas? (Disponible: {inv.cantidad})"))
                    if 0 < cantidad <= inv.cantidad:
                        break
                    else:
                        tema_advertencia.print("Cantidad inválida.", style="warning")
                except ValueError:
                    tema_advertencia.print("Ingresa un número válido.", style="warning")

            subtotal = cantidad * prod.precio_unitario
            carrito.append((prod, cantidad))
            total_compra += subtotal
            tema_advertencia.print(f"{cantidad}x {prod.nombre} agregado al carrito.", style="success")

            respuesta = Prompt.ask("[bold yellow]¿Deseas agregar otro producto? (S/N)[/]").strip().upper()
            if respuesta == "S":
                continue
            elif respuesta == "N":
                break
            else:
                tema_advertencia.print("Respuesta inválida. Regresando al menú principal.", style="error")
                return

    if not carrito:
        tema_advertencia.print("No hay productos en el carrito.", style="warning")
        return

    resumen = Table(title="[bold green]Resumen de Compra[/]", show_lines=True)
    resumen.add_column("Producto", style="cyan")
    resumen.add_column("Cantidad", justify="center", style="magenta")
    resumen.add_column("Precio Unitario", justify="right", style="green")
    resumen.add_column("Subtotal", justify="right", style="yellow")

    for p, c in carrito:
        resumen.add_row(p.nombre, str(c), f"${p.precio_unitario:.2f}", f"${p.precio_unitario * c:.2f}")

    print(resumen)
    print(f"[bold green]Total de la compra: ${total_compra:.2f}[/]")

    respuesta = Prompt.ask("[bold cyan]¿Confirmar la compra? (S/N)[/]").strip().upper()
    if respuesta == "S":
        pass
    elif respuesta == "N":
        tema_advertencia.print("Compra cancelada. Volviendo al menú principal...", style="warning")
        return
    else:
        tema_advertencia.print("Respuesta inválida. Regresando al menú principal.", style="error")
        return

    # Registrar la venta
    with obtener_session() as db:
        for p, c in carrito:
            subtotal = p.precio_unitario * c
            impuesto = round(subtotal * 0.16, 2)
            total = round(subtotal + impuesto, 2)

            movimiento = Movimientos(
                id_usuario=cliente.id_cliente,
                id_producto=p.id_producto,
                descripcion="Venta al cliente",
                cantidad=c,
                subtotal=subtotal,
                impuesto=impuesto,
                total=total,
                fecha=datetime.now(),
                tipo="Venta",
                estado="Activo"
            )
            db.add(movimiento)
            db.commit()
            db.refresh(movimiento)

            venta = Ventas(id_movimiento=movimiento.id_movimiento, id_cliente=cliente.id_cliente)
            db.add(venta)

            inv = db.query(Inventarios).filter_by(id_producto=p.id_producto).first()
            if inv:
                inv.cantidad -= c

        db.commit()
        carrito.clear()
        tema_advertencia.print("¡Compra realizada con éxito!", style="success")

# [2] Función para ver los pedidos desde el menú del cliente
def cliente_ver_pedidos(cliente):
    with obtener_session() as db:
        ventas = db.query(Ventas).filter_by(id_cliente=cliente.id_cliente).all()
        if ventas:
            table = Table(title="Mis Pedidos", show_header=True, header_style="bold green")
            table.add_column("ID Venta")
            table.add_column("Producto")
            table.add_column("Cantidad")
            table.add_column("Total")
            table.add_column("Estado")

            for v in ventas:
                mov = db.query(Movimientos).filter_by(id_movimiento=v.id_movimiento).first()
                prod = db.query(Productos).filter_by(id_producto=mov.id_producto).first()
                table.add_row(str(v.id_venta), prod.nombre, str(mov.cantidad), f"${mov.total:.2f}", mov.estado)
            print(table)
        else:
            tema_advertencia.print("No tienes pedidos registrados.", style="info")

# [3] Función para ver el perfil del cliente desde el menú de cliente
def cliente_ver_perfil(cliente):
    perfil = Panel(f"""
    Nombre: {cliente.nombres} {cliente.apellidos}
    Teléfono: {cliente.telefono}
    Dirección: {cliente.direccion}
    Email: {cliente.email}
    Estado: {cliente.estado}
    """, title="[bold cyan]Mi Perfil[/bold cyan]", style="bold blue", width=50)
    print(perfil)


# FUNCIÓN PRINCIPAL
login_menu()



'''

Color azul rey #0F6FC6
Color azul claro #009DD9
Color aqua #0BD0D9
Color menta #10CF9B
Color verde #7CCA62

'''