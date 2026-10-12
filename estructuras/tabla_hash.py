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

    def insert(self, key, value):
        index = self._funcion_hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
        self.cantidad += 1

    def get(self, key):
        index = self._funcion_hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def remove(self, key):
        index = self._funcion_hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.cantidad -= 1
                return True
        return False