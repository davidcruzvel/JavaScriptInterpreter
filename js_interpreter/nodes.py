from typing import List
from tokens import *

# prototipos de clases
class Node: ...
class Statement(Node): ...
class Expression(Node): ...
storage = {} # variable storage la cual contendra las declaraciones

class Identifier(Expression): # clase para el proceso de cuando es un identificador o sea una declaracion de una variable
    def __init__(self, name): # inicializacion
        self.name = name
    def __repr__(self) -> str: # retorno de la representacion
        return self.name
    def eval(self): # ejecucion del proceso
        if self.name in storage:
            return storage[self.name]
        else:
            raise NameError(f"'{self.name}' is not defined")

class Literal(Expression): # clase para el proceso de deteccion del tipo de dato
    def __init__(self, typ: str, value: str): # inicializacion
        self.type = typ
        self.value = value
    def __repr__(self) -> str: # retorno de la representacion
        return str(self.value)
    def get_type(self) -> str:
        # retorna si es booleano
        if self.type == Token.FALSE or self.type == Token.TRUE:
            return "bool"
        return self.type.lower()
    def type_casting(self):
        # convesion del valor al tipo de dato
        if self.type == Token.INT:
            return int(self.value)
        elif self.type == Token.FLOAT:
            return float(self.value)
        elif self.type == Token.STRING:
            return str(self.value)[1:-1]
        elif self.type == Token.TRUE:
            return True
        elif self.type == Token.FALSE:
            return False
        else:
            return None
    def eval(self): # ejecucion del proceso 
        try:
            out = self.type_casting()
        except ValueError:
            raise ValueError(f"Error converting {self.value} to {self.type}")
        return out

class LetStatement(Statement): # clase para el proceso de let
    def __init__(self, name: Identifier, expr: Expression): # inicializacion
        self.name = name
        self.expr = expr
    def __repr__(self) -> str: # retorno de la representacion
        return f"(let ({self.name}) ({self.expr}))"
    def eval(self): # ejecucion del proceso
        if self.name in storage:
            raise NameError(f'"{self.name}" already defined')
        storage[self.name] = self.expr.eval()

class AssignStatement(Statement): # clase para el proceso de una asignacion
    def __init__(self, name: str, expr: Expression): # inicializacion
        self.name = name
        self.expr = expr
    def __repr__(self) -> str: # retorno de la representacion
        return f"(set ({self.name}) ({self.expr}))"
    def eval(self): # ejecucion del proceso
        if self.name not in storage:
            raise NameError(f'"{self.name}" not defined')
        storage[self.name] = self.expr.eval()

class BlockStatement(Statement): # clase para el proceso de los bloques, lo que esta dentro de los {}
    def __init__(self, statements: List[Statement]): # inicializacion
        self.statements = statements
    def __repr__(self) -> str: # retorno de la representacion
        data = ""
        for x in self.statements:
            data += x.__repr__()
        return f"({data})"
    def eval(self): # ejecucion del proceso
        for x in self.statements:
            data = x.eval()

class ConsolelogStatement(Statement): # clase para el proceso console.log()
    def __init__(self, state, value: Expression): # inicializacion
        self.state = state
        self.value = value
    def __repr__(self) -> str: # retorno de la representacion
        return f"(console.log({self.value}))"
    def eval(self): # ejecucion del proceso
        print(self.value.eval())

class IfStatement(Statement): # clase para el proceso del if
    def __init__(self, condition: Expression, true_stmt: BlockStatement, false_stmt: BlockStatement): # inicializacion
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt
    def __repr__(self) -> str: # retorno de la representacion
        if self.false_stmt == None:
            return f"(if ({self.condition}) ({self.true_stmt}))"
        else:
            return f"(if ({self.condition}) ({self.true_stmt}) ({self.false_stmt}))"
    def eval(self): # ejecucion del proceso
        if self.condition.eval():
            self.true_stmt.eval()
        else:
            self.false_stmt.eval() if self.false_stmt else None

class ForStatement(Statement): # clase para el proceso del for
    def __init__(self, name: Identifier, expr1: Expression, condition: Expression, afterthought: str, expr2: Expression, stmt: BlockStatement): # inicializacion
        self.name = name
        self.expr1 = expr1
        self.condition = condition
        self.afterthought = afterthought
        self.expr2 = expr2
        self.stmt = stmt
    def __repr__(self) -> str: # retorno de la representacion
        return f"(for (let ({self.name}) ({self.expr1});({self.condition});({self.afterthought}) ({self.expr2})) ({self.stmt}))"
    def eval(self): # ejecucion del proceso
        if self.name not in storage:
            storage[self.name] = self.expr1.eval()
        if self.afterthought not in storage:
            raise NameError(f'"{self.name}" not defined')
        else:
            while self.condition.eval():
                storage[self.name] = self.expr2.eval()
                self.stmt.eval()

class WhileStatement(Statement): # clase para el proceso del while
    def __init__(self, condition: Expression,  true_stmt: Statement): # inicializacion
        self.condition = condition
        self.stmt = true_stmt
    def __repr__(self) -> str: # retorno de la representacion
        return f"(while ({self.condition}) ({self.stmt}))"
    def eval(self): # ejecucion del proceso
        while self.condition.eval():
            self.stmt.eval()

class DoWhileStatement(Statement): # clase para el proceso de do while
    def __init__(self, condition: Expression, stmt: BlockStatement): # inicializacion
        self.condition = condition
        self.stmt = stmt
    def __repr__(self) -> str: # retorno de la representacion
        return f"(do ({self.stmt}) while ({self.condition}))"
    def eval(self): # ejecucion del proceso
        while 1:
            self.stmt.eval()
            if not self.condition.eval():
                break

class InfixExpression(Expression): # clase para el proceso de expresion de tipo a == b, variable operador variable
    def __init__(self, left: Expression, operator: Statement, right: Expression): # inicializacion
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self) -> str: # retorno de la representacion
        return f"(({self.left}) ({self.operator}) ({self.right}))"
    def eval(self): # ejecucion del proceso
        operator = {
            '+' : lambda a,b: a+b,
            '-' : lambda a,b: a-b,
            '*' : lambda a,b: a*b,
            '/' : lambda a,b: a//b,
            '%' : lambda a,b: a%b,
            '^' : lambda a,b: a**b,
            '==' : lambda a,b: a==b,
            '<' : lambda a,b: a<b,
            '>' : lambda a,b: a>b,
            '<=' : lambda a,b: a<=b,
            '>=' : lambda a,b: a>=b,
            '!=' : lambda a,b: a!=b,
            '&&' : lambda a,b: a and b,
            '||' : lambda a,b: a or b,
        }
        try:
            return operator[self.operator](self.left.eval(), self.right.eval())
        except TypeError:
            raise TypeError(f"can't perform {self.operator} between {self.left_type()} and  {self.left_type()}")

class PrefixExpression(Expression): # clase para el proceso de expresion de tipo !a, operador variable
    def __init__(self, operator: Statement, right: Expression): # inicializacion
        self.operator = operator
        self.right = right
    def get_type(self) -> str: # retorna el tipo de dato
        return self.type.right
    def __repr__(self) -> str: # retorno de la representacion
        return f"(({self.operator})({self.right}))"
    def eval(self): # ejecucion del proceso
        operator = {
            '!' : lambda a: not a,
            '-' : lambda a: -a,
        }
        try:
            return operator[self.operator](self.right.eval())
        except TypeError:
            raise TypeError(f"can't perform {self.operator} between {self.left_type()} and  {self.left_type()}")
