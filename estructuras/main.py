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
    
    def menu_archivos(self):
        servidor = self._pedir_servidor()
        if servidor is None:
            return
        while True:
            print(f"\n--- Sistema de archivos de {servidor.nombre} ---")
            print("1) Crear carpeta")
            print("2) Crear archivo")
            print("3) Buscar")
            print("4) Eliminar (en cascada)")
            print("5) Mostrar árbol")
            print("0) Volver")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                ruta = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre de la nueva carpeta: ")
                ok, msg = servidor.sistema_archivos.crear_carpeta(ruta, nombre)
                print(msg)
                self.auditoria.registrar(f"[{servidor.nombre}] crear_carpeta {ruta}/{nombre} -> {'OK' if ok else 'FALLO'}")
            elif opcion == "2":
                ruta = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre del nuevo archivo: ")
                ok, msg = servidor.sistema_archivos.crear_archivo(ruta, nombre)
                print(msg)
                self.auditoria.registrar(f"[{servidor.nombre}] crear_archivo {ruta}/{nombre} -> {'OK' if ok else 'FALLO'}")
            elif opcion == "3":
                nombre = input("Nombre a buscar: ")
                ruta = servidor.sistema_archivos.buscar(nombre)
                print(f"Encontrado en: {ruta}" if ruta else "No encontrado.")
            elif opcion == "4":
                ruta = input("Ruta a eliminar: ")
                ok, msg = servidor.sistema_archivos.eliminar(ruta)
                print(msg)
                self.auditoria.registrar(f"[{servidor.nombre}] eliminar {ruta} -> {'OK' if ok else 'FALLO'}")
            elif opcion == "5":
                servidor.sistema_archivos.mostrar()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")