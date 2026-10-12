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
        """Inserta un usuario o actualiza su contraseña si ya existe."""
        indice = self._funcion_hash(usuarios)
        bucket = self.table[indice]

        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                bucket[i] = (usuarios, contraseña)
                return
        bucket.append((usuarios, contraseña))
        self.cantidad += 1

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