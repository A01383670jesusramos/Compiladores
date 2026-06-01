class Dictionary:
    def __init__(self):
        self.dict = {}
    
    # mostrar tamaño de diccionario
    def size(self):
        return len(self.dict)
    
    def items(self):
        return self.dict.items()
    
    # mostrar todas las keys del diccionario
    def keys(self):
        return list(self.dict.keys())
    
    def values(self):
        return list(self.dict.values())
    
    # mostrar si diccionario contiene una key
    def contains(self, key):
        return key in self.dict

    # agregar par key-value al diccionario
    def insert(self, key, value):
        self.dict[key] = value

    # mostrar valor asociado a una key
    def getValue(self, key):
        return self.dict.get(key, None)

def main():
    d = Dictionary()

    print("Pruebas Diccionario")
    # 1. Agregar elementos al diccionario
    print("\n1. Agregar elementos")
    print("Agregue una key: ")
    key = input()
    print("Agregue un valor para la key: ")
    value = input()
    d.insert(key, value)
    for i in range(2):
        print("Agregue otra key: ")
        key = input()
        print("Agregue un valor para la key: ")
        value = input()
        d.insert(key, value)
    
    # 2. Mostrar tamaño y elementos del diccionario
    print("\n2. Tamaño y elementos del diccionario")
    print("Tamaño: ", d.size())
    print(d.items())

    # 3. Mostrar el valor asociado a una key específica
    print("\n3. Valor asociado a una key")
    print("Escribir key")
    key = input()
    if d.contains(key): # Verificar si la key existe
        print("Valor de la key: ", d.getValue(key))
    else:
        print("Esta key no existe en el diccionario")
    
    # 4. Agregar un nuevo par key-value y mostrar el diccionario actualizado
    print("\n4. Agregar un nuevo par key-value")
    print("Escribir nueva key")
    newKey = input()
    print("Asociar valor a la nueva key")
    newValue = input()
    d.insert(newKey, newValue)
    print(d.items())

main()
