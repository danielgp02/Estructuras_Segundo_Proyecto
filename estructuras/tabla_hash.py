class tabla_hash:
    """Tabla hash con manejo de colisiones por encadenamiento.

    Almacena pares (usuario, contraseña). Permite registrar,
    consultar y eliminar usuarios de forma eficiente.
    """

    def __init__(self, capacidad=101):
        self.capacidad = capacidad
        # Cada posicion es una lista (bucket) para manejar colisiones.
        self.table = [[] for _ in range(capacidad)]
        self.cantidad = 0

    def _funcion_hash(self, clave):
        """Convierte una clave en un indice valido de la tabla."""
        primo = 31
        hash_value = 0
        for char in str(clave):
            hash_value = (hash_value * primo + ord(char)) % self.capacidad
        return hash_value

    def insert(self, usuarios, contraseña):
        """Registra un usuario.

        Si el usuario ya existe, actualiza su contraseña.
        Si no, lo agrega al bucket e incrementa el contador.
        """
        indice = self._funcion_hash(usuarios)
        bucket = self.table[indice]

        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                bucket[i] = (usuarios, contraseña)
                return
        bucket.append((usuarios, contraseña))
        self.cantidad += 1

    def get(self, usuarios):
        """Devuelve la contraseña del usuario, o None si no existe."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for u, contraseña in bucket:
            if u == usuarios:
                return contraseña
        return None

    def remove(self, usuarios):
        """Elimina el usuario. Devuelve True si se elimino, False si no existe."""
        bucket = self.table[self._funcion_hash(usuarios)]
        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                del bucket[i]
                self.cantidad -= 1
                return True
        return False