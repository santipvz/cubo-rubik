#Nodos a almacenar como parte de los algoritmos de búsqueda

class Nodo:
    def __init__(self, estado, padre):
        self.estado=estado
        self.padre=padre




#Nodos usados por la BusquedaAnchura. 
#Añade el Operador usado para generar el estado almacenado en este Nodo. 
#Usado para simplificar la reconstrucción del camino solución.

class NodoAnchura(Nodo):
    def __init__(self, estado, padre, operador):
        super().__init__(estado, padre)
        self.operador=operador

# Nueva clase de Nodo para la búsqueda en profundidad, que almacena la profundidad del nodo en el árbol de búsqueda
class NodoProfundidad(NodoAnchura):
    def __init__(self, estado, padre, operador, profundidad):
        super().__init__(estado, padre, operador)
        self.profundidad = profundidad

# Nueva clase de Nodo para la búsqueda en profundidad iterativa, que almacena la profundidad del nodo en el árbol de búsqueda
class NodoProfundidadIterativa(NodoProfundidad):
    def __init__(self, estado, padre, operador, profundidad):
        super().__init__(estado, padre, operador, profundidad)


# Nueva clase de Nodo para la búsqueda voraz, que almacena la heurística del nodo
class NodoVoraz(Nodo):
    def __init__(self, estado, padre, operador, heuristica):
        super().__init__(estado, padre)
        self.operador = operador
        self.heuristica = heuristica

class NodoAStar(Nodo):
    def __init__(self, estado, padre, operador, costo, heuristica):
        super().__init__(estado, padre)
        self.operador = operador
        self.costo = costo
        self.heuristica = heuristica


class NodoIDAStar(Nodo):
    def __init__(self, estado, padre, operador, costo, heuristica):
        super().__init__(estado, padre)
        self.operador = operador
        self.costo = costo
        self.heuristica = heuristica
