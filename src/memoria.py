"""
memoria.py
==========
Gestor de memoria para RISCO.

Controla:
- profundidad de recursión
- cantidad de variables
- tamaño máximo de listas/matrices
- validación de matrices
- liberación explícita
"""

import gc # Para forzar la recolección de basura después de eliminar referencias
import sys # Para estimar el tamaño en bytes de objetos (opcional, no es exacto pero da una idea)


class GestorMemoria:
    def __init__(
        self,
        max_recursion=500,
        max_variables=10000,
        max_lista=1_000_000,
        max_celdas_matriz=1_000_000,
    ):
        self.max_recursion = max_recursion
        self.max_variables = max_variables
        self.max_lista = max_lista
        self.max_celdas_matriz = max_celdas_matriz
        self.profundidad_recursion = 0

    def entrar_funcion(self):
        if self.profundidad_recursion >= self.max_recursion:
            raise Exception(
                f"Límite de recursión alcanzado ({self.max_recursion}). "
                "Use una versión iterativa o reduzca la profundidad."
            )
        self.profundidad_recursion += 1

    def salir_funcion(self):
        if self.profundidad_recursion > 0:
            self.profundidad_recursion -= 1

    def validar_num_variables(self, memoria):
        if len(memoria) > self.max_variables:
            raise Exception(
                f"Límite de variables alcanzado ({self.max_variables})."
            )

    def validar_lista(self, lista, nombre="lista"):
        if isinstance(lista, list) and len(lista) > self.max_lista:
            raise Exception(
                f"{nombre} excede el límite permitido de elementos "
                f"({len(lista)} > {self.max_lista})."
            )

    def validar_matriz(self, M, nombre="matriz"):
        if not isinstance(M, list) or len(M) == 0:
            raise Exception(f"{nombre} debe ser una matriz no vacía.")

        if not isinstance(M[0], list) or len(M[0]) == 0:
            raise Exception(f"{nombre} debe tener filas no vacías.")

        columnas = len(M[0])
        celdas = 0

        for fila in M:
            if not isinstance(fila, list):
                raise Exception(f"{nombre} debe ser una lista de listas.")
            if len(fila) != columnas:
                raise Exception(f"{nombre} tiene filas de distinto tamaño.")
            celdas += len(fila)

        if celdas > self.max_celdas_matriz:
            raise Exception(
                f"{nombre} excede el límite de celdas "
                f"({celdas} > {self.max_celdas_matriz})."
            )

        return len(M), columnas

    def validar_resultado_matriz(self, filas, columnas, nombre="resultado"):
        celdas = filas * columnas
        if celdas > self.max_celdas_matriz:
            raise Exception(
                f"La matriz {nombre} excede el límite de celdas "
                f"({celdas} > {self.max_celdas_matriz})."
            )

    def liberar_referencias(self, memoria, vals, valor):
        nombres_a_borrar = [
            nombre for nombre, val in memoria.items()
            if val is valor and nombre not in vals
        ]

        for nombre in nombres_a_borrar:
            del memoria[nombre]

        gc.collect()
        return len(nombres_a_borrar)

    def estimar_bytes(self, valor):
        try:
            return sys.getsizeof(valor)
        except Exception:
            return 0