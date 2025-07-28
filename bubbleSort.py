def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


numeros = [5, 2, 9, 1, 5, 6]
print("Lista original:", numeros)
ordenada = bubble_sort(numeros)
print("Lista ordenada:", ordenada)
