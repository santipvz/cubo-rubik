import sys
from cubo import *
from problemaRubik import *
from busqueda import *
import time

cubo = Cubo()

print("CUBO SIN MEZCLAR:\n" + cubo.visualizar())


#Mover frontal face
cubo.mover(cubo.F)

print("CUBO resultado del movimiento F:\n" + cubo.visualizar())

movs=int(sys.argv[1])

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:",movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())




algoritmos = [BusquedaAnchura(), BusquedaProfundidadIterativa(), BusquedaVoraz(), BusquedaAStar(), BusquedaIDAStar()]

#Descomentar una vez se implemente la búsqueda en anchura
#Creación de un problema
#problema = Problema(cubo, EstadoRubik(cubo), algoritmos[4])

for i in range(len(algoritmos)):
    cubo = Cubo()
    seed(14)
    problema = Problema(EstadoRubik(cubo), algoritmos[i])
    print(f"ALGORITMO: {algoritmos[i].__class__.__name__}\n")
    #Mover frontal face
    cubo.mover(cubo.F)

    movs=int(sys.argv[1])

    movsMezcla = cubo.mezclar(movs)

    a = time.time()
    print("SOLUCION:")
    opsSolucion = problema.obtenerSolucion()
    if opsSolucion != None:
        for o in opsSolucion[0]:
            print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
            cubo.mover(o.movimiento)
        print()
        print("CUBO FINAL:\n" + cubo.visualizar())
        b = time.time()
        print(f"TIEMPO: {b-a}\n")
        for r in opsSolucion[1]:
            print(r)

    else:
        print("no se ha encontrado solución")
        b = time.time()
        print(f"TIEMPO: {b-a}\n")


