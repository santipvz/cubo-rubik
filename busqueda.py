from nodos import *
from cubo import *

from abc import abstractmethod
from abc import ABCMeta

#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass


class BusquedaAnchura(Busqueda):
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()

        # Variables para rastrear la información
        num_nodos_explorados = 0
        max_tam_abiertos = len(abiertos)
        total_tam_abiertos = len(abiertos)

        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            num_nodos_explorados += 1  # Incrementar el número de nodos explorados
            max_tam_abiertos = max(max_tam_abiertos, len(abiertos))  # Actualizar el tamaño máximo de ABIERTOS
            total_tam_abiertos += len(abiertos)  # Actualizar el total de tamaños de ABIERTOS para calcular el promedio más tarde

            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre

            resultado = [f"Número total de nodos explorados: {num_nodos_explorados}",
                         f"Tamaño máximo de la lista ABIERTOS: {max_tam_abiertos}",
                         f"Tamaño medio de la lista ABIERTOS: {total_tam_abiertos / num_nodos_explorados}",
                         f"Tamaño de la solución encontrada: {len(lista)}"]

            return lista, resultado
        else:
            return None


class BusquedaProfundidad(Busqueda):
    def buscarSolucion(self, inicial, profundidad_maxima=float('inf')):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = set()

        # Variables para rastrear la información
        num_nodos_explorados = 0
        max_tam_abiertos = len(abiertos)
        total_tam_abiertos = len(abiertos)

        abiertos.append(NodoProfundidad(inicial, None, None, 0))
        cerrados.add(inicial.cubo.visualizar())
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado

            num_nodos_explorados += 1  # Incrementar el número de nodos explorados
            max_tam_abiertos = max(max_tam_abiertos, len(abiertos))  # Actualizar el tamaño máximo de ABIERTOS
            total_tam_abiertos += len(abiertos)  # Actualizar el total de tamaños de ABIERTOS para calcular el promedio más tarde

            if actual.esFinal():
                solucion = True
            elif nodoActual.profundidad < profundidad_maxima:
                cerrados.add(actual.cubo.visualizar())
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados:
                        abiertos.append(NodoProfundidad(hijo, nodoActual, operador, nodoActual.profundidad + 1))

        if solucion:
            lista = []
            while nodoActual.padre is not None:
                lista.insert(0, nodoActual.operador)
                nodoActual = nodoActual.padre

            resultado = [f"Número total de nodos explorados: {num_nodos_explorados}",
                         f"Tamaño máximo de la lista ABIERTOS: {max_tam_abiertos}",
                         f"Tamaño medio de la lista ABIERTOS: {total_tam_abiertos / num_nodos_explorados}",
                         f"Tamaño de la solución encontrada: {len(lista)}"]

            return lista, resultado
        else:
            return None

# Implementa la búsqueda en profundidad iterativa. Si encuentra solución, recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoProfundidadIterativa

class BusquedaProfundidadIterativa(Busqueda):
    
    def buscarSolucion(self, inicial):
        profundidad_maxima = 0
        solucion = None
        while solucion is None:
            solucion = BusquedaProfundidad().buscarSolucion(inicial, profundidad_maxima)
            profundidad_maxima += 1
        return solucion


# Implementa la búsqueda voraz. Si encuentra solución, recupera la lista de Operadores empleados.
class BusquedaVoraz(Busqueda):
    def buscarSolucion(self, inicial):
        abiertos = [NodoVoraz(inicial, None, None, 0)]  # Añade None como operador
        cerrados = set()
        solucion = False

        # Variables para rastrear la información
        num_nodos_explorados = 0
        max_tam_abiertos = len(abiertos)
        total_tam_abiertos = len(abiertos)

        while abiertos and not solucion:
            abiertos.sort(key=lambda x: x.heuristica)  # Ordenar por heurística
            nodo_actual = abiertos.pop(0)
            actual = nodo_actual.estado

            num_nodos_explorados += 1  # Incrementar el número de nodos explorados
            max_tam_abiertos = max(max_tam_abiertos, len(abiertos))  # Actualizar el tamaño máximo de ABIERTOS
            total_tam_abiertos += len(abiertos)  # Actualizar el total de tamaños de ABIERTOS para calcular el promedio más tarde

            if actual.esFinal():
                solucion = True
            else:
                cerrados.add(actual.cubo.visualizar())
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    # Calcular la heurística del nuevo estado
                    heuristica = hijo.cubo.heuristicaCasillasDescolocadas()  # Usar la nueva heurística admisible
                    if hijo.cubo.visualizar() not in cerrados:
                        abiertos.append(NodoVoraz(hijo, nodo_actual, operador, heuristica))  # Pasar el operador y la heurística

        if solucion:
            lista = []
            while nodo_actual.padre:
                lista.insert(0, nodo_actual.operador)
                nodo_actual = nodo_actual.padre

            # Imprimir la información
            resultado = [f"Número total de nodos explorados: {num_nodos_explorados}",
                         f"Tamaño máximo de la lista ABIERTOS: {max_tam_abiertos}",
                         f"Tamaño medio de la lista ABIERTOS: {total_tam_abiertos / num_nodos_explorados}",
                         f"Tamaño de la solución encontrada: {len(lista)}"]

            return lista, resultado
        else:
            return None


class BusquedaAStar(Busqueda):
    def buscarSolucion(self, inicial):
        abiertos = [NodoAStar(inicial, None, None, 0, 0)]
        cerrados = set()
        solucion = False

        # Variables para rastrear la información
        num_nodos_explorados = 0
        max_tam_abiertos = len(abiertos)
        total_tam_abiertos = len(abiertos)

        while abiertos and not solucion:
            abiertos.sort(key=lambda x: x.costo + x.heuristica)  # Ordenar por costo total (g(n) + h(n))
            nodo_actual = abiertos.pop(0)
            actual = nodo_actual.estado

            num_nodos_explorados += 1  # Incrementar el número de nodos explorados
            max_tam_abiertos = max(max_tam_abiertos, len(abiertos))  # Actualizar el tamaño máximo de ABIERTOS
            total_tam_abiertos += len(abiertos)  # Actualizar el total de tamaños de ABIERTOS para calcular el promedio más tarde

            if actual.esFinal():
                solucion = True
            else:
                cerrados.add(actual.cubo.visualizar())
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    # Calcular la heurística del nuevo estado
                    heuristica = hijo.cubo.heuristicaCasillasDescolocadas()  # Cambio aquí
                    costo_acumulado = nodo_actual.costo + 1  # Asumiendo que cada movimiento tiene un costo de 1
                    if hijo.cubo.visualizar() not in cerrados:
                        abiertos.append(NodoAStar(hijo, nodo_actual, operador, costo_acumulado, heuristica))

        if solucion:
            lista = []
            while nodo_actual.padre:
                lista.insert(0, nodo_actual.operador)
                nodo_actual = nodo_actual.padre

            # Imprimir la información
            resultado = [f"Número total de nodos explorados: {num_nodos_explorados}",
                         f"Tamaño máximo de la lista ABIERTOS: {max_tam_abiertos}",
                         f"Tamaño medio de la lista ABIERTOS: {total_tam_abiertos / num_nodos_explorados}",
                         f"Tamaño de la solución encontrada: {len(lista)}"]


            return lista, resultado
        else:
            return None


# Implementa la búsqueda IDA*

class BusquedaIDAStar(Busqueda):
    def __init__(self):
        self.heuristica_personalizada = None
        # Variables para rastrear la información
        self.num_nodos_explorados = 0
        self.max_tam_abiertos = 0
        self.total_tam_abiertos = 0

    def buscarSolucion(self, inicial):
        self.heuristica_personalizada = self.calcularHeuristicaPersonalizada(inicial)
        limite = self.heuristica_personalizada
        solucion = None

        while solucion is None:
            solucion, limite = self.buscarSolucionRecursiva(inicial, 0, limite)

        # Imprimir la información
            resultado = [f"Número total de nodos explorados: {self.num_nodos_explorados}",
                         f"Tamaño máximo de la lista ABIERTOS: {self.max_tam_abiertos}",
                         f"Tamaño medio de la lista ABIERTOS: {self.total_tam_abiertos / self.num_nodos_explorados}",
                         f"Tamaño de la solución encontrada: {len(solucion if solucion else [])}"]

        return solucion, resultado

    def buscarSolucionRecursiva(self, estado, costo_acumulado, limite):
        heuristica = self.calcularHeuristicaPersonalizada(estado)
        f = costo_acumulado + heuristica

        self.num_nodos_explorados += 1  # Incrementar el número de nodos explorados
        self.max_tam_abiertos = max(self.max_tam_abiertos, len(estado.operadoresAplicables()))  # Actualizar el tamaño máximo de ABIERTOS
        self.total_tam_abiertos += len(estado.operadoresAplicables())  # Actualizar el total de tamaños de ABIERTOS para calcular el promedio más tarde

        if f > limite:
            return None, f

        if estado.esFinal():
            return [], f

        minimo = float('inf')
        for operador in estado.operadoresAplicables():
            hijo = estado.aplicarOperador(operador)
            costo = 1  # Asumiendo que cada movimiento tiene un costo de 1
            resultado, nuevo_limite = self.buscarSolucionRecursiva(hijo, costo_acumulado + costo, limite)
            if resultado is not None:
                resultado.insert(0, operador)
                return resultado, nuevo_limite
            if nuevo_limite < minimo:
                minimo = nuevo_limite

        return None, minimo

    def calcularHeuristicaPersonalizada(self, estado):
        # Heuristica basada en la cantidad de casillas correctamente orientadas
        heuristica = estado.cubo.heuristicaPosicionesCorrectas()
        return heuristica
