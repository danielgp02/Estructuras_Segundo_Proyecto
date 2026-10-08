"""
Módulo: grafo_red.py
Implementa la topología de la red como un Grafo Ponderado no dirigido:
los vértices son servidores y el peso de cada arista es la latencia (ms)
de la conexión de fibra óptica entre dos servidores.

Big-O:
    - agregar/eliminar conexión: O(1)
    - dijkstra: O((V + E) log V) usando una cola de prioridad (heapq)
    - bfs / dfs: O(V + E)
"""

import heapq
from collections import deque


class GrafoRed:
    """Grafo ponderado representado como lista de adyacencia:
    adyacencia = { servidor: { vecino: latencia_ms, ... }, ... }"""

    def __init__(self):
        self.adyacencia = {}

    # ------------------------------------------------------------------ #
    # Gestión de vértices y aristas
    # ------------------------------------------------------------------ #
    def agregar_servidor(self, nombre):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = {}
            return True
        return False

    def agregar_conexion(self, origen, destino, peso):
        if origen not in self.adyacencia or destino not in self.adyacencia:
            return False, "Ambos servidores deben existir antes de conectarlos."
        self.adyacencia[origen][destino] = peso
        self.adyacencia[destino][origen] = peso  # fibra óptica bidireccional
        return True, f"Conexión {origen} <-> {destino} con latencia {peso}ms agregada."

    def eliminar_conexion(self, origen, destino):
        if origen in self.adyacencia and destino in self.adyacencia[origen]:
            del self.adyacencia[origen][destino]
            del self.adyacencia[destino][origen]
            return True
        return False

    # ------------------------------------------------------------------ #
    # Enrutamiento: Dijkstra
    # ------------------------------------------------------------------ #
    def dijkstra(self, origen, destino):
        """Calcula la ruta de menor costo acumulado entre dos servidores.
        Devuelve (ruta_como_lista, costo_total). Si no hay ruta, (None, inf)."""
        if origen not in self.adyacencia or destino not in self.adyacencia:
            return None, float("inf")

        costos_minimos = {nodo: float("inf") for nodo in self.adyacencia}
        costos_minimos[origen] = 0
        anteriores = {nodo: None for nodo in self.adyacencia}
        visitados = set()
        cola_prioridad = [(0, origen)]  # (costo_acumulado, servidor)

        while cola_prioridad:
            costo_actual, actual = heapq.heappop(cola_prioridad)
            if actual in visitados:
                continue
            visitados.add(actual)

            if actual == destino:
                break

            for vecino, peso in self.adyacencia[actual].items():
                nuevo_costo = costo_actual + peso
                if nuevo_costo < costos_minimos[vecino]:
                    costos_minimos[vecino] = nuevo_costo
                    anteriores[vecino] = actual
                    heapq.heappush(cola_prioridad, (nuevo_costo, vecino))

        if costos_minimos[destino] == float("inf"):
            return None, float("inf")

        # Reconstruir la ruta siguiendo los "anteriores" desde el destino
        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.insert(0, nodo)
            nodo = anteriores[nodo]

        return ruta, costos_minimos[destino]

    def simular_envio(self, origen, destino):
        """Imprime el salto por cada nodo de la ruta óptima y el costo total."""
        ruta, costo = self.dijkstra(origen, destino)
        if ruta is None:
            print(f"No existe una ruta entre '{origen}' y '{destino}'.")
            return
        print("Ruta calculada:")
        for i, salto in enumerate(ruta):
            etiqueta = "origen" if i == 0 else ("destino" if i == len(ruta) - 1 else "salto intermedio")
            print(f"  {i}. {salto}  ({etiqueta})")
        print(f"Costo total (latencia acumulada): {costo} ms")

    # ------------------------------------------------------------------ #
    # Diagnóstico: BFS / DFS
    # ------------------------------------------------------------------ #
    def bfs(self, inicio):
        """Recorrido en anchura. Devuelve la lista de servidores alcanzados desde 'inicio'."""
        if inicio not in self.adyacencia:
            return []
        visitados = []
        vistos = {inicio}
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            visitados.append(actual)
            for vecino in self.adyacencia[actual]:
                if vecino not in vistos:
                    vistos.add(vecino)
                    cola.append(vecino)
        return visitados

    def dfs(self, inicio, visitados=None):
        """Recorrido en profundidad, recursivo."""
        if visitados is None:
            visitados = []
        if inicio not in self.adyacencia or inicio in visitados:
            return visitados
        visitados.append(inicio)
        for vecino in self.adyacencia[inicio]:
            if vecino not in visitados:
                self.dfs(vecino, visitados)
        return visitados

    def ping_general(self):
        """'Ping General': recorre el grafo y reporta si todos los servidores
        están comunicados, o cuáles quedan aislados / en una sub-red separada."""
        servidores = list(self.adyacencia.keys())
        if not servidores:
            print("No hay servidores registrados en la red.")
            return

        aislados = [s for s in servidores if not self.adyacencia[s]]
        alcanzados = set(self.bfs(servidores[0]))
        no_alcanzados = [s for s in servidores if s not in alcanzados and s not in aislados]

        if not aislados and not no_alcanzados:
            print("Todos los servidores están comunicados entre sí.")
            return

        if aislados:
            print(f"Servidor(es) aislado(s) (sin ninguna conexión): {', '.join(aislados)}")
        if no_alcanzados:
            print(f"Servidor(es) en una sub-red separada (no llegan a '{servidores[0]}'): {', '.join(no_alcanzados)}")