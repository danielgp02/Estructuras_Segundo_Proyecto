from estructuras.grafo_red import GrafoRed
from servidor import Servidor
from auditoria import Auditoria


class NetworkOS:
    def __init__(self):
        self.grafo = GrafoRed()
        self.servidores = {}  # nombre -> Servidor
        self.auditoria = Auditoria()
        
    def crear_servidor(self, nombre):
        if nombre in self.servidores:
            print(f"El servidor '{nombre}' ya existe.")
            return
        self.servidores[nombre] = Servidor(nombre)
        self.grafo.agregar_servidor(nombre)
        self.auditoria.registrar(f"Servidor '{nombre}' creado.")
        print(f"Servidor '{nombre}' creado.")

    def _pedir_servidor(self, mensaje="Nombre del servidor: "):
        nombre = input(mensaje).strip()
        if nombre not in self.servidores:
            print(f"El servidor '{nombre}' no existe.")
            return None
        return self.servidores[nombre]