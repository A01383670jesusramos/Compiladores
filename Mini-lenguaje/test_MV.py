from MV import MaquinaVirtual, Memoria

def test_lectura_escritura():
    mem = Memoria()
    vm = MaquinaVirtual([], mem)

    mem.push_frame()

    vm.escribir(2000, 10)
    vm.escribir(8000, 99)

    valor1 = vm.leer(2000)
    valor2 = vm.leer(8000)

    print("Test_lectura_escritura OK")
    print(f"Global (2000) = {valor1}")
    print(f"Temp (8000) = {valor2}")
    print()

def test_suma_asignacion():
    mem = Memoria()
    mem.push_frame()

    vm = MaquinaVirtual([], mem)
    vm.escribir(2000, 5)
    vm.escribir(2001, 7)

    cuadruplos = [
        ('+', 2000, 2001, 8000),
        ('=', 8000, None, 2002)
    ]

    vm.cuadruplos = cuadruplos
    vm.ejecutar()

    resultado = vm.leer(2002)
    print("Test_suma_asignacion OK")
    print(f"Resultado = {resultado}")
    print()

def test_funcion_suma():
    mem = Memoria()
    mem.push_frame()

    vm = MaquinaVirtual([], mem)
    vm.escribir(2000, 5)  # parametro 1
    vm.escribir(2001, 10) # parametro 2

    cuadruplos = [
        ('ERA', 'suma', None, None),
        ('PARAM', 2000, None, 1),
        ('PARAM', 2001, None, 2),
        ('GOSUB', 'suma', None, 6),
        ('=', 8999, None, 2002),
        ('GOTO', None, None, 9),
        ('+', 6000, 6001, 8000),  
        ('RETURN', 8000, None, None),
        ('ENDF', None, None, None)
    ]

    vm.cuadruplos = cuadruplos
    vm.ejecutar()

    resultado = vm.leer(2002)
    print("TEST FUNCION SUMA OK")
    print(f"Resultado = {resultado}")
    print()

def test_if():
    mem = Memoria()
    mem.push_frame()
    
    vm = MaquinaVirtual([], mem)
    vm.escribir(6000, 5)   # x
    vm.escribir(6001, 10)  # y

    cuadruplos = [
        ('>', 6000, 6001, 8000),     # t1 = 5 > 10 (false)
        ('GOTOF', 8000, None, 4),    # si falso salta
        ('=', 6000, None, 2000),     # NO se ejecuta
        ('LABEL', None, None, 4),
        ('=', 6001, None, 2000)      # sí se ejecuta
    ]

    vm.cuadruplos = cuadruplos
    vm.ejecutar()

    result = vm.leer(2000)
    print("TEST IF OK")
    print(f"Resultado = {result} (debería ser 10)")
    print()

def test_while():
    mem = Memoria()
    mem.push_frame()

    vm = MaquinaVirtual([], mem)
    vm.escribir(6000, 0)   # i = 0

    cuadruplos = [
        ('LABEL', None, None, 0),

        ('<', 6000, 5, 8000),       # t1 = i < 5
        ('GOTOF', 8000, None, 6),

        ('+', 6000, 1, 6000),       # i++

        ('GOTO', None, None, 0),

        ('LABEL', None, None, 6)
    ]

    vm.cuadruplos = cuadruplos
    vm.ejecutar()

    result = vm.leer(6000)
    print("TEST WHILE OK")
    print(f"Resultado = {result} (debería ser 5)")
    print()

if __name__ == "__main__":
    #test_lectura_escritura()
    #test_suma_asignacion()
    test_funcion_suma()
    #test_if()
    #test_while()