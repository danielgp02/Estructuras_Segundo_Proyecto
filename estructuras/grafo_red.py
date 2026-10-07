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
