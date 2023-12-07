from itertools import chain, combinations

def todos_subconjuntos(estados):
    """Genera todos los subconjuntos de un conjunto dado de estados."""
    return chain.from_iterable(combinations(estados, r) for r in range(len(estados)+1))

def ordenar_subconjuntos(subconjuntos):
    """Ordena los subconjuntos primero por tamaño y luego lexicográficamente."""
    # Convertir cada subconjunto a una lista de índices (números) para ordenar
    subconjuntos_indices = [list(int(estado[1:]) for estado in subconjunto) for subconjunto in subconjuntos]
    subconjuntos_indices.sort(key=lambda x: (len(x), x))
    # Convertir de nuevo a la notación original
    return [list('q' + str(index) for index in subconjunto) for subconjunto in subconjuntos_indices]

def estados_finales_posibles(n,nFinal=None):
    """Genera y ordena los estados finales posibles para un autómata de n estados."""
    estados = ['q' + str(i) for i in range(n)]
    subconjuntos = list(todos_subconjuntos(estados))
    subconjuntos_ordenados = ordenar_subconjuntos(subconjuntos)
    if nFinal != None:
        ret = []
        for i in subconjuntos_ordenados:
            if len(i) >= nFinal:
                ret.append(i)
        return ret     
    return subconjuntos_ordenados
def estados_finales_tamano_n(n, n_final):
    """Genera los estados finales posibles de tamaño n_final para un autómata de n estados."""
    estados = ['q' + str(i) for i in range(n)]
    # Generar solo los subconjuntos de tamaño n_final
    subconjuntos = combinations(estados, n_final)
    return [list(subconjunto) for subconjunto in subconjuntos]
