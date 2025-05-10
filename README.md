# Sistema de Gestión de Inventarios para una PyME

Este es un sistema de gestión de inventarios diseñado para adaptarse a cualquier PyME que maneje productos físicos. Permite un control organizado del inventario, registro de operaciones clave y generación de reportes que facilitan la toma de decisiones estratégicas.

---

##  Características Principales

- Gestión de productos, categorías, proveedores y empleados (altas, bajas y modificaciones)
- Control de stock con entradas (compras) y salidas (ventas)
- Módulo de registro y validación de clientes y proveedores
- Inicio de sesión con control de roles (administrador y empleado)
- Modificación de roles y perfiles (solo administradores)
- Auditoría de acciones importantes
- Visualización clara y estructurada de datos con la librería `Rich`
- Validación de correos electrónicos al registrar clientes/proveedores

---

##  Tecnologías Utilizadas

- **Lenguaje:** Python  
- **Base de datos:** SQL  
- **ORM:** SQLAlchemy  
- **Visualización en consola:** Rich  
- **Otras librerías:**
  - `datetime`, `re`, `contextlib`
  - Módulo interno: `database_V3_1.py` (modelo de datos y sesión)

---

## Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- Python 3.10 o superior
- Gestor de paquetes `pip` (viene con Python)
- (Opcional) Un entorno de desarrollo como VS Code

---

## Instalación de Dependencias

Instala las dependencias necesarias ejecutando en la terminal:

```bash
pip install rich sqlalchemy
```

---

## Modo de Uso

> **IMPORTANTE:** Antes de ejecutar el sistema principal, primero debes ejecutar el archivo de configuración de la base de datos.

1. Ejecuta el archivo de la base de datos:
   ```bash
   python database_V3_1.py
   ```

2. Luego ejecuta el archivo principal del sistema:
   ```bash
   python main.py
   ```

---

## Funcionalidades Futuras

- Migración de la interfaz a una versión web o menú interactivo gráfico (opcional)
- Implementación de reportes exportables (PDF, Excel)
- Mejoras en la experiencia del usuario

---

##  Equipo de Desarrollo

- **Scrum Master:** Cerón Urbina Itzel Anaid  
- **Product Owner:** Ríos Olivares Cesar Antonio  
- **Desarrolladores:**  
  - Cameras Hidalgo Arturo  
  - Eduardo Arturo Campillo López  
  - Ernesto Rojas Pérez  
  - Paola Carolina Gonzales Pérez  
  - Wendy Nicole Luna Colula  
  - Jhoana Yamile Alonso Aldrete  

---

## Licencia

Este proyecto aún no cuenta con una licencia definida

---

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas colaborar:

1. Haz un fork del repositorio
2. Crea una rama (`git checkout -b feature/nueva-feature`)
3. Realiza tus cambios
4. Haz commit y push (`git push origin feature/nueva-feature`)
5. Crea un Pull Request para revisión

---
