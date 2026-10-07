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
    
    def buscar_hijo_directo(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre ==nombre:
                return hijo
        return None

class ArbolDirectorios:
    def __init__(self):
        self.raiz = Carpeta("/")
    
    def _navegar(self, ruta):
        if ruta.strip() in ("", "/"):
            return self.raiz
        partes = [p for p in ruta.strip("/").split("/") if p]
        actual = self.raiz
        for parte in partes:
            if actual.tipo == "carpeta":
                return None
            siguente = actual.buscar_hijo_directo(parte)
            if siguente is None:
                return None
            actual = siguente
        return actual
    
    
            
                