import sys
from lexico import lexico
from parser import parser

def main():
    

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"Iniciando: {filename}")
        print("\n")
        result = parser.parse(code, lexer=lexico)
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