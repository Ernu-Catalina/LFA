import enum

class TokenType(enum.Enum):
    EOF = -1
    DEF = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUMBER = -5
    OPERATOR = -6
    LPAREN = -7
    RPAREN = -8
    COMMA = -9
    IF = -10
    THEN = -11
    ELSE = -12

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = input_text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.input_text):
            self.current_char = None
        else:
            self.current_char = self.input_text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()

            if self.current_char.isdigit() or self.current_char == '.':
                return self.get_number()

            if self.current_char in {'+', '-', '*', '/'}:
                op = self.current_char
                self.advance()
                return Token(TokenType.OPERATOR, op)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.DEF, '=')

            if self.current_char == '?':
                self.advance()
                return Token(TokenType.EXTERN, '?')

            if self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            self.advance()

        return Token(TokenType.EOF, None)

    def get_identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result == 'def':
            return Token(TokenType.DEF, result)
        elif result == 'if':
            return Token(TokenType.IF, result)
        elif result == 'then':
            return Token(TokenType.THEN, result)
        elif result == 'else':
            return Token(TokenType.ELSE, result)
        else:
            return Token(TokenType.IDENTIFIER, result)

    def get_number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result))

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Number({self.value})'

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name})'

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinaryOp({self.left}, {self.op}, {self.right})'

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'FunctionCall({self.name}, {self.args})'

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f'FunctionDef({self.name}, {self.params}, {self.body})'

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f'IfStatement({self.condition}, {self.then_branch}, {self.else_branch})'

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Unexpected token {self.current_token.type}, expected {token_type}')

    def parse(self):
        return self.parse_function()

    def parse_function(self):
        self.eat(TokenType.DEF)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        params = self.parse_params()
        self.eat(TokenType.RPAREN)
        body = self.parse_expression()
        return FunctionDef(name, params, body)

    def parse_params(self):
        params = []
        if self.current_token.type == TokenType.IDENTIFIER:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        return params

    def parse_expression(self):
        if self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        else:
            return self.parse_term()

    def parse_if_statement(self):
        self.eat(TokenType.IF)
        condition = self.parse_expression()
        self.eat(TokenType.THEN)
        then_branch = self.parse_expression()
        self.eat(TokenType.ELSE)
        else_branch = self.parse_expression()
        return IfStatement(condition, then_branch, else_branch)

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('+', '-', '*', '/'):
            op = self.current_token.value
            self.eat(TokenType.OPERATOR)
            node = BinaryOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LPAREN:
                return self.parse_function_call(token.value)
            else:
                return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return node

    def parse_function_call(self, name):
        self.eat(TokenType.LPAREN)
        args = []
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.parse_expression())
        self.eat(TokenType.RPAREN)
        return FunctionCall(name, args)

# Example usage:
text = """
def fib(x)
  if x < 3 then
    1
  else
    fib(x-1)+fib(x-2)

fib(40)
"""

lexer = Lexer(text)
parser = Parser(lexer)

# Debug: Print tokens
print("Tokens:")
while True:
    token = lexer.get_next_token()
    if token.type == TokenType.EOF:
        break
    print(token)

# Reinitialize lexer for parsing
lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()
print(ast)