class CuboSemantico:
    # Definicion de reglas de tipos para operaciones

    def __init__(self):
        # Operadores aritmeticos (+, -, *)
        self.aritmeticos = {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
        }

        # Division (/)
        # Siempre retorna flotantes
        self.division = {
            ('int', 'int'): 'float',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
        }

        # Operadores relacionales (==, !=, <, >, <=, >=)
        # Booleano numerico (1 = verdadero, 0 = falso)
        self.relacionales = {
            ('int', 'int'): 'int',
            ('int', 'float'): 'int',
            ('float', 'int'): 'int',
            ('float', 'float'): 'int',
        }

        # Asignacion (=)
        self.asignacion = {
            ('int', 'int'): True,
            ('int', 'float'): True, # Truncamiento
            ('float', 'int'): True,
            ('float', 'float'): True,
        }

    def tipo_aritmetico(self, tip_izq, tip_der, operador):
        # Determinar el tipo resultante de una operacion
        if operador == '/':
            return self.division.get((tip_izq, tip_der))
        else:
            return self.aritmeticos.get((tip_izq, tip_der))
    
    def tipo_relacional(self, tip_izq, tip_der, operador):
        # Determinar el tipo resultante de una comparacion
        # Primero validar que los tipos sean compatibles
        if (tip_izq, tip_der) in self.relacionales:
            return 'int'
        return None
    
    def asignacion_valida(self, tip_var, tip_exp):
        # Verificar si la asignacion es valida
        return self.asignacion.get((tip_var, tip_exp), False)
    
    def promocion(self, tip_izq, tip_der):
        # Determinar el tipo comun para promocion de operandos.
        # 'float' si alguno es flotante. Si no, 'int'
        if tip_izq == 'float' or tip_der == 'float':
            return 'float'
        return 'int'

class DirectorioFunciones:
    # Estructura: Diccionario

    def __init__(self):
        self.funciones = {}

    def agregar(self, nombre, tipo_return, parametros, inicio=None):
        self.funciones[nombre] = {
            'tipo_return': tipo_return,
            'parametros': parametros,
            'num_parametros': len(parametros),
            'inicio': inicio
        }
    
    def buscar(self, nombre):
        return self.funciones.get(nombre)
    
    def existe(self, nombre):
        return nombre in self.funciones
    
    def actualizar_inicio(self, nombre, inicio):
        if nombre in self.funciones:
            self.funciones[nombre]['inicio'] = inicio
            
class TablaVariables:
    # Estructura: Pila de diccionarios
    # Forma de la estructura:
    #     pila_ambitos = [
    #     {},                    # Ámbito 0 (global)
    #     {"a": {...}},          # Ámbito 1 (función saludar)
    #     {"temp": {...}}        # Ámbito 2 (bloque dentro de función)
    #     ]

    def __init__(self):
        self.pila_ambitos = [{}] # Ambito 0 = global
        self.cont_ambitos = 0

        # Seccion de entrega 4: Direcciones virtuales
        self.rango_dir_cte = 1 # Constantes en direcciones de 1 a 1999
        self.rango_dir_g = 2000 # Var globales en direcciones de 2000 a 3999
        self.rango_dir_l = 4000 # var locales en direcciones de 4000 a 5999
        self.rango_dir_p = 6000 # parametros en direcciones de 6000 a 7999
        self.rango_dir_temp = 8000 # var temporales en direcciones de 8000 a 9999

        self.cont_cte = 0
        self.cont_g = 0
        self.cont_l = 0
        self.cont_p = 0
        self.cont_temp = 0

        # Diccionarios de almacenamiento de direcciones asignadas
        self.dir_cte = {}
        self.dir_g = {}
        self.dir_l = {}
        self.dir_p = {}
        self.dir_temp = {}

    def entrada_ambito(self):
        self.cont_ambitos += 1
        self.pila_ambitos.append({})
    
    def salida_ambito(self):
        if len(self.pila_ambitos) > 1:
            self.pila_ambitos.pop()
            self.cont_ambitos -= 1
    
    def declar_var(self, nombre, tipo, linea):
        ambito_act = self.pila_ambitos[-1]

        if nombre in ambito_act:
            print(f"Error semantico: Variable '{nombre}' ya declarada en el mismo ambito en linea {linea}")
            return False
        
        ambito_act[nombre] = {
            'tipo': tipo,
            'inicializada': False,
            'ambito': self.cont_ambitos,
            'linea': linea
        }
        return True
    
    def buscar_var(self, nombre):
        for i in range(len(self.pila_ambitos) -1, -1, -1):
            if nombre in self.pila_ambitos[i]:
                return self.pila_ambitos[i][nombre]
        return None

    # ENTREGA 4
    # Crear direcciones
    def nueva_cte(self, valor):
        # Asignar dirección virtual a una constante
        if valor not in self.dir_cte:
            self.cont_cte += 1
            direccion = self.rango_dir_cte + self.cont_cte - 1
            self.dir_cte[valor] = direccion
        return self.dir_cte[valor]
    
    def nueva_var_g(self, nombre):
        # Asignar dirección virtual a una variable global
        if nombre not in self.dir_g:
            self.cont_g += 1
            direccion = self.rango_dir_g + self.cont_g - 1
            self.dir_g[nombre] = direccion
        return self.dir_g[nombre]
    
    def nueva_var_l(self, nombre, ambito):
        # Asignar dirección virtual a una variable local
        clave = (ambito, nombre)
        if clave not in self.dir_l:
            self.cont_l += 1
            direccion = self.rango_dir_l + self.cont_l - 1
            self.dir_l[clave] = direccion
        return self.dir_l[clave]

    def nueva_var_p(self, nombre, func):
        # Asignar dirección virtual a un parámetro
        clave = (func, nombre)
        if clave not in self.dir_p:
            self.cont_p += 1
            direccion = self.rango_dir_p + self.cont_p - 1
            self.dir_p[clave] = direccion
        return self.dir_p[clave]
    
    # Obtener direcciones
    def obtener_dir_cte(self, valor):
        # Obtener direccion de una constante
        return self.dir_cte.get(valor)
    
    def obtener_dir_g(self, nombre):
        # Obtener direccion de una variable global
        return self.dir_g.get(nombre)

    def obtener_dir_l(self, nombre, ambito):
        # Obtener direccion de una variable local
        return self.dir_l.get((ambito, nombre))

    def obtener_dir_p(self, nombre, func):
        # Obtener direccion de un parámetro
        return self.dir_p.get((func, nombre))

    def obtener_dir_temp(self):
        # Obtener direccion de una variable temporal
        return self.dir_temp.get(self.cont_temp)
    
    def obtener_dir_var(self, nombre, ambito_actual=0, funcion_actual=None):
        # Obtener direccion de una variable segun su ambito
        # Primero busca en parametros, luego locales, luego globales
        if funcion_actual:
            dir_p = self.obtener_dir_p(nombre, funcion_actual)
            if dir_p is not None:
                return dir_p
        
        dir_l = self.obtener_dir_l(nombre, ambito_actual)
        if dir_l:
            return dir_l
        
        dir_g = self.obtener_dir_g(nombre)
        if dir_g:
            return dir_g
        
        return None
    
    def obtener_func_actual(self):
        # Obtener la funcion actual en la pila de ambitos
        for i in range(len(self.pila_ambitos) -1, -1, -1):
            if 'funcion' in self.pila_ambitos[i]:
                return self.pila_ambitos[i]['funcion']
        return None

    # Depuracion
    def mostrar_tabla_dir(self):
        print("Tabla de Direcciones Virtuales:")
        print("Constantes:")
        if self.dir_cte:
            for valor, dir in self.dir_cte.items():
                print(f"  {dir}: {valor}")
        else:
            print(" No hay constantes.")
        print("Variables Globales:")
        if self.dir_g:
            for nombre, dir in self.dir_g.items():
                print(f"  {dir}: {nombre}")
        else:
            print(" No hay variables globales.")
        print("Variables Locales:")
        if self.dir_l:
            for (ambito, nombre), dir in self.dir_l.items():
                print(f"  {dir}: {nombre} (ambito {ambito})")
        else:
            print(" No hay variables locales.")
        print("Parametros:")
        if self.dir_p:
            for (func, nombre), dir in self.dir_p.items():
                print(f"  {dir} - {nombre} (funcion {func})")
        else:
            print(" No hay parametros.")
        print(f"Variables Temporales: {self.cont_temp}")


class Pila:
    # Pila general para mejor manejo de uso para pilas de operadores, operandos y tipos
    
    def __init__(self):
        self.items = []

    def push(self, item):
        # Agregar un elemento a la pila
        self.items.append(item)

    def pop(self):
        # Saca y retorna el elemento superior de la pila
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def top(self):
        # Retorna el elemento superior
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        # Verifica si la pila esta vacia
        return len(self.items) == 0
    
    def limpiar(self):
        # Limpia la pila
        self.items = []

    def __repr__(self): # Representacion de la pila para debug
        return str(self.items)
    
class Pila_Operadores(Pila):
    # Pila para operadores

    # Precedencia de operadores
    # (numero mas alto equivale a mayor prioridad)
    precedencia = {
        '=': 1,
        '==': 2, '!=': 2, '<': 2, '>': 2, '<=': 2, '>=': 2,
        '+': 3, '-': 3,
        '*': 4, '/': 4,
        'UMENOS': 5,
        '(': 0, 
        ')': 0
    }

    # def get_precedencia(self, operador):
    #     # Retorna la precedencia de un operador
    #     return self.precedencia.get(operador, 0)
    
    def mayor_precedencia(self, op1, op2):
        # Verifica si op1 tiene mayor o igual precedencia que op2
        return self.precedencia.get(op1, 0) >= self.precedencia.get(op2, 0)
    
class Pila_Operandos(Pila):
    # Pila para operandos
    
    def __init__(self):
        super().__init__() # Inicializa la pila de operandos (self.items = [])
        self.contador_temporales = 0

    def nuevo_temporal(self):
        # Genera un nuevo temporal
        self.contador_temporales += 1
        return f"t{self.contador_temporales}"
    
    def push_temp(self):
        # Crea un temporal y lo agrega a la pila
        temp = self.nuevo_temporal()
        self.push(temp)
        return temp
    
class Pila_Tipos(Pila):
    # Pila para tipos

    def push_operando(self, tipo):
        # Registra el tipo de un operando
        self.push(tipo)

    def pop_operando(self):
        # Obtiene el tipo del ultimo operando
        return self.pop()
    
    def compatible(self, tipo1, tipo2):
        # Verificar si dos tipos son compatibles
        # Ej. int and float = True
        if tipo1 == tipo2:
            return True
        if (tipo1 == 'int' and tipo2 == 'float') or (tipo1 == 'float' and tipo2 == 'int'):
            return True
        return False
    
class Fila_Cuadruplos:
    # Fila (Queue) para almacenar cuadruplos

    def __init__(self):
        self.cuadruplos = []
        self.contador = 0

    def agregar(self, operador, operando1, operando2, result):
        # Agrega un nuevo cuadruplo a la fila
        # Formato: (operador, operando1, operando2, resultado)
        cuadruplo = (operador, operando1, operando2, result)
        self.cuadruplos.append(cuadruplo)
        self.contador += 1
        return self.contador - 1
    
    def obtener(self, indice):
        # Retorna el cuadruplo por su indice
        if 0 <= indice < len(self.cuadruplos):
            return self.cuadruplos[indice]
        return None
    
    def obtener_todos(self):
        # Retorna todos los cuadruplos
        return self.cuadruplos
    
    def __len__(self):
        return len(self.cuadruplos)
    
    def actualizar_result(self, indice, nuevo_result):
        # Actualiza el resultado de un cuadruplo existente
        operador, op1, op2, _ = self.obtener(indice)
        self.cuadruplos[indice] = (operador, op1, op2, nuevo_result)
    
    def __repr__(self):
        result = []
        for i, (opr, op1, op2, res) in enumerate(self.cuadruplos):
            result.append(f"{i}: ({opr}, {op1}, {op2}, {res})")
        return "\n".join(result)
    
# Generacion de codigo intermedio
class Generar_Codigo:
    # Integra las estructuras para hacer cuadruplos

    def __init__(self):
        self.operadores = Pila_Operadores()
        self.operandos = Pila_Operandos()
        self.tipos = Pila_Tipos()
        self.cuadruplos = Fila_Cuadruplos()
        self.operandos_direcciones = Pila_Direcciones()
        self.saltos = Pila_Jumps()

    def limpiar(self):
        # Limpia las estructuras
        self.operadores.limpiar()
        self.operandos.limpiar()
        self.tipos.limpiar()
        self.operandos_direcciones.limpiar()
        self.cuadruplos = Fila_Cuadruplos()

    def mostrar_estado(self):
        # Muestra el estado actual de las estructuras
        print("Pila de Operadores:", self.operadores)
        print("Pila de Operandos:", self.operandos)
        print("Pila de Tipos:", self.tipos)
        print("Cuadruplos:")
        if len(self.cuadruplos) > 0:
            print("Cuadruplos")
            print(self.cuadruplos)


# Entrega 4
class Pila_Direcciones(Pila):
    # Pila para direcciones virtuales
    pass

class Pila_Jumps(Pila):
    # Pila para saltos
    pass

