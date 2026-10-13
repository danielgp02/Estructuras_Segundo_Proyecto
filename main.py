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
                
    def menu_usuarios(self):
        servidor = self._pedir_servidor()
        if servidor is None:
            return
        while True:
            print(f"\n--- Usuarios de {servidor.nombre} ---")
            print("1) Registrar usuario")
            print("2) Iniciar sesión")
            print("3) Eliminar usuario")
            print("4) Mostrar tabla hash (buckets)")
            print("0) Volver")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                usuario = input("Usuario: ")
                contrasena = input("Contraseña: ")
                indice, _nuevo = servidor.registrar_usuario(usuario, contrasena)
                print(f"Guardado en el bucket #{indice}.")
                self.auditoria.registrar(f"[{servidor.nombre}] registrar_usuario {usuario}")
            elif opcion == "2":
                usuario = input("Usuario: ")
                contrasena = input("Contraseña: ")
                exito = servidor.iniciar_sesion(usuario, contrasena)
                print("Inicio de sesión exitoso." if exito else "Credenciales incorrectas.")
                self.auditoria.registrar(f"[{servidor.nombre}] login {usuario} -> {'EXITOSO' if exito else 'FALLIDO'}")
            elif opcion == "3":
                usuario = input("Usuario: ")
                ok = servidor.usuarios.eliminar(usuario)
                print("Usuario eliminado." if ok else "No existía ese usuario.")
            elif opcion == "4":
                servidor.usuarios.mostrar()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
                
    def menu_red(self):
        while True:
            print("\n--- Topología de red ---")
            print("1) Agregar conexión entre servidores")
            print("2) Eliminar conexión")
            print("3) Simular envío de paquete (Dijkstra)")
            print("4) Ping general (detectar servidores aislados)")
            print("0) Volver")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                origen = input("Servidor origen: ")
                destino = input("Servidor destino: ")
                try:
                    peso = float(input("Latencia (ms): "))
                except ValueError:
                    print("La latencia debe ser un número.")
                    continue
                ok, msg = self.grafo.agregar_conexion(origen, destino, peso)
                print(msg)
                self.auditoria.registrar(f"conexion {origen}-{destino} ({peso}ms) -> {'OK' if ok else 'FALLO'}")
            elif opcion == "2":
                origen = input("Servidor origen: ")
                destino = input("Servidor destino: ")
                ok = self.grafo.eliminar_conexion(origen, destino)
                print("Conexión eliminada." if ok else "No existía esa conexión.")
            elif opcion == "3":
                origen = input("Servidor origen: ")
                destino = input("Servidor destino: ")
                self.grafo.simular_envio(origen, destino)
                self.auditoria.registrar(f"ruta calculada {origen} -> {destino}")
            elif opcion == "4":
                self.grafo.ping_general()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
    
    def menu_principal(self):
        while True:
            print("\n========== NETWORK OS ==========")
            print("1) Crear servidor")
            print("2) Sistema de archivos de un servidor")
            print("3) Usuarios / autenticación de un servidor")
            print("4) Topología y enrutamiento de red")
            print("5) Ver log de auditoría")
            print("0) Salir")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre del nuevo servidor: ")
                self.crear_servidor(nombre)
            elif opcion == "2":
                self.menu_archivos()
            elif opcion == "3":
                self.menu_usuarios()
            elif opcion == "4":
                self.menu_red()
            elif opcion == "5":
                self.auditoria.leer_log()
            elif opcion == "0":
                print("Cerrando Network OS...")
                break
            else:
                print("Opción inválida.")
                
                
if __name__ == "__main__":
    sistema = NetworkOS()
    sistema.menu_principal()