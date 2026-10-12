from datetime import datetime

class auditoria:
    def __init__(self, ruta_archivo= "Network_audit_log.txt"):
        self.ruta_archivo = ruta_archivo

    def registrar_evento(self, detalle):
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        linea = f":{marca_tiempo} - {detalle}\n"

        with open(self.ruta_archivo, "a") as archivo:
            archivo.write(linea)

        return linea