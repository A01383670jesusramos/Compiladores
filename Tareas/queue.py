from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    # mostrar tamaño de queue
    def size(self):
        return len(self.items)
    
    # mostrar si queue esta vacio
    def isEmpty(self):
        return len(self.items) == 0
    
    # agregar item a queue
    def enqueue(self, item):
        self.items.append(item)

    # mostrar primer item en queue
    def front(self):
       if not self.isEmpty():
           return self.items[0]
       
    def back(self):
        if not self.isEmpty():
            return self.items[-1]

    # quitar item del queue
    def dequeue(self):
        if not self.isEmpty():
            return self.items.popleft()

def main():
    q = Queue()

    print("Pruebas Queue")
    # 1. Agregar elementos a la queue
    print("\n1. Agregar elementos")
    print("Agregue un elemento a la queue: ")
    elem = input()
    q.enqueue(elem)
    for i in range(3):
        print("Agregue otro elemento: ")
        elem = input()
        q.enqueue(elem)
    
    # 2. Mostrar tamaño de queue y elementos
    print("\n2. Tamaño y elementos del queue")
    print("Tamaño: ", q.size())
    print(q.items)

    # 3. Mostrar el elemento al frente de queue
    print("\n3. Elemento al frente de queue")
    print("Elemento al frente: ", q.front())

    # 4. Mostrar el elemento al final de queue
    print("\n4. Elemento al final de queue")
    print("Elemento al final: ", q.back())

    # 5. Quitar un elemento del queue
    print("\n5. Quitar un elemento del queue")
    q.dequeue()
    # Mostrar tamaño y elementos del queue actualizado
    print("Tamaño: ", q.size())
    print(q.items)
    print ("First In, First Out. El primer elemento agregado es el primero en salir.")
    

main()
