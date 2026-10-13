class TablaHash:
    """Tabla hash con manejo de colisiones por encadenamiento (listas separadas).

    Permite almacenar pares (usuario, contraseña) y resolver colisiones
    guardando varios elementos en la misma posición de la tabla.
    """

    def __init__(self, capacidad=101):
        self.capacidad = capacidad
        self.table = [[] for _ in range(capacidad)]
        self.cantidad = 0

    def _funcion_hash(self, clave):
        """Genera el índice de la tabla para una clave usando hashing polinomial."""
        primo = 31
        hash_value = 0
        for char in str(clave):
            hash_value = (hash_value * primo + ord(char)) % self.capacidad
        return hash_value

    def insertar(self, usuarios, contraseña):
        """Inserta un usuario o actualiza su contraseña si ya existe.
        Devuelve (indice_del_bucket, es_nuevo): es_nuevo es False si solo
        se actualizó la contraseña de un usuario existente."""
        indice = self._funcion_hash(usuarios)
        bucket = self.table[indice]

        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                bucket[i] = (usuarios, contraseña)
                return indice, False
        bucket.append((usuarios, contraseña))
        self.cantidad += 1
        return indice, True

    def obtener(self, usuarios):
        """Devuelve la contraseña asociada al usuario, o None si no existe."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for u, contraseña in bucket:
            if u == usuarios:
                return contraseña
        return None

    def eliminar(self, usuarios):
        """Elimina un usuario. Devuelve True si existía, False en caso contrario."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                del bucket[i]
                self.cantidad -= 1
                return True
        return False

    def buscar(self, usuarios):
        """Verifica si un usuario existe en la tabla. Devuelve True o False."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for u, _c in bucket:
            if u == usuarios:
                return True
        return False

    def autenticar(self, usuarios, contraseña):
        """Autentica un usuario comparando usuario y contraseña. Devuelve True o False."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for u, c in bucket:
            if u == usuarios:
                return c == contraseña
        return False

    def mostrar_tabla(self):
        """Muestra el contenido de la tabla y resalta los buckets con colisiones."""
        print(f"Tabla hash (capacidad: {self.capacidad}, elementos: {self.cantidad})")
        print("-" * 52)
        colisiones = 0
        for indice, bucket in enumerate(self.table):
            if bucket:
                if len(bucket) > 1:
                    colisiones += 1
                    print(f"  [{indice}] {bucket}   <-- COLISION")
                else:
                    print(f"  [{indice}] {bucket}")
        print("-" * 52)
        print(f"Buckets con colision: {colisiones}")


if __name__ == "__main__":
    tabla = TablaHash(capacidad=3)

    print("========== PRUEBA DE TablaHash ==========\n")

    print("[1] Insertar usuarios")
    tabla.insertar("ana", "1234")
    tabla.insertar("bob", "abcd")
    tabla.insertar("carla", "clave1")
    tabla.insertar("daniel", "clave2")
    print("    ana, bob, carla y daniel fueron insertados.\n")

    print("[2] Buscar usuarios")
    print(f"    'ana' existe? -> {tabla.buscar('ana')}")
    print(f"    'zoe' existe? -> {tabla.buscar('zoe')}\n")

    print("[3] Autenticar usuarios")
    print(f"    ana / 1234       -> {tabla.autenticar('ana', '1234')}")
    print(f"    ana / incorrecta -> {tabla.autenticar('ana', 'incorrecta')}")
    print(f"    zoe / cualquiera -> {tabla.autenticar('zoe', 'cualquiera')}\n")

    print("[4] Mostrar la tabla y sus colisiones")
    tabla.mostrar_tabla()
    print()

    print("[5] Eliminar usuario 'bob'")
    print(f"    eliminar('bob') -> {tabla.eliminar('bob')}")
    print(f"    'bob' existe ahora? -> {tabla.buscar('bob')}\n")

    print("[6] Tabla despues de eliminar")
    tabla.mostrar_tabla()