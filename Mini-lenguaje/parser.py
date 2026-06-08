import ply.yacc as yacc
from lexico import tokens, lexico
from semantica import DirectorioFunciones, TablaVariables, Generar_Codigo, CuboSemantico
from traductor import Traductor
from MV import Memoria, MaquinaVirtual

directorio = DirectorioFunciones()
tabla_vars = TablaVariables()
traductor = Traductor(tabla_vars, directorio)
funcion_actual = None
parametros_actuales = []

precedence = (
    ('left', 'IGUAL', 'NO_IGUAL', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMENOS'),
)

def p_program(p):
    '''
    programa : PROGRAM ID DOS_PUNTOS inicio_program vars lista_funcs main_inicio START body END
    '''
    print("Programa valido")
    print(f" Nombre: {p[2]}")

    print("TABLA CONSTANTES")
    print(tabla_vars.dir_cte)
    print("CUADRUPLOS")
    if len(traductor.gen.cuadruplos) == 0:
        print(" No se generaron cuadruplos")
    else:
        print(traductor.gen.cuadruplos)

    p[0] = ('program', p[2])

def p_inicio_program(p):
    '''
    inicio_program :
    '''
    traductor.iniciar_main()

def p_main_inicio(p):
    '''
    main_inicio :
    '''
    # Traducir inicio de main
    traductor.marcar_main()

def p_lista_funcs(p):
    '''
    lista_funcs : func lista_funcs
                | empty
    '''
    p[0] = None

def p_func(p):
    '''
    func : VOID ID inicio_func PARENT_A parametros PARENT_C vars START body END
         | INT ID inicio_func PARENT_A parametros PARENT_C vars START body END
         | FLOAT ID inicio_func PARENT_A parametros PARENT_C vars START body END
    '''
    global funcion_actual
    if len(p) > 2:
        tipo_return = p[1]
        parametros = p[5]
        info = directorio.buscar(funcion_actual)
        info['parametros'] = parametros
        info['num_parametros'] = len(parametros)
        traductor.finalizar_func()
        print("DIRECTORIO DE FUNCIONES:")
        print(directorio.funciones)
        tabla_vars.salida_ambito()
        funcion_actual = None
    p[0] = None

def p_inicio_func(p):
    '''
    inicio_func :
    '''
    global funcion_actual
    funcion_actual = p[-1] # ID funcion
    traductor.funcion_actual = funcion_actual
    tipo_return = p[-2] # tipo de retorno (VOID, INT, FLOAT)
    directorio.agregar(funcion_actual, tipo_return, [])
    inicio_func = traductor.iniciar_func(funcion_actual)
    directorio.actualizar_inicio(funcion_actual, inicio_func)
    tabla_vars.entrada_ambito()

def p_parametros(p):
    '''
    parametros : tipo ID mas_parametros
               | empty
    '''
    if len(p) == 4:
        lista = [(p[2], p[1])] + (p[3] if p[3] else [])
        for nom_param, tipo_param in lista:
            dir_param = tabla_vars.nueva_var_p(nom_param, funcion_actual)
            tabla_vars.declar_var(nom_param, tipo_param, p.lineno(2))
            tabla_vars.pila_ambitos[-1][nom_param]['direccion'] = dir_param
        p[0] = lista
    else:
        p[0] = []

def p_mas_parametros(p):
    '''
    mas_parametros : COMA tipo ID mas_parametros
                   | empty
    '''
    if len(p) == 5:
        p[0] = [(p[3], p[2])] + (p[4] if p[4] else [])
    else:
        p[0] = []

def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''
    p[0] = p[1]

def p_vars(p):
    '''
    vars : var vars
         | empty
    '''
    p[0] = None

def p_var(p):
    '''
    var : VAR tipo lista_id PUNTO_COMA
    '''
    tipo_var = p[2]
    for nombre in p[3]:
        #tabla_vars.declar_var(nombre, tipo_var, p.lineno(1))
        if tabla_vars.cont_ambitos == 0:
            direccion = tabla_vars.nueva_var_g(nombre)
        else:
            direccion = tabla_vars.nueva_var_l(nombre, tabla_vars.cont_ambitos)
        
        tabla_vars.declar_var(nombre, tipo_var, p.lineno(1))
        # Se guarda la direccion virtual
        tabla_vars.pila_ambitos[-1][nombre]['direccion'] = direccion

    print(f" Variable(s): {p[3]} tipo {p[2]}")
    p[0] = None

def p_lista_id(p):
    '''
    lista_id : ID
             | ID COMA lista_id
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_body(p):
    '''
    body : estatuto body
         | empty
    '''
    p[0] = None

def p_estatuto(p):
    '''
    estatuto : asigna
             | condicion
             | ciclo
             | call
             | print
             | retorno
    '''
    if p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = None

def p_asigna(p):
    '''
    asigna : ID ASIGNA exp PUNTO_COMA
    '''
    result, dir_result, tipo_exp = traductor.fin_expresion()
    traductor.traduc_asignacion(p[1], dir_result, tipo_exp)
    p[0] = ('asigna', p[1], result)

def p_condicion(p):
    '''
    condicion : IF PARENT_A exp_relacion PARENT_C if_condicion estatuto if_fin
              | IF PARENT_A exp_relacion PARENT_C if_condicion estatuto ELSE else_inicio estatuto else_fin
    '''
    result = p[3][0]  # resultado de la condicion
    dir_result = p[3][1]  # direccion del resultado
    tipo_exp = p[3][2]  # tipo del resultado
    if len(p) == 6:
        print(f" If: condicion {result}")
        p[0] = ('if', result, p[5])
    else:
        print(f" If-Else: condicion {result}")
        p[0] = ('if-else', result, p[5], p[7])

def p_if_condicion(p):
    '''
    if_condicion :
    '''
    # Se evalua la exp_relacion
    _, dir_result, _, = p[-2] # exp_relacion contiene el resultado, su direccion y tipo
    label_fin = traductor.nueva_etiqueta()
    traductor.gen.cuadruplos.agregar('GOTOF', dir_result, None, label_fin)

    traductor.gen.saltos.push(label_fin)

def p_if_fin(p):
    '''
    if_fin :
    '''
    # Fin del cuerpo de la condicional. Se saca el salto de la pila
    label_fin = traductor.gen.saltos.pop()
    traductor.gen.cuadruplos.agregar('LABEL', None, None, label_fin)

def p_else_inicio(p):
    '''
    else_inicio :
    '''
    # Se crea la etiqueta para el salto del else
    label_else = traductor.gen.saltos.pop()
    label_fin = traductor.nueva_etiqueta()
    traductor.gen.cuadruplos.agregar('GOTO', None, None, label_fin)
    traductor.gen.cuadruplos.agregar('LABEL', None, None, label_else)
    traductor.gen.saltos.push(label_fin)

def p_else_fin(p):
    '''
    else_fin :
    '''
    # Fin del cuerpo del else. Se saca el salto de la pila
    label_fin = traductor.gen.saltos.pop()
    traductor.gen.cuadruplos.agregar('LABEL', None, None, label_fin)

# def p_ciclo(p):
#     '''
#     ciclo : WHILE PARENT_A exp_relacion PARENT_C body
#     '''
#     label_inicio, label_fin = traductor.traduc_while_inicio()
#     result = p[3][0]  # resultado de la condicion
#     dir_result = p[3][1]  # direccion del resultado
#     tipo_exp = p[3][2]  # tipo del resultado

#     traductor.traduc_while_condicion(dir_result, label_inicio, label_fin)
#     traductor.finalizar_while(label_inicio, label_fin)
#     print(f" While: condicion {result}")
#     p[0] = ('while', result, p[5])

def p_ciclo(p):
    '''
    ciclo : WHILE while_inicio PARENT_A exp_relacion PARENT_C while_condicion estatuto while_fin
    '''
    print(f" While: condicion {p[4][0]}")

def p_while_inicio(p):
    '''
    while_inicio : 
    '''
    # Crear etiqueta de inicio
    label_inicio = traductor.nueva_etiqueta()
    traductor.gen.cuadruplos.agregar('LABEL', None, None, label_inicio)
    traductor.gen.saltos.push(label_inicio)

def p_while_condicion(p):
    '''
    while_condicion :
    '''
    # Se evalua la exp_relacion
    _, dir_result, _, = p[-2] # exp_relacion contiene el resultado, su direccion y tipo
    label_fin = traductor.nueva_etiqueta()
    traductor.gen.cuadruplos.agregar('GOTOF', dir_result, None, label_fin)

    traductor.gen.saltos.push(label_fin)

def p_while_fin(p):
    '''
    while_fin :
    '''
    # Fin del cuerpo de la condicional. Se sacan los saltos de la pila
    label_fin = traductor.gen.saltos.pop()
    label_inicio = traductor.gen.saltos.pop()
    traductor.gen.cuadruplos.agregar('GOTO', None, None, label_inicio)
    traductor.gen.cuadruplos.agregar('LABEL', None, None, label_fin)

def p_call(p):
    '''
    call : ID PARENT_A lista_exp PARENT_C PUNTO_COMA
    '''
    nombre_func = p[1]
    args = p[3] if p[3] else []

    dirs_agrs = []
    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2:
            dirs_agrs.append(arg[1]) # valor y direccion
        else:
            dirs_agrs.append(arg)

    info = directorio.buscar(nombre_func)
    if info:
        args_esperados = info['num_parametros']
        args_recibidos = len(args)
        if args_esperados != args_recibidos:
            print(f"Error: funcion '{nombre_func}' esperaba "
                  f"{args_esperados} argumento(s) pero recibio {args_recibidos}")
        else:
            traductor.traduc_call(nombre_func, dirs_agrs)
    else:
        print(f"Error: funcion '{nombre_func}' no declarada")
    print(f" Call: {p[1]}({p[3]})")
    p[0] = ('call', p[1], p[3])

def p_print(p):
    '''
    print : PRINT PARENT_A exp PARENT_C PUNTO_COMA
    '''
    result, dir_result, tipo_exp = traductor.fin_expresion()
    traductor.gen.cuadruplos.agregar('print', dir_result, None, None)
    print(f" Print: {result}")
    p[0] = ('print', result)

def p_retorno(p):
    '''
    retorno : RETURN exp PUNTO_COMA
            | RETURN PUNTO_COMA
    '''
    if len(p) == 4:
        result, dir_result, tipo_exp = traductor.fin_expresion()
        traductor.validar_return(tipo_exp, valor=True)
        traductor.traduc_return(dir_result)
        p[0] = ('return', result)
    else:
        traductor.validar_return('void', valor=False)
        traductor.traduc_return(None)
        print(f" Return")
        p[0] = ('return', None)

def p_lista_exp(p):
    '''
    lista_exp : exp mas_exp
              | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + (p[2] if p[2] else [])
    else:
        p[0] = []

def p_mas_exp(p):
    '''
    mas_exp : COMA exp mas_exp
            | empty
    '''
    if len(p) == 4:
        p[0] = [p[2]] + (p[3] if p[3] else [])
    else:
        p[0] = []

def p_exp(p):
    '''
    exp : termino sig_exp
    '''
    p[0] = p[1]

def p_sig_exp(p):
    '''
    sig_exp : MAS termino sig_exp
            | MENOS termino sig_exp
            | empty
    '''
    if len(p) == 4:
        traductor.proces_operador(p[1])
        #p[0] = (p[1], p[2], p[3])
    else:
        p[0] = None

def p_termino(p):
    '''
    termino : factor sig_termino
    '''
    p[0] = p[1]

def p_sig_termino(p):
    '''
    sig_termino : MULT factor sig_termino
                | DIV factor sig_termino
                | empty
    '''
    if len(p) == 4:
        traductor.proces_operador(p[1])
        #p[0] = (p[1], p[2], p[3])
    else:
        p[0] = None

def p_factor(p):
    '''
    factor : ID
           | ID PARENT_A lista_exp PARENT_C
           | CTE_INT
           | CTE_FLOAT
           | NULL
           | PARENT_A exp PARENT_C
           | MENOS factor %prec UMENOS
    '''
    if len(p) == 2:
        if p.slice[1].type == 'ID':
            nombre = p[1]
            var_info = tabla_vars.buscar_var(nombre)
            tipo = var_info['tipo'] if var_info else 'int'
            # Obtener direccion virtual
            direccion = tabla_vars.obtener_dir_var(nombre, tabla_vars.cont_ambitos, funcion_actual)
            traductor.proces_operando(nombre, tipo, direccion)
            p[0] = (nombre, direccion)
        elif p.slice[1].type == 'CTE_INT':
            direccion = tabla_vars.nueva_cte(p[1])
            traductor.proces_operando(p[1], 'int', direccion)
            p[0] = (p[1], direccion)
        elif p.slice[1].type == 'CTE_FLOAT':
            direccion = tabla_vars.nueva_cte(p[1])
            traductor.proces_operando(p[1], 'float', direccion)
            p[0] = (p[1], direccion)
        elif p.slice[1].type == 'NULL':
            traductor.proces_operando(p[1], 'null')
            p[0] = 'null'
        else:
            p[0] = p[1]
    elif len(p) == 4 and p[1] == '(':
        # Expresion entre parentesis
        p[0] = p[2]
    elif len(p) == 3:
        # - factor (UMENOS)
        traductor.proces_umenos()
        p[0] = ('-', p[2])
    elif len(p) == 5:
        nombre_func = p[1]
        args = p[3] if p[3] else []
        dirs_agrs = []
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                dirs_agrs.append(arg[1]) # valor y direccion
            else:
                dirs_agrs.append(arg)
        info = directorio.buscar(nombre_func)
        if info:
            traductor.traduc_call(nombre_func, dirs_agrs)
            traductor.proces_operando(10000, info['tipo_return'], 10000)
            p[0] = (nombre_func, 10000)
        else:
            print(f"Error: funcion '{nombre_func}' no declarada")

def p_exp_relacion(p):
    '''
    exp_relacion : exp op_relacion exp
    '''
    traductor.proces_operador(p[2])
    result, dir_result, tipo = traductor.fin_expresion()
    p[0] = (result, dir_result, tipo)

def p_op_relacion(p):
    '''
    op_relacion : IGUAL
                | NO_IGUAL
                | MENOR
                | MAYOR
                | MENOR_IGUAL
                | MAYOR_IGUAL
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    if p:
        print(f"Error sintactico: token '{p.value}' inesperado en linea {p.lineno}")
    else:
        print("Error sintactico: fin de archivo inesperado")

parser = yacc.yacc()

# Prueba
if __name__ == "__main__":
    test_code = """
    program test:
        var int x, y, z;
        
        start
            x = 5;
            y = 10;
            z = x + y * 2;
            print(z);
            
            if (x < y)
                print(x);
            else
                print(y);
            
            return z;
        end
    """
    
    print("=== INICIO DEL ANÁLISIS ===\n")
    result = parser.parse(test_code, lexer=lexico)
    print("\n=== FIN DEL ANÁLISIS ===")