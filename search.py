from collections import deque
def generalSearch(goal, expande, start={}, check_point=lambda nodo, frontera: None):
    mejor_path = []

    frontera = deque()  # En BFS la frontera es una pila

    # Agrego por a derecha, ya que es una cola
    frontera.append((start, [start])) # nodo y path

    while frontera:
        # print('Tamaño de la frontera ', len(frontera))
        nodo, path = frontera.popleft() # Extraigo por la izquierda
        check_point(nodo, frontera)
        if goal(nodo):
            mejor_path = path
            mejor_solucion = nodo
            yield mejor_solucion, mejor_path
        else:
            vecinos = expande(nodo)
            for vecino in vecinos:
                frontera.appendleft((vecino, path+[vecino]))