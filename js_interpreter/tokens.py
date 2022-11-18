from enum import Enum
import re
from collections import namedtuple

TokenInfo = namedtuple("Tokens", ["name", "value"]) # declaracion de la variable TokenInfo que es una tupla

class NewEnum(Enum): # clase NewEnum
    def __eq__(self, b) -> bool:
        if isinstance(b, str):
            return self.name == b
        else:
            return  self.name == b.name
    def __hash__(self):
        return id(self.name)

ILLEGAL = 'ILLEGAL' # caracter ilegal
EOF     = 'EOF' # caracter eof

class Token(NewEnum): # clase con la declaracion de los tokens
    # tipos de datos
    STRING  = re.compile(r'(\".*\")|(\'.*\')')
    FLOAT   = re.compile(r'\d+\.\d+')
    INT     = re.compile(r'\d+')
    TRUE    = re.compile(r'true')
    FALSE   = re.compile(r'false')
    # simbolos agrupacion
    LPAREN  = re.compile(r'\(')
    RPAREN  = re.compile(r'\)')
    LBRACE  = re.compile(r'\{')
    RBRACE  = re.compile(r'\}')
    LSQUARE = re.compile(r'\[')
    RSQUARE = re.compile(r'\]')
    # operador de asignacion
    ASSIGN  = re.compile(r'=')
    # operadores aritmeticos
    PLUS    = re.compile(r'\+')
    MINUS   = re.compile(r'\-')
    TIMES   = re.compile(r'\*')
    DIVIDE  = re.compile(r'/')
    MODULUS = re.compile(r'%')
    POWER   = re.compile(r'\^')
    # operadores logicos
    AND     = re.compile(r'&&')
    OR      = re.compile(r'\|\|')
    NOT     = re.compile(r'!')
    # operadores condicionales
    EQUAL   = re.compile(r'==')
    SMALL   = re.compile(r'<')
    SMALLEQ = re.compile(r'<=')
    LARGE   = re.compile(r'>')
    LARGEEQ = re.compile(r'>=')
    NOTEQ   = re.compile(r'!=')
    # palabras reservadas
    IF      = re.compile(r'if')
    ELSE    = re.compile(r'else')
    FOR   = re.compile(r'for')    
    WHILE   = re.compile(r'while')
    DO      = re.compile(r'do')
    LET     = re.compile(r'let|var|const')
    CONSOLELOG   = re.compile(r'console.log')
    # variables
    ID      = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
    # comentarios
    COMMENT = re.compile(r'//.*')
    # delimitadores
    COMMA      = re.compile(r',')
    SEMICOLON  = re.compile(r';')
    WHITESPACE = re.compile(r'(\t|\n|\s|\r)+')

Priority = NewEnum("priority", [ # declaracion de las prioridades
    "LOWEST",
    "LOWER",
    "LOW",
    "HIGH",
    "HIGHER",
    "HIGHEST",
])

precedence =  {
    Token.EQUAL.name : Priority.LOWER,       # ==
    Token.NOTEQ.name : Priority.LOWER,       # !=
    Token.SMALL.name : Priority.LOW,         # <
    Token.LARGE.name : Priority.LOW,         # >
    Token.PLUS.name  : Priority.HIGH,        # +
    Token.MINUS.name : Priority.HIGH,        # -
    Token.TIMES.name : Priority.HIGHER,      # *
    Token.DIVIDE.name: Priority.HIGHER,      # /
    Token.LPAREN.name: Priority.HIGHEST,     # ()
}

def get_precedence(token: Token) -> Priority:
    return precedence.get(token.name, Priority.LOWEST) # retornar el nombre del token con su prioridad
