class NodoSistemaArchivos:
    """Nodo base del árbol: representa un elemento del sistema de archivos."""

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.padre = None


class Archivo(NodoSistemaArchivos):
    """Archivo dentro del árbol, puede almacenar contenido textual."""

    def __init__(self, nombre, contenido=""):
        super().__init__(nombre, "archivo")
        self.contenido = contenido


class Carpeta(NodoSistemaArchivos):
    """Carpeta que puede contener múltiples hijos (archivos u otras carpetas)."""

    def __init__(self, nombre):
        super().__init__(nombre, "carpeta")
        self.hijos = []

    def agregar_hijo(self, nodo):
        """Agrega un hijo a la carpeta y actualiza su referencia al padre.

        Devuelve el nodo agregado para permitir encadenar llamadas.
        """
        nodo.padre = self
        self.hijos.append(nodo)
        return nodo