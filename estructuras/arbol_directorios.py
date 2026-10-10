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
    
    def _ruta_completa(self, nodo):
        partes = []
        actual = nodo
        while actual is not None and actual.padre is not None:
            partes.insert(0, actual.nombre)
            actual = actual.padre
        return "/" + "/".join(partes)  # Exclude the root's name
    
            
    def crear_carpeta(self, ruta_padre, nombre_nueva):
        padre = self._navegar(ruta_padre)
        if padre is None or padre.tipo != "carpeta":
            return False, f"La ruta '{ruta_padre}' no existe o no es una carpeta."
        if padre.buscar_hijo_directo(nombre_nueva) is not None:
            return False, f"Ya existe un elemento llamado '{nombre_nueva}' en '{ruta_padre}'."
        padre.agregar_hijo(Carpeta(nombre_nueva))
        return True, f"Carpeta '{nombre_nueva}' creada en '{ruta_padre}'."
                
                
    def crear_archivo(self, ruta_padre, nombre_nuevo, contenido=""):
        padre = self._navegar(ruta_padre)
        if padre is None or padre.tipo != "carpeta":
            return False, f"La ruta '{ruta_padre}' no existe o no es una carpeta."
        if padre.buscar_hijo_directo(nombre_nuevo) is not None:
            return False, f"Ya existe un elemento llamado '{nombre_nuevo}' en '{ruta_padre}'."
        padre.agregar_hijo(Archivo(nombre_nuevo, contenido))
        return True, f"Archivo '{nombre_nuevo}' creado en '{ruta_padre}'."
    
    def buscar(self, nombre, nodo=None):
         if nodo is None:
            nodo = self.raiz
         if nodo.nombre == nombre:
             return self._ruta_completa(nodo)
         if nodo.tipo == "carpeta":
             for hijo in nodo.hijos:
                 resultado = self.buscar(nombre, hijo)
                 if resultado is not None:
                     return resultado
         return None
     
    def eliminar(self, ruta):
        nodo = self._navegar(ruta)
        if nodo is None or nodo.padre is None:
            return False, f"La ruta '{ruta}' no existe o es la raíz."
        eliminados =self._eliminar_subarbol(nodo)
        nodo.padre.hijos.remove(nodo)
        return True, f"Elemento '{nodo.nombre}' y sus {eliminados} elementos hijos eliminados de '{self._ruta_completa(nodo.padre)}'."