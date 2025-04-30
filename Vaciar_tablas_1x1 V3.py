# limpiar_auditoria.py

from database import SessionLocal, Usuarios #Cambia el nombre de la tabla para importarla
from rich import print


def limpiar_tabla():
    with SessionLocal() as db:
        db.query(Usuarios).delete() #Cambia el nombre de la tabla para eliminar los registros que hay dentro de ella
        db.commit()
        print("✅ Se han eliminado todos los registros de la tabla.")

if __name__ == "__main__":
    limpiar_tabla()


    
