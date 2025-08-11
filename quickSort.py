def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]  # pivô fixo
    menores = [x for x in arr[1:] if x <= pivot]  # partição linear
    maiores = [x for x in arr[1:] if x > pivot]   # partição linear
    return quick_sort(menores) + [pivot] + quick_sort(maiores)


lista_teste = [42, 17, 8, 99, 4, 73, 28, 91, 33, 5, 67, 12, 60, 3, 88]
lista_ordenada = quick_sort(lista_teste)
print("Lista ordenada:", lista_ordenada)
