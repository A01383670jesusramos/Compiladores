class Memoria:
    def __init__(self):
        self.memoria = {
            "global": {},
            "cte": {},
            "local": {},
            "temp": {},
            "param": {},
            "retorno": {}
        }

        self.pila_calls = []  # Pila para manejar llamadas a funciones
        self.pila_ambitos = []  # Pila para manejar ámbitos (local/temp)

    def push_frame(self):
        # Crea un nuevo frame para un ambito local
        self.pila_ambitos.append({
            "local": {},
            "temp": {},
            "param": {}
        })

    def pop_frame(self):
        # Elimina el frame actual y retorna al ámbito anterior (salida de función)
        if self.pila_ambitos:
            self.pila_ambitos.pop()
        return None
    
    def frame_actual(self):
        # Retorna el frame actual de la pila de ámbitos
        if self.pila_ambitos:
            return self.pila_ambitos[-1]

    def obtener_segmento(self, dir):
        # Determina a qué segmento de memoria pertenece una dirección virtual
        if 1 <= dir < 2000:
            return "cte"
        elif 2000 <= dir < 4000:
            return "global"
        elif 4000 <= dir < 6000:
            return "local"
        elif 6000 <= dir < 8000:
            return "param"
        elif 8000 <= dir < 10000:
            return "temp"
        elif 10000 <= dir < 12000:
            return "retorno"

    def leer_cte(self, dir):
        # Lee el valor de una constante en la memoria
        return self.memoria["cte"].get(dir, 0)
    
    def escribir_cte(self, dir, valor):
        # Escribe un valor en el segmento de constantes
        self.memoria["cte"][dir] = valor
    

class MaquinaVirtual:
    def __init__(self, cuadruplos, memoria, directorio_funciones):
        self.cuadruplos = cuadruplos
        self.memoria = memoria
        self.directorio_funciones = directorio_funciones
        self.ip = 0  # pointer de instruccion
        self.pila_retornos = []  # pila para manejar direcciones de retorno
        self.pila_funciones = []  # pila para manejar funciones
        self.valor_retorno = None

    def leer(self, dir):
        # Lee el valor almacenado en una dirección
        # Accede al segmento correcto según la dirección
        seg = self.memoria.obtener_segmento(dir)
        frame = self.memoria.frame_actual()

        if seg == "global":
            return self.memoria.memoria["global"].get(dir, 0)
        elif seg == "cte":
            return self.memoria.memoria["cte"].get(dir, 0)
        elif seg == "local":
            if frame:
                return frame["local"].get(dir, 0)
            return 0
        elif seg == "temp":
            if frame:
                return frame["temp"].get(dir, 0)
            return self.memoria.memoria["temp"].get(dir, 0)
        elif seg == "param":
            if frame:
                return frame["param"].get(dir, 0)
        elif seg == "retorno":
            return self.memoria.memoria["retorno"].get(dir, 0)
    
    def escribir(self, dir, valor):
        # Escribe un valor en una dirección 
        # Almacenando en el segmento correcto
        seg = self.memoria.obtener_segmento(dir)
        frame = self.memoria.frame_actual()

        if seg == "global":
            self.memoria.memoria["global"][dir] = valor
        elif seg == "cte":
            self.memoria.memoria["cte"][dir] = valor
        elif seg == "local":
            if frame:
                frame["local"][dir] = valor
        elif seg == "temp":
            if frame:
                frame["temp"][dir] = valor
            else:
                self.memoria.memoria["temp"][dir] = valor
        elif seg == "param":
            if frame:
                frame["param"][dir] = valor
        elif seg == "retorno":
            self.memoria.memoria["retorno"][dir] = valor

    # ASIGNACION
    def ejecutar_asignacion(self, arg1, result):
        # Asigna el valor de arg1 a result
        if arg1 == 8999:
            valor = self.leer(8999)
        else:
            valor = self.leer(arg1)
        self.escribir(result, valor)
    
    # OPERACIONES ARITMETICAS
    def ejecutar_suma(self, arg1, arg2, result):
        # Suma result = arg1 + arg2
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        print(f"SUMA: {valor1} + {valor2}")
        self.escribir(result, valor1 + valor2)

    def ejecutar_resta(self, arg1, arg2, result):
        # Resta result = arg1 - arg2
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, valor1 - valor2)

    def ejecutar_mult(self, arg1, arg2, result):
        # Multiplica result = arg1 * arg2
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, valor1 * valor2)

    def ejecutar_div(self, arg1, arg2, result):
        # Divide result = arg1 / arg2 (valida división por cero)
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        if valor2 != 0:
            self.escribir(result, valor1 / valor2)
        else:
            print("Error: Division por cero")
            self.escribir(result, 0)

    # OPERACIONES RELACIONALES
    def ejecutar_mayor(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 > arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 > valor2 else 0)
    
    def ejecutar_menor(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 < arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 < valor2 else 0)

    def ejecutar_mayorigual(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 >= arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 >= valor2 else 0)

    def ejecutar_menorigual(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 <= arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 <= valor2 else 0)

    def ejecutar_igual(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 == arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 == valor2 else 0)

    def ejecutar_noigual(self, arg1, arg2, result):
        # Realiza comparación: result = 1 si arg1 != arg2, sino 0
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 != valor2 else 0)

    # FUNCIONES
    def ejecutar_era(self, nombre_func, arg1, result):
        # Prepara un nuevo frame para la ejecución de una función (asigna espacio)
        self.memoria.push_frame()
    
    def ejecutar_param(self, arg1, result):
        # Almacena un parámetro en el frame actual para pasar a la función
        frame = self.memoria.frame_actual()
        seg = self.memoria.obtener_segmento(arg1)
        frame_origen = self.memoria.pila_ambitos[-2] if len(self.memoria.pila_ambitos) >= 2 else None

        if seg == "local" and frame_origen:
            valor = frame_origen["local"].get(arg1, 0)
        elif seg == "temp" and frame_origen:
            valor = frame_origen["temp"].get(arg1, 0)
        elif seg == "temp":
            valor = self.memoria.memoria["temp"].get(arg1, 0)
        elif seg == "param" and frame_origen:
            valor = frame_origen["param"].get(arg1, 0)
        elif seg == "global":
            valor = self.memoria.memoria["global"].get(arg1, 0)
        else:
            valor = self.leer(arg1)
        print(f"PARAM {result}: valor = {valor}")
        frame["param"][result] = valor

    def ejecutar_gosub(self, nombre_func, arg1, result):
        # Realiza un salto a la función, guardando la dirección de retorno en la pila
        self.pila_retornos.append(self.ip + 1)
        self.pila_funciones.append(nombre_func)
        self.ip = result - 1
    
    def ejecutar_return(self, arg1, arg2, result):
        # Retorna de una función, almacena el valor de retorno y recupera el punto de llamada
        if arg1 is not None:
            valor = self.leer(arg1)
            nombre_func = self.pila_funciones[-1]
            info = self.directorio_funciones[nombre_func]
            dir_ret = info['dir_ret']

            self.valor_retorno = valor
            self.escribir(dir_ret, valor)
        
        self.pila_funciones.pop()
        self.memoria.pop_frame()

        if self.pila_retornos:
            self.ip = self.pila_retornos.pop() - 1
        else:
            self.ip = len(self.cuadruplos)  # Terminar ejecucion
    
    def ejecutar_endf(self):
        # Finaliza la ejecución de una función
        self.memoria.pop_frame()
        if self.pila_retornos:
            self.ip = self.pila_retornos.pop() - 1
    
    # CONTROL DE FLUJO
    def ejecutar_goto(self, arg1, arg2, result):
        # Realiza un salto a la etiqueta especificada
        self.ip = result - 1  # -1 porque loop suma 1 despues
    
    def ejecutar_gotof(self, arg1, arg2, result):
        # Realiza un salto si la condición es falsa
        condicion = self.leer(arg1)
        if not condicion:
            self.ip = result - 1
    
    def ejecutar_label(self, arg1, arg2, result):
        # Punto de referencia para saltos
        pass

    def resolver_label(self):
        # Convierte etiquetas (nombres) en direcciones de cuadruplos
        mapa = {}
        for i, (op, arg1, arg2, res) in enumerate(self.cuadruplos):
            if op == 'LABEL' and isinstance(res, str):
                mapa[res] = i
        
        resueltos = []
        for (op, arg1, arg2, res) in self.cuadruplos:
            if op in ('GOTO', 'GOTOF') and isinstance(res, str):
                res = mapa.get(res, res)
            resueltos.append((op, arg1, arg2, res))
        
        self.cuadruplos = resueltos
    
    # EJECUCION PRINCIPAL
    def ejecutar(self):
        # Ejecuta todos los cuadruplos en orden, interpretando cada instrucción
        self.resolver_label()
        while self.ip < len(self.cuadruplos):
            operador, arg1, arg2, result = self.cuadruplos[self.ip]

            print(f"IP = {self.ip} -> {(operador,arg1,arg2,result)}")
            # OPERACIONES ARITMETICAS
            if operador == '+':
                self.ejecutar_suma(arg1, arg2, result)
            elif operador == '-':
                self.ejecutar_resta(arg1, arg2, result)
            elif operador == '*':
                self.ejecutar_mult(arg1, arg2, result)
            elif operador == '/':
                self.ejecutar_div(arg1, arg2, result)
            
            # OPERACIONES RELACIONALES
            elif operador == '>':
                self.ejecutar_mayor(arg1, arg2, result)
            elif operador == '<':
                self.ejecutar_menor(arg1, arg2, result)
            elif operador == '>=':
                self.ejecutar_mayorigual(arg1, arg2, result)
            elif operador == '<=':
                self.ejecutar_menorigual(arg1, arg2, result)
            elif operador == '==':
                self.ejecutar_igual(arg1, arg2, result)
            elif operador == '!=':
                self.ejecutar_noigual(arg1, arg2, result)
            
            # ASIGNACION
            elif operador == '=':
                self.ejecutar_asignacion(arg1, result)
            
            # CONTROL DE FLUJO
            elif operador == 'GOTO':
                self.ejecutar_goto(arg1, arg2, result)
            elif operador == 'GOTOF':
                self.ejecutar_gotof(arg1, arg2, result)
            elif operador == 'LABEL':
                self.ejecutar_label(arg1, arg2, result)
            
            # FUNCIONES
            elif operador == 'ERA':
                self.ejecutar_era(arg1, arg2, result)
            elif operador == 'PARAM':
                self.ejecutar_param(arg1, result)
            elif operador == 'GOSUB':
                self.ejecutar_gosub(arg1, arg2, result)
            elif operador == 'RETURN':
                self.ejecutar_return(arg1, arg2, result)
            elif operador == 'ENDF':
                self.ejecutar_endf()

            elif operador == 'PRINT':
                valor = self.leer(arg1)
                print(valor)

            self.ip += 1