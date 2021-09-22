
import numpy as np
import matplotlib.pyplot as plt
import itertools


""" Clase para representar una restriccion por separado su ecuacion, operador y resultado"""
class Restriccion():
    def __init__(self, ecuacion, operador, resultado):
        self.ecuacion = ecuacion
        self.operador = operador
        self.resultado = resultado

""" obtiene las intersecciones entre 2 restricciones"""
def get_intersection(restricciones):
    results = []
    A = []
    for restriccion in restricciones:
        results.append(restriccion.resultado)
        A.append(restriccion.ecuacion)
    B = np.array(results)
    A = np.array(A)
    X = np.linalg.solve(A,B)

    return X[0], X[1]


# Evalua si una matriz de un sistema de ecuaciones tiene solucion con el determinante
def has_solution(matriz):

    det = np.linalg.det(matriz)
    if det != 0:
        return True
    return False

# Funcion objetivo
def funcion_objetivo(x, y):
    return 30 * x + 50 * y

# Curva de nivel de la funcion objetivo
def curva_nivel():
    x = np.linspace(0, 100, 100)
    y = np.linspace(0, 100, 100)

    X, Y = np.meshgrid(x, y)
    Z = funcion_objetivo(X, Y)
    plt.contour(X, Y, Z, levels=80)
    plt.show()

""" obtiene los vertices de todas las restricciones"""
def get_vertices(restricciones):
    vertices = []
    for a, b in itertools.combinations(restricciones, 2):
        # evaluamos solo la ecuacion para el determinante
        matriz = np.array([a.ecuacion, b.ecuacion])
        if has_solution(matriz):
            vertices.append(get_intersection([a, b]))
    return vertices

""" Grafica los vertices"""
def graficar_vertices(vertices):
    for vertice in vertices:
        plt.plot(vertice[0], vertice[1], marker='o', color='k')

""" Grafica el espacio factible cerrado"""
def graficar_espacio(vertices):
    x = []
    y = []
    
    for vertice in vertices:
        x.append(vertice[0])
        y.append(vertice[1])
    plt.fill(x, y, color='lime')

# evaulua que un punto pertenezca a la inecuacion
def evaluar_punto(restriccion, punto):
    suma = 0
    for index, variable in enumerate(restriccion.ecuacion):
        suma = variable * punto[index] + suma

    if restriccion.operador == "<=":
        resultado = suma <= restriccion.resultado
    else:
        resultado =  suma >= restriccion.resultado
    if resultado == False:
        return False
    return True
# evalua que un punto pertenezca a la ecuacion
def evaluar_punto_ecuacion(restriccion, punto):
    suma = 0
    for index, variable in enumerate(restriccion.ecuacion):
        suma = variable * punto[index] + suma
    return suma == restriccion.resultado

# evalua un vertice en todas las restricciones
def evaluar_vertice(restricciones, vertice):
    
    for restriccion in restricciones:
        if not evaluar_punto(restriccion, vertice):
            return False
    return True
""" verifica que los vertices cumplan todas las restricciones"""
def solucion_factible(restricciones, vertices):
    vertices_soluciones = []
    for vertice in vertices:
        if evaluar_vertice(restricciones, vertice):
            vertices_soluciones.append(vertice)
    return vertices_soluciones

""" Esta funcion se encarga de obtener el optimo,
    recibe por parametro los vertices y la variable maximo
    si se quiere maximizar debe ser True, para minimizar debe ser False"""

def obtener_optimo(vertices, maximo):
    best_resultado = 0
    best = None
    for vertice in vertices:
        resultado = funcion_objetivo(vertice[0], vertice[1])
        if maximo:
            if resultado >= best_resultado:
                best = vertice
                best_resultado = resultado
        else:
            if resultado <= best_resultado or best_resultado == 0:
                best = vertice
                best_resultado = resultado
        print(f'La funcion objetivo en el vertice ({vertice[0]}, {vertice[1]}) tiene un resultado de: {resultado}')
    return best


# retorna true si el espacio factible es cerrado
def espacio_cerrado(restricciones, vertices):


    copy_vertices = vertices.copy()
    """ Se guarda el primer vertice para ser evaluado al final del recorrido"""
    first = copy_vertices.pop()
    vertice_actual = first
    ultimo_vertice = first
    """ Se recorre el resto de los vertices moviendonos a traves de las funciones de restriccion hasta no poder movernos mas"""
    while copy_vertices:
        for restriccion in restricciones:
            if evaluar_punto_ecuacion(restriccion, vertice_actual):
                vertice_actual = siguiente_vertice(restriccion, copy_vertices, vertice_actual)
        if vertice_actual == ultimo_vertice:
            return False
        ultimo_vertice = vertice_actual
    """ Se evalua si es posible llegar desde el vertice actual hasta el vertice de inicio cerrando asi el espacio"""
    for restriccion in restricciones:
        if evaluar_punto_ecuacion(restriccion, vertice_actual):
            if evaluar_punto_ecuacion(restriccion, first):
                return True
    return False

""" Se mueve desde el vertice actual al siguiente vertice a traves de una misma funcion de restriccion"""
def siguiente_vertice(restriccion, copy_vertices, old_vertice):
    for index, vertice in enumerate(copy_vertices):
        if evaluar_punto_ecuacion(restriccion, old_vertice):
            if evaluar_punto_ecuacion(restriccion, vertice):
                copy_vertices.pop(index)
                return vertice
    return old_vertice

if __name__ == "__main__":
    curva_nivel()
    
    """ valores que tendra x en el grafico """
    x = np.arange(-100, 100)

    """ Las restricciones deben tener 2 formatos, el de objeto y el de funcion despejada para poder graficarla"""
    # Restricciones escritas en vectores y como funciones
    # -x + y <= 11
    restriccion_1 = Restriccion([-1, 1], "<=", 11)
    y1 = 11 + x
    
    restriccion_2 = Restriccion([1, 1], "<=", 27)
    y2 = 27 - x

    restriccion_3 = Restriccion([2, 5], "<=", 90)
    y3 = (90 - 2 *x) / 5
    
    restriccion_5 = Restriccion([1, 0], ">=", 0)

    x1 = 0 
    restriccion_6 = Restriccion([0, 1], ">=", 0)

    y4 = 0

    restricciones = [restriccion_1, restriccion_2, restriccion_3, restriccion_5, restriccion_6]
    plt.plot(x, y1, '-', linewidth=2, color='b')
    plt.plot(x, y2, '-', linewidth=2, color='g')
    plt.plot(x, y3, '-', linewidth=2, color='g')


    plt.axhline(y = y4, linewidth=2, color='c')
    plt.axvline(x = x1, linewidth=2, color='r')
    plt.grid()
    vertices = get_vertices(restricciones)
    vertices = solucion_factible(restricciones, vertices)
    if len(vertices) == 0:
        print('El espacio factible es vacio')
    elif len(vertices) > 2:
        """ Se verifica si por lo menos existen 3 vertices que es lo minimo para formar un espacio cerrado"""
        cerrado = espacio_cerrado(restricciones, vertices)
        if cerrado:
            graficar_vertices(vertices)
            print('El espacio factible es cerrado y distinto de vacio')
            # Vertices ordenados con la coordenada X de menor a mayor
            vertices = sorted(vertices, key=lambda tup: (tup[0], tup[1]))
            graficar_espacio(vertices)
            optimo = obtener_optimo(vertices, True)
            print(f' El valor optimo es en el vertice ({optimo[0]}, {optimo[1]})')
            ax = plt.subplot()
            ax.set_ylim(bottom=0)
            # set the x-spine (see below for more info on `set_position`)
            ax.spines['left'].set_position('zero')

            # turn off the right spine/ticks
            ax.spines['right'].set_color('none')
            ax.yaxis.tick_left()

            # set the y-spine
            ax.spines['bottom'].set_position('zero')

            # turn off the top spine/ticks
            ax.spines['top'].set_color('none')
            ax.xaxis.tick_bottom()

            plt.show()
        else:
            print('El espacio factible es abierto')
