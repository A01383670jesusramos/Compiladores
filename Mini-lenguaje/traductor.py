from semantica import Generar_Codigo, CuboSemantico

class Traductor:
    # Traduce expresiones y estatutos a cuadruplos
    def __init__(self, tabla_vars, directorio):
        self.gen = Generar_Codigo()
        self.cubo = CuboSemantico()
        self.tabla_vars = tabla_vars
        self.directorio = directorio
        self.operadores_aritmeticos = {'+', '-', '*', '/'}
        self.operadores_relacionales = {'==', '!=', '<', '>', '<=', '>='}
        self.cont_etiquetas = 0 # ENTREGA 4
        self.funcion_actual = None # ENTREGA 4
        self.retorno = False # ENTREGA 4
        self.pos_goto_main = None # ENTREGA 4

    # ENTREGA 4
    def nueva_var_temp(self):
        # Asignar dirección virtual a una variable temporal
        self.tabla_vars.cont_temp += 1
        direccion = (self.tabla_vars.rango_dir_temp + self.tabla_vars.cont_temp - 1)
        nombre = f"t{self.tabla_vars.cont_temp}"

        # Guardar al diccionario de variables temporales
        self.tabla_vars.dir_temp[nombre] = direccion
        return nombre, direccion

    # ENTREGA 4
    def nueva_etiqueta(self):
        # Crear una etiqueta
        self.cont_etiquetas += 1
        return f"L{self.cont_etiquetas}"
    
    # ENTREGA 4
    def nueva_etiqueta_funcion(self, nombre):
        # Crear etiqueta para funcion
        return f"func_{nombre}"

    # Expresiones Aritmeticas
    
    def proces_operador(self, operador):
        # Procesar operador según el algoritmo de traducción
        while (not self.gen.operadores.is_empty() and
               self.gen.operadores.top() != '(' and
               self.gen.operadores.mayor_precedencia(self.gen.operadores.top(), operador)):
            
            # Generar cuadruplo para el operador pendiente
            op = self.gen.operadores.pop()
            if op == 'UMENOS':
                operando = self.gen.operandos.pop()
                tipo_op = self.gen.tipos.pop()

                temp_nombre, temp_dir = self.nueva_var_temp()
                self.gen.operandos.push(temp_nombre)
                self.gen.operandos_direcciones.push(temp_dir)
                self.gen.tipos.push(tipo_op)
                self.gen.cuadruplos.agregar(op, operando, None, temp_dir)
            else:
                dir_operando2 = self.gen.operandos_direcciones.pop()
                tipo_op2 = self.gen.tipos.pop()
                dir_operando1 = self.gen.operandos_direcciones.pop()
                tipo_op1 = self.gen.tipos.pop()

                # Determinar el tipo resultante
                if op in self.operadores_aritmeticos:
                    tipo_res = self.cubo.tipo_aritmetico(tipo_op1, tipo_op2, op)
                else:
                    tipo_res = self.cubo.tipo_relacional(tipo_op1, tipo_op2, op)

                # Verificar si la operacion es valida
                if tipo_res is None:
                    print(f"Error semantico: '{op}' entre {tipo_op1} y {tipo_op2} no valida")
                    tipo_res = 'error'

                temp_nombre, temp_dir = self.nueva_var_temp()
                self.gen.operandos.push(temp_nombre)
                self.gen.operandos_direcciones.push(temp_dir)
                self.gen.tipos.push(tipo_res)
                self.gen.cuadruplos.agregar(op, dir_operando1, dir_operando2, temp_dir)
        
        self.gen.operadores.push(operador)
    
    def proces_operando(self, operando, tipo, direccion=None):
        # Procesar un operando
        if direccion is None:
            if isinstance(operando, (int,float)):
                direccion = self.tabla_vars.nueva_cte(operando)
            else:
                direccion = operando
        self.gen.operandos.push(operando)
        self.gen.operandos_direcciones.push(direccion)
        self.gen.tipos.push(tipo)

    def proces_parentesisA(self):
        # Procesar '('
        self.gen.operadores.push('(')

    def proces_parentesisC(self):
        # Procesar ')'
        while not self.gen.operadores.is_empty() and self.gen.operadores.top() != '(':
            op = self.gen.operadores.pop()
            if op == 'UMENOS':
                operando = self.gen.operandos.pop()
                tipo_op = self.gen.tipos.pop()
                temp = self.gen.operandos.push_temp()
                self.gen.tipos.push(tipo_op)
                self.gen.cuadruplos.agregar(op, operando, None, temp)
            else:
                operando2 = self.gen.operandos.pop()
                tipo_op2 = self.gen.tipos.pop()
                operando1 = self.gen.operandos.pop()
                tipo_op1 = self.gen.tipos.pop()

                if op in self.operadores_aritmeticos:
                    tipo_res = self.cubo.tipo_aritmetico(tipo_op1, tipo_op2, op)
                else:
                    tipo_res = self.cubo.tipo_relacional(tipo_op1, tipo_op2, op)

                if tipo_res is None:
                    print(f"Error semantico: '{op}' entre {tipo_op1} y {tipo_op2} no valida")
                    tipo_res = 'error'

                temp = self.gen.operandos.push_temp()
                self.gen.tipos.push(tipo_res)
                self.gen.cuadruplos.agregar(op, operando1, operando2, temp)
        
        if not self.gen.operadores.is_empty() and self.gen.operadores.top() == '(':
            self.gen.operadores.pop() # Eliminar '('
    
    def proces_umenos(self):
        # Procesar menos unario
        self.gen.operadores.push('UMENOS')

    def fin_expresion(self):
        # Finaliza el proceso de una expreision
        
        while not self.gen.operadores.is_empty():
            op = self.gen.operadores.pop()
            if op == '(' or op == ')':
                continue
            elif op == 'UMENOS':
                operando = self.gen.operandos.pop()
                dir_operando = self.gen.operandos_direcciones.pop()
                tipo_op = self.gen.tipos.pop()

                temp_nombre, temp_dir = self.nueva_var_temp()
                self.gen.operandos.push(temp_nombre)
                self.gen.operandos_direcciones.push(temp_dir)
                self.gen.tipos.push(tipo_op)
                self.gen.cuadruplos.agregar(op, dir_operando, None, temp_dir)
            else:
                operando2 = self.gen.operandos.pop()
                dir_operando2 = self.gen.operandos_direcciones.pop()
                tipo_op2 = self.gen.tipos.pop()
                operando1 = self.gen.operandos.pop()
                dir_operando1 = self.gen.operandos_direcciones.pop()
                tipo_op1 = self.gen.tipos.pop()

                if op in self.operadores_aritmeticos:
                    tipo_res = self.cubo.tipo_aritmetico(tipo_op1, tipo_op2, op)
                else:
                    tipo_res = self.cubo.tipo_relacional(tipo_op1, tipo_op2, op)

                if tipo_res is None:
                    print(f"Error semantico: '{op}' entre {tipo_op1} y {tipo_op2} no valida")
                    tipo_res = 'error'
                
                temp_nombre, temp_dir = self.nueva_var_temp()
                self.gen.operandos.push(temp_nombre)
                self.gen.operandos_direcciones.push(temp_dir)
                self.gen.tipos.push(tipo_res)
                print(f"Debug op = {op}\n"
                      f"dir1 = {dir_operando1}\n"
                      f"dir2 = {dir_operando2}")
                self.gen.cuadruplos.agregar(op, dir_operando1, dir_operando2, temp_dir)
        
        #Resuldato final en el tope de Pila_Operandos
        result = self.gen.operandos.pop()
        direccion_result = self.gen.operandos_direcciones.pop()
        tipo_result = self.gen.tipos.pop()

        return result, direccion_result, tipo_result
    

    def traduc_asignacion(self, id_var, dir_result, tipo_exp):
        var_info = self.tabla_vars.buscar_var(id_var)
        if var_info and 'direccion' in var_info:
            dir_var = var_info['direccion']
        else:
            dir_var = self.tabla_vars.nueva_var_g(id_var)
        self.gen.cuadruplos.agregar('=', dir_result, None, dir_var)

    def traduc_call(self, nom_func, args):
        # Traducir llamada a funcion

        for i, arg in enumerate(args):
            self.gen.cuadruplos.agregar('PARAM', arg, None, None)
        
        self.gen.cuadruplos.agregar('call', nom_func, None, None)

    def traduc_print(self, exp):
        # Traducir print
        pass

     # ENTREGA 4
    def traduc_if(self, dir_condicion):
        # Traducir if
        label_fin = self.nueva_etiqueta()
        self.gen.cuadruplos.agregar('if', dir_condicion, None, label_fin)
        return label_fin
    
    def finalizar_if(self, label_fin):
        # Finalizar if
        self.gen.cuadruplos.agregar('label', None, None, label_fin)

    def traduc_else(self, dir_condicion):
        # Traducir else
        label_else = self.nueva_etiqueta()
        label_fin = self.nueva_etiqueta()
        self.gen.cuadruplos.agregar('if', dir_condicion, None, label_else)
        return label_else, label_fin
    
    def salto(self, label_else, label_fin):
        # Manejar saltos
        # Salto al final
        self.gen.cuadruplos.agregar('goto', None, None, label_fin)
        # Salto a else
        self.gen.cuadruplos.agregar('label', None, None, label_else)

    def finalizar_else(self, label_fin):
        # Finalizar else
        self.gen.cuadruplos.agregar('label', None, None, label_fin)

    def traduc_while_inicio(self):
        # Traducir inicio de while
        label_inicio = self.nueva_etiqueta()
        label_fin = self.nueva_etiqueta()
        self.gen.cuadruplos.agregar('label', None, None, label_inicio)
        return label_inicio, label_fin
    
    def traduc_while_condicion(self, dir_condicion, label_inicio, label_fin):
        # Traducir condición de while
        self.gen.cuadruplos.agregar('if', dir_condicion, None, label_fin)

    def finalizar_while(self, label_inicio, label_fin):
        # Finalizar while
        self.gen.cuadruplos.agregar('goto', None, None, label_inicio)
        self.gen.cuadruplos.agregar('label', None, None, label_fin)

    def iniciar_func(self, nombre):
        # Iniciar traduccion de funcion
        label = self.nueva_etiqueta_funcion(nombre)
        self.gen.cuadruplos.agregar('label', None, None, label)

        self.funcion_actual = nombre
        self.retorno = False
    
    def finalizar_func(self):
        # Finalizar traduccion de funcion
        info = self.directorio.buscar(self.funcion_actual)
        if info is not None:
            tipo = info['tipo_return']
            if tipo != 'void' and not self.retorno:
                print(f"Error: Funcion debe devolver valor.\nFuncion: {self.funcion_actual}")

        self.gen.cuadruplos.agregar('ENDF', None, None, None)
        self.funcion_actual = None

    def traduc_call(self, nom_func, argumentos):
        # Traducir llamada a funcion
        num_param = 1
        for arg_dir in argumentos:
            self.gen.cuadruplos.agregar('PARAM', arg_dir, None, num_param)
            num_param += 1

        self.gen.cuadruplos.agregar('GOSUB', nom_func, None, None)
    
    def traduc_return(self, dir_result=None):
        # Traducir return
        self.retorno = True
        if dir_result is not None:
            self.gen.cuadruplos.agregar('return', dir_result, None, None)
        else:
            self.gen.cuadruplos.agregar('return', None, None, None)
    
    def validar_return(self, tipo_exp, valor):
        # Validar tipo de return
        info = self.directorio.buscar(self.funcion_actual)
        if info is None:
            print(f"Error: return fuera de funcion")
            return
        
        tipo_func = info['tipo_return']
        if tipo_func == 'void':
            if valor:
                print(f"Error: funcion void no devuelve valor.\nFuncion: {self.funcion_actual}")
        else:
            if not valor:
                print(f"Error: Funcion debe devolver valor.\nFuncion: {self.funcion_actual}")
            elif not self.cubo.asignacion_valida(tipo_func, tipo_exp):
                print(f"Error: Type Mismatch."
                      f"Tipo obtenido: {tipo_exp}"
                      f"Tipo esperado: {tipo_func}."
                      f"Funcion: {self.funcion_actual}")
    
    def iniciar_main(self):
        # Traducir main
        self.pos_goto_main = self.gen.cuadruplos.agregar('GOTO', None, None, None)
    
    def marcar_main(self):
        # Marcar inicio de main para generar el cuádruplo
        inicio_main = len(self.gen.cuadruplos)
        self.gen.cuadruplos.actualizar_result(self.pos_goto_main, inicio_main)


# Prueba

if __name__ == "__main__":
    traductor = Traductor()

    print(" PRUEBA 1: a + b * c")
    traductor.proces_operando('a', 'int')
    traductor.proces_operador('+')
    traductor.proces_operando('b', 'int')
    traductor.proces_operador('*')
    traductor.proces_operando('c', 'int')
    result, tipo = traductor.fin_expresion()
    print(f"Resultado: {result}, (Tipo: {tipo})")
    print("Cuadruplos:")
    print(traductor.gen.cuadruplos)

    traductor.gen.limpiar()
    print("\n PRUEBA 2: (a + b) * c")
    traductor.proces_operando('a', 'int')
    traductor.proces_operador('+')
    traductor.proces_operando('b', 'int')
    traductor.proces_parentesisC()
    traductor.proces_operador('*')
    traductor.proces_operando('c', 'int')
    result, tipo = traductor.fin_expresion()
    print(f"Resultado: {result}, (Tipo: {tipo})")
    print("Cuadruplos:")
    print(traductor.gen.cuadruplos)

    traductor.gen.limpiar()
    print("\n PRUEBA 3: a > b == c")
    traductor.proces_operando('a', 'int')
    traductor.proces_operador('>')
    traductor.proces_operando('b', 'int')
    traductor.proces_operador('==')
    result, tipo = traductor.fin_expresion()
    print(f"Resultado: {result}, (Tipo: {tipo})")
    print("Cuadruplos:")
    print(traductor.gen.cuadruplos)

