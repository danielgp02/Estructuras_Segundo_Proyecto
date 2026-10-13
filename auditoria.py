from datetime import datetime


class Auditoria:
    """Gestor de registro de auditoría que escribe eventos en un archivo de log."""

    def __init__(self, ruta_archivo="Network_audit_log.txt"):
        self.ruta_archivo = ruta_archivo

    def registrar_evento(self, detalle):
        """Registra un evento en el log con marca de tiempo y devuelve la línea escrita."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f":{marca_tiempo} - {detalle}\n"

        with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(linea)

        return linea

    def leer_log(self):
        """Devuelve el contenido completo del log formateado para su lectura."""
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
        except FileNotFoundError:
            return "Todavía no existe el registro de auditoría."

        if not contenido:
            return "El registro de auditoría está vacío."

        separador = "------ Registro de auditoría ---"
        return f"{separador}\n{contenido}{separador}"


if __name__ == "__main__":
    registro = Auditoria()

    registro.registrar_evento("Se ha iniciado la auditoría.")
    registro.registrar_evento("Se ha ejecutado una operación.")

    print(registro.leer_log())
