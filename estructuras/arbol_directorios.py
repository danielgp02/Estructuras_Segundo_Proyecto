class NodoSistemaArchivos:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.padre = None
        
class Archivo(NodoSistemaArchivos):
    def __init__(self, nombre, contenido=""):
        super().__init__(nombre, "archivo")
        self.contenido = contenido
    
class Carpeta(NodoSistemaArchivos):
    def __init__(self, nombre):
        super().__init__(nombre, "carpeta")
        self.hijos = []
    
    def agregar_hijo(self, nodo):
        nodo.padre = self
        self.hijos.append(nodo)