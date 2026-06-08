import sys
from lexico import lexico
from parser import parser, traductor, directorio, tabla_vars
from MV import Memoria, MaquinaVirtual

def main():
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"Iniciando: {filename}")
        print("\n")
        result = parser.parse(code, lexer=lexico)
        print("\n")
        print("TABLA DE CONSTANTES")
        mem = Memoria()
        for valor, dir in tabla_vars.dir_cte.items():
            mem.escribir_cte(dir, valor)
        print(mem.memoria["cte"])
        mv = MaquinaVirtual(traductor.gen.cuadruplos.obtener_todos(), mem, directorio.funciones)
        for valor, dir_cte in tabla_vars.dir_cte.items():
            mem.memoria["cte"][dir_cte] = valor
        mv.ejecutar()
        print("RETURN = ", mv.valor_retorno)
        #print(tabla_vars.dir_cte)
        print("\n")

        if result is not None:
            print("Analisis exitoso.")
        else:
            print("El analisis presenta advertencias.")
    
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()