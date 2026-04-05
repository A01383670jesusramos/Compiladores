class Stack:
    def __init__(self):
        self.items = []
    
    # mostrar tamaño de stack
    def size(self):
        return len(self.items)
    
    # mostrar si stack esta vacio
    def isEmpty(self):
        return not self
    
    # agregar item a stack
    def push(self, item):
        self.items.append(item)
    
    # quitar item del stack
    def pop(self):
        return self.items.pop()
    
def main():
    s = Stack()

    print("Pruebas Stack")
    print("1. Agregar elementos")
    # 1. Agregar elementos a la stack
    print("\nAgregar un elemento a la stack: ")
    elem = input()
    s.push(elem)
    for i in range(3):
        print("Agregar otro elemento: ")
        elem = input()
        s.push(elem)

    # 2. Mostrar tamaño de stack y elementos
    print("\nTamaño y elementos del stack")
    print("Tamaño: ", s.size())
    print(s.items)

    # 3. Quitar un elemento del stack
    print("\nQuitar un elemento del stack")
    s.pop()
    # Mostrar tamaño y elementos del stack actualizado
    print("Tamaño: ", s.size())
    print(s.items)
    print("Last In, First Out. El último elemento agregado es el primero en salir.")

main()