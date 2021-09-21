
import numpy as np
import matplotlib.pyplot as plt
import itertools

class Restriccion():
    def __init__(self, ecuacion, operador, resultado):
        self.ecuacion = ecuacion
        self.operador = operador
        self.resultado = resultado

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


# Evalua si una matriz de un sistema de ecuaciones tiene solucion
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


def get_vertices(restricciones):
    vertices = []
    for a, b in itertools.combinations(restricciones, 2):
        # quitamos los resultados ya que solo queremos calcular el determinante
        matriz = np.array([a.ecuacion, b.ecuacion])
        if has_solution(matriz):
            vertices.append(get_intersection([a, b]))
    return vertices

def graficar_vertices(vertices):
    for vertice in vertices:
        plt.plot(vertice[0], vertice[1], marker='o', color='k')

def graficar_espacio(vertices):
    x = []
    y = []
    
    for vertice in vertices:
        x.append(vertice[0])
        y.append(vertice[1])
    plt.fill(x, y, color='lime')


def evaluar_vertice(restricciones, vertice):
    
    for restriccion in restricciones:
        suma = 0
        
        for index, variable in enumerate(restriccion.ecuacion):
            suma = variable * vertice[index] + suma

        if restriccion.operador == "<=":
            resultado =  suma <= restriccion.resultado
        else:
            resultado =  suma >= restriccion.resultado
        if resultado == False:
            return False
    return True

def solucion_factible(restricciones, vertices):
    vertices_soluciones = []
    for vertice in vertices:
        if evaluar_vertice(restricciones, vertice):
            vertices_soluciones.append(vertice)
    
    return vertices_soluciones


def obtener_optimo(vertices):
    best_resultado = 0
    best = None
    for vertice in vertices:
        resultado = funcion_objetivo(vertice[0], vertice[1])
        if resultado >= best_resultado:
            best = vertice
            best_resultado = resultado
        print(f'La funcion objetivo en el vertice ({vertice[0]}, {vertice[1]}) tiene un resltado de: {resultado}')
    return best

if __name__ == "__main__":
    #curva_nivel()
    
    """
    x + 3y ≤ 200

    x + y ≤ 100

    x ≥ 20

    y ≥ 10

    """
    x = np.arange(0, 200)
    # Restricciones escritas en vectores y como funciones
    restriccion_1 = Restriccion([1, 3], "<=", 200)
    y1 = (200 - x) / 3
    
    restriccion_2 = Restriccion([1, 1], "<=", 100)
    y2 = 100 - x

    restriccion_3 = Restriccion([1, 0], ">=", 20)
    x1 = 20
    
    restriccion_4 = Restriccion([0, 1], ">=", 10)
    y3 = 10
    restricciones = [restriccion_1, restriccion_2, restriccion_3, restriccion_4]
    plt.plot(x, y1, '-', linewidth=2, color='b')
    plt.plot(x, y2, '-', linewidth=2, color='g')
    plt.axhline(y = y3, linewidth=2, color='c')
    plt.axvline(x = x1, linewidth=2, color='r')
    plt.grid()
    vertices = get_vertices(restricciones)
    vertices = solucion_factible(restricciones, vertices)
    # Vertices ordenados con la coordenada X de menor a mayor
    vertices = sorted(vertices, key=lambda tup: (tup[0], tup[1]))
    graficar_vertices(vertices)
    graficar_espacio(vertices)
    obtener_optimo(vertices)
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