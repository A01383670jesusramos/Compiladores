import ply.lex as lex # type: ignore

# Tokens
tokens = [
    'PROGRAM', 'FUNC', 'BODY', 'START', 'END',
    'IF', 'ELSE', 'WHILE', 'CALL', 'PRINT', 'INT',
    'FLOAT', 'NULL', 'VOID', 'RETURN', 'VAR', 'ID', 'CTE_INT',
    'CTE_FLOAT', 'ASIGNA', 'MAS', 'MENOS', 'MULT', 'DIV',
    'IGUAL', 'NO_IGUAL', 'MENOR', 'MAYOR', 'MENOR_IGUAL',
    'MAYOR_IGUAL', 'PARENT_A', 'PARENT_C', 'CORCH_A', 'CORCH_C',
    'LLAVE_A', 'LLAVE_C', 'PUNTO_COMA', 'COMA', 'DOS_PUNTOS'
]

# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'func': 'FUNC',
    'body': 'BODY',
    'start': 'START',
    'end': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'call': 'CALL',
    'print': 'PRINT',
    'int': 'INT',
    'float': 'FLOAT',
    'null': 'NULL',
    'void': 'VOID',
    'return': 'RETURN',
    'var': 'VAR'
}

# Simbolos y operadores
t_ASIGNA = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_IGUAL = r'=='
t_NO_IGUAL = r'!='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_PARENT_A = r'\('
t_PARENT_C = r'\)'
t_CORCH_A = r'\['
t_CORCH_C = r'\]'
t_LLAVE_A = r'\{'
t_LLAVE_C = r'\}'
t_PUNTO_COMA = r';'
t_COMA = r','
t_DOS_PUNTOS = r':'

# Definir flotantes
def t_CTE_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# Definir enteros
def t_CTE_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Definir identificadores y si son palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Checar si es una palabra reservada
    return t

# Ingorar espacios y tabulaciones
t_ignore = ' \t'

# Manejar nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejar errores de lexico
def t_error(t):
    print(f"Error lexico: Caracter '{t.value[0]}' invalido en linea {t.lexer.lineno}")
    t.lexer.skip(1)

lexico = lex.lex()


# Prueba del lexer
if __name__ == "__main__":
    test_code = """
    program main
      var int x, y;

      start
        x = 5;
        y = 10;
      end
    """
    lexico.input(test_code)
    for token in lexico:
        print(f" {token.type}: '{token.value}' (linea {token.lineno})")