class Memoria:
    def __init__(self):
        self.memoria = {
            "global": {},
            "cte": {},
            "local": {},
            "temp": {},
            "param": {}
        }

        self.pila_calls = []  # Pila para manejar llamadas a funciones
        self.pila_ambitos = []  # Pila para manejar ámbitos (local/temp)

    def push_frame(self):
        self.pila_ambitos.append({
            "local": {},
            "temp": {},
            "param": {}
        })

    def pop_frame(self):
        if self.pila_ambitos:
            self.pila_ambitos.pop()
        return None
    
    def frame_actual(self):
        if self.pila_ambitos:
            return self.pila_ambitos[-1]

    def obtener_segmento(self, dir):
        if 1 <= dir < 2000:
            return "cte"
        elif 2000 <= dir < 4000:
            return "global"
        elif 4000 <= dir < 6000:
            return "local"
        elif 6000 <= dir < 8000:
            return "param"
        elif dir >= 8000:
            return "temp"
        elif dir == 10000:
            return self.valor_retorno 
    
    def leer_cte(self, dir):
        return self.memoria["cte"].get(dir, 0)
    
    def escribir_cte(self, dir, valor):
        self.memoria["cte"][dir] = valor
    

class MaquinaVirtual:
    def __init__(self, cuadruplos, memoria, directorio_funciones):
        self.cuadruplos = cuadruplos
        self.memoria = memoria
        self.directorio_funciones = directorio_funciones
        self.ip = 0  # pointer de instruccion
        self.pila_retornos = []  # pila para manejar direcciones de retorno
        self.valor_retorno = None
        self.dir_retorno = 10000  # Dirección especial para retorno de funciones

    def leer(self, dir):
        #return self.memoria.memoria.get(dir, 0)
        if dir == 10000:
            return self.valor_retorno
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
            return 0
        elif seg == "param":
            if frame:
                return frame["param"].get(dir, 0)
    
    def escribir(self, dir, valor):
        if dir == 10000:
            self.valor_retorno = valor
            return
        
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
        elif seg == "param":
            if frame:
                frame["param"][dir] = valor

    # ASIGNACION
    def ejecutar_asignacion(self, arg1, result):
        if arg1 == 8999:
            valor = self.leer(8999)
        else:
            valor = self.leer(arg1)
        self.escribir(result, valor)
        print(f"ASIGNA: {result} = {valor}")
    
    # OPERACIONES ARITMETICAS
    def ejecutar_suma(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        print(f"SUMA: {valor1} + {valor2}")
        self.escribir(result, valor1 + valor2)

    def ejecutar_resta(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, valor1 - valor2)

    def ejecutar_mult(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, valor1 * valor2)

    def ejecutar_div(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        if valor2 != 0:
            self.escribir(result, valor1 / valor2)
        else:
            print("Error: Division por cero")
            self.escribir(result, 0)

    # OPERACIONES RELACIONALES
    def ejecutar_mayor(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 > valor2 else 0)
    
    def ejecutar_menor(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 < valor2 else 0)

    def ejecutar_mayorigual(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 >= valor2 else 0)

    def ejecutar_menorigual(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 <= valor2 else 0)

    def ejecutar_igual(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 == valor2 else 0)

    def ejecutar_noigual(self, arg1, arg2, result):
        valor1 = self.leer(arg1)
        valor2 = self.leer(arg2)
        self.escribir(result, 1 if valor1 != valor2 else 0)

    # FUNCIONES
    def ejecutar_era(self, nombre_func, arg1, result):
        self.memoria.push_frame()
    
    def ejecutar_param(self, arg1, result):
        frame = self.memoria.frame_actual()
        valor = self.leer(arg1)
        print(f"PARAM {result}: valor = {valor}")
        dir_param = 6000 + (result - 1)  # Asumimos que los parametros se almacenan a partir de 6000
        frame["param"][dir_param] = valor

    def ejecutar_gosub(self, nombre_func, arg1, result):
        self.pila_retornos.append(self.ip + 1)
        self.ip = result - 1
    
    def ejecutar_return(self, arg1, arg2, result):
        if arg1 is not None:
            valor = self.leer(arg1)

            self.valor_retorno = valor
            self.escribir(10000, valor)
            print("RETURN:", valor)
            print("DIR 10000 =", self.leer(10000))
        
        self.memoria.pop_frame()

        if self.pila_retornos:
            self.ip = self.pila_retornos.pop() - 1
        else:
            self.ip = len(self.cuadruplos)  # Terminar ejecucion
    
    def ejecutar_endf(self):
        self.memoria.pop_frame()
        if self.pila_retornos:
            self.ip = self.pila_retornos.pop() - 1
    
    # CONTROL DE FLUJO
    def ejecutar_goto(self, arg1, arg2, result):
        self.ip = result - 1  # -1 porque loop suma 1 despues
    
    def ejecutar_gotof(self, arg1, arg2, result):
        condicion = self.leer(arg1)
        if not condicion:
            self.ip = result - 1
    
    def ejecutar_label(self, arg1, arg2, result):
        pass
    
    # EJECUCION PRINCIPAL
    def ejecutar(self):
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
