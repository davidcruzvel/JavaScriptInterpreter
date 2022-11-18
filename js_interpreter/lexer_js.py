from tokens import *
    
___all__ = ["Lexer"] # nombre para importar el archivo

def Lexer(data: str) -> TokenInfo: # clase del Lexer
    pos = 0
    auxBool = False
    while pos < len(data): # mientras la posicion sea menor a la longitud del string donde esta todo el codigo enviado
        for tokenId in Token: # evaluar cada token de la clase Token
            if match := tokenId.value.match(data, pos): # si el token coincide a partir del caracter de la posicion actual
                pos = match.end(0) # la posicion va a ser el final del token
                if(str((Token.COMMENT).value.match(data, pos)) != "None"): # si el token es un comentario
                    try:
                        dataaux = ""
                        while (dataaux != "\n"): # proceso para ir al final del token del comentario
                            pos = pos+1
                            dataaux = data[pos]
                    except:
                        break
                if tokenId == Token.WHITESPACE: # que ignore los espacios en blanco o comentarios
                    break
                # estas condicionales existen ya que al declarar un token doble del cual uno solo esta declarado toma este y da un error
                # por lo que hay que manejar cada uno de esos tokens de forma manual
                elif(str(tokenId.name) == "ASSIGN" and str((Token.ASSIGN).value.match(data, pos)) != "None"): # si el token es ==
                    yield TokenInfo((Token.EQUAL).name, "==")
                    auxBool = True
                elif(str(tokenId.name) == "LARGE" and str((Token.ASSIGN).value.match(data, pos)) != "None"): # si el token es >=
                    yield TokenInfo((Token.LARGEEQ).name, ">=")
                    auxBool = True
                elif(str(tokenId.name) == "SMALL" and str((Token.ASSIGN).value.match(data, pos)) != "None"): # si el token es <=
                    yield TokenInfo((Token.SMALLEQ).name, "<=")
                    auxBool = True
                elif(str(tokenId.name) == "NOT" and str((Token.ASSIGN).value.match(data, pos)) != "None"): # si el token es !=
                    yield TokenInfo((Token.NOTEQ).name, "!=")
                    auxBool = True
                elif(auxBool): # si entro a uno de los operadores ==, >=, <= y != debe entrar aca ya que se saltara una posicion
                    auxBool = False
                    break
                else: # agregando token
                    yield TokenInfo(tokenId.name, match.group(0))
                break
        else:
            # en caso de que el patron no coincide se debe mandar el caracter como tipo ilegal
            yield TokenInfo(ILLEGAL, data[pos])
            pos += 1
    else:
        # en el parser se lee el token dos veces en cada iteracion
        # una para el token actual y otra para el siguiente token
        # para entregarlo enviandolo dos veces al EOF
        yield TokenInfo(EOF, '\x00')
        yield TokenInfo(EOF, '\x00')
