class tabla_hash:
    def __init__(self, capacidad=101):
        self.capacidad = capacidad
        self.table = [[] for _ in range(capacidad)]
        self.cantidad = 0

    def _funcion_hash(self, clave):
        primo = 31
        hash_value = 0
        for char in str(clave):
            hash_value = (hash_value * primo + ord(char)) % self.capacidad
        return hash_value

    def insert(self, usuarios, contraseña):
        indice = self._funcion_hash(usuarios)
        bucket = self.table[indice]

        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                bucket[i] = (usuarios, contraseña)
                return
        bucket.append((usuarios, contraseña))
        self.cantidad += 1

    def get(self, usuarios):
        bucket = self.table[self._funcion_hash(usuarios)]
        for u, contraseña in bucket:
            if u == usuarios:
                return contraseña
        return None

    def remove(self, usuarios):
        bucket = self.table[self._funcion_hash(usuarios)]
        for i, (u, _c) in enumerate(bucket):
            if u == usuarios:
                del bucket[i]
                self.cantidad -= 1
                return True
        return False