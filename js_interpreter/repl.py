from lexer_js import Lexer
from parser_js import Parser
from tokens import *

def interpretor(data: str): # metodo que envia el string lo proceso y retorna el resultado
    lex = Lexer(data) # envio del string con el codigo al lexer para que lo separe por tokens
    parse = Parser(lex) # envio de la devolucion del lexer para el procesado sintactico y devolucion de resultado por parte del parser
    for p in parse: # evluar cada una de las devoluciones del parser
        if p == EOF: # si es error se termina
            break
        p.eval() # retorno del resultado

def repl():
    i = 0
    while True: # mientras sea true ejecutar, o sea un bucle
        try:
            data: str = input(f"[{i}]: ") # leer lo que se escribe en el bash y mandarlo a interpretor
            interpretor(data)
        except EOFError: # en caso de error
            print()
        except KeyboardInterrupt: # al presionar ctrl+c es decir una interrupcion por tecla se imprime el siguiente mensaje y se termina el bucle
            print("closing...")
            break
        except Exception as msg: #en caso de una excepcion
            print(msg)
        finally: # para el conteo de lineas
                i += 1

if __name__ == "__main__": # funcion principal del archivo
    import sys
    from os.path import exists
    if len(sys.argv) < 2: # si no se recibe un parametro es decir un archivo .js entra aca y se abre un bash para probar codigo de JavaScript
        repl() # llamada al metodo repl el cual se ejecutara en bucle
    else: # si se recibe un parametro es decir un archivo .js se procede a poner todo lo que este dentro de este en un string
        file_name = sys.argv[1]
        if not exists(file_name): # si no existe muestra el error
            print(f"{file_name} not found")
            sys.exit(0)
        with open(file_name) as f: # asignacion dentro de un string
            data = f.read()
        interpretor(data) # envio del string al metodo interpretor
