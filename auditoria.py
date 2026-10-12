from datetime import datetime

class auditoria:
    def __init__(self, ruta_archivo="Network_audit_log.txt"):
        self.ruta_archivo = ruta_archivo

    def registrar_evento(self, detalle):
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        linea = f":{marca_tiempo} - {detalle}\n"

        with open(self.ruta_archivo, "a") as archivo:
            archivo.write(linea)

        return linea

    def leer_log(self):
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()

        except FileNotFoundError:
            return "Todavia no existe el registro de auditoria."

        if not contenido:
            return "El registro de auditoria esta vacio."

        return "------ Registro de auditoria ---\n" + contenido + "------ Fin del registro de auditoria ---"


if __name__ == "__main__":
    auditoria = auditoria()

    auditoria.registrar_evento("Se ha iniciado la auditoria.")
    auditoria.registrar_evento("Se ha ejecutado una operacion.")

    print(auditoria.leer_log())
