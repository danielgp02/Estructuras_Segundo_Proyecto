"""
Módulo: servidor.py
Representa un servidor de la red. Cada servidor alberga su PROPIO
sistema de archivos (ArbolDirectorios) y su PROPIA base de datos local
de credenciales (TablaHash) — no se comparten entre servidores.
"""

from estructuras.arbol_directorios import ArbolDirectorios
from estructuras.tabla_hash import TablaHash


class Servidor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.sistema_archivos = ArbolDirectorios()
        self.usuarios = TablaHash()

    def registrar_usuario(self, usuario, contrasena):
        return self.usuarios.insertar(usuario, contrasena)

    def iniciar_sesion(self, usuario, contrasena):
        return self.usuarios.autenticar(usuario, contrasena)