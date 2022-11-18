from tokens import *
from nodes import *
from lexer_js import Lexer

___all__ = ["Parser"] # nombre para importar el archivo

class Parser:
    def __init__(self, lex):
        self.lex = lex
        self.program = []
        self.curr_token = None
        self.next_token = None
        self.update() # inicializar self.next_token
        self.update() # inicializar self.curr_token

    def update(self):
        self.curr_token = self.next_token
        self.next_token = next(self.lex)

    def is_next(self, t):
        if self.next_token != t:
            raise AssertionError(f"expected {t} but got {self.next_token.name}")
        self.update()

    def __iter__(self):
        # para que la clase sea iterable
        return self

    def __next__(self) -> Statement:    
        # Este es el generador que debe llamarse para obtener la declaracion, esta es la clase main
        while self.curr_token.name != EOF:
            if statement := self.parse_statement():
                return statement
        else:
            return EOF

    def parse_expression(self, precedence: Priority) -> Expression: # determinar que tipo de token es, si es un datatype, identificador, unary o un grupo
        expression = self.parse_datatypes() or \
                    self.parse_identifier() or \
                    self.parse_unary() or \
                    self.parse_group()
        if expression == None:
            raise SyntaxError(f"operand '{self.curr_token.value}' not defined")
        while self.next_token != Token.SEMICOLON and \
            precedence.value <= get_precedence(self.next_token).value:
            if new_expression := self.parse_infix_expression(expression):
                expression = new_expression
            else:
                break
        return expression

    def parse_datatypes(self) -> Expression: # retorna que tipo de datos es el del token si no coincide retorna None
        datatypes = [
            Token.INT.name,
            Token.FLOAT.name,
            Token.TRUE.name,
            Token.FALSE.name,
            Token.STRING.name,
        ]
        if self.curr_token.name in datatypes:
            return Literal(self.curr_token.name, self.curr_token.value)
    
    def parse_identifier(self):
        if self.curr_token == Token.ID:
            return Identifier(self.curr_token.value)
   
    def parse_unary(self): # determina si es un token unary es decir uno de prioridad alta
        if self.curr_token.name in [Token.NOT, Token.MINUS]:
            operator = self.curr_token.value
            precedence = get_precedence(self.curr_token)
            self.update()
            right = self.parse_expression(Priority.HIGHER)
            return PrefixExpression(operator, right)
        elif self.curr_token.name == Token.LPAREN:
            self.update()
            expression = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.RPAREN)
            return expression

    def parse_group(self): # cuando una expresion esta entre parentesis se entra a esta funcion num = (12+3)
        if self.curr_token.name == Token.LPAREN:
            self.update()
            expression = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.RPAREN)
            return expression

    def parse_statement(self) -> Statement:
        if self.curr_token == ILLEGAL:
            raise SyntaxError(f"invalid input: {self.curr_token.value}")
        return self.parse_let_statement() or \
                self.parse_assign_statement() or \
                self.parse_consolelog_statement() or \
                self.parse_if_expression() or \
                self.parse_for_expression() or \
                self.parse_while_expression() or \
                self.parse_do_while_expression() or \
                self.parse_expression_statement()
                
    def parse_expression_statement(self):
            expression = self.parse_expression(Priority.LOWEST)
            if self.next_token == Token.SEMICOLON:
                self.update()
                self.update()
            return expression

    def parse_let_statement(self) -> Statement: # si es una declaracion let
        if self.curr_token == Token.LET:
            self.is_next(Token.ID)
            variable = self.curr_token.value
            self.is_next(Token.ASSIGN)
            self.update()
            value = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.SEMICOLON)
            self.update()
            return LetStatement(variable, value)
            
    def parse_assign_statement(self) -> Statement: # si es una declaracion de asignacion "="
        if self.curr_token == Token.ID:
            variable = self.curr_token.value
            self.is_next(Token.ASSIGN)
            self.update()
            value = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.SEMICOLON)
            self.update()
            return AssignStatement(variable, value)

    def parse_block_Statements(self) -> Statement: # cuando se encuentra un bloque es decir lo que este dentro de {}
        self.is_next(Token.LBRACE)
        self.update()
        block = []
        while self.curr_token != Token.RBRACE:
            stmt = self.parse_statement()
            block.append(stmt)
        else:
            self.update()
        return BlockStatement(block)

    def parse_consolelog_statement(self) -> Statement: # para la impresion de datos console.log()
        if self.curr_token == Token.CONSOLELOG:
            state = self.curr_token.value
            self.is_next(Token.LPAREN)
            self.update()
            value = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.RPAREN)
            self.is_next(Token.SEMICOLON)
            self.update()
            return ConsolelogStatement(state, value)

    def parse_if_expression(self) -> Expression: # para la evaluacion de un if
        if self.curr_token == Token.IF:
            self.is_next(Token.LPAREN)
            self.update()
            condition = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.RPAREN)
            true_stmt = self.parse_block_Statements()
            false_stmt = None
            if self.curr_token == Token.ELSE:
                false_stmt = self.parse_block_Statements()
            return IfStatement(condition, true_stmt, false_stmt)

    def parse_for_expression(self) -> Expression: # para la evaluacion de un for
        if self.curr_token == Token.FOR:
            self.is_next(Token.LPAREN)
            self.update()
            if self.curr_token == Token.LET:
                self.is_next(Token.ID)
                variable = self.curr_token.value
                self.is_next(Token.ASSIGN)
                self.update()
                value = self.parse_expression(Priority.LOWEST)
                self.is_next(Token.SEMICOLON)
                self.update()
            condition = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.SEMICOLON)
            self.update()
            if self.curr_token == Token.ID:
                afterthought = self.curr_token.value
                self.is_next(Token.ASSIGN)
                self.update()
                expr = self.parse_expression(Priority.LOWEST)
                self.update()
            block = self.parse_block_Statements()
            return ForStatement(variable, value, condition, afterthought, expr, block)

    def parse_while_expression(self) -> Expression:  # para la evaluacion de un while
        if self.curr_token == Token.WHILE:
            self.is_next(Token.LPAREN)
            self.update()
            condition = self.parse_expression(Priority.LOWEST)
            self.is_next(Token.RPAREN)
            block = self.parse_block_Statements()
            return WhileStatement(condition, block)

    def parse_do_while_expression(self) -> Expression:  # para la evaluacion de un do while
        if self.curr_token == Token.DO:
            block = self.parse_block_Statements()
            if self.curr_token == Token.WHILE:
                self.is_next(Token.LPAREN)
                self.update()
                condition = self.parse_expression(Priority.LOWEST)
                self.is_next(Token.RPAREN)
                self.is_next(Token.SEMICOLON)
                self.update()
                return DoWhileStatement(condition, block)
            else:
                raise SyntaxError("expected while")

    def parse_infix_expression(self, left: Expression) -> Expression: # determinar que la expresion es del tipo variable operador variable
        infix_list = [
            # operadores aritmeticos
            Token.PLUS,   Token.MINUS,   Token.DIVIDE,
            Token.TIMES,  Token.MODULUS, Token.POWER,
            # operadores condicionales
            Token.EQUAL,  Token.LARGE,   Token.LARGEEQ,
            Token.SMALL,  Token.SMALLEQ, Token.NOTEQ,
            # operadores logicos
            Token.AND, Token.OR,
        ]
        if self.next_token.name in infix_list:
            self.update()
            operator = self.curr_token.value
            precedence = get_precedence(self.curr_token)
            self.update()
            right = self.parse_expression(precedence)
            return InfixExpression(left, operator, right)
