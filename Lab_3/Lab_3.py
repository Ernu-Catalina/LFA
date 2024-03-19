class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, input):
        self.input = input
        self.index = 0

    def is_digit(self, char):
        return char.isdigit()

    def is_operator(self, char):
        return char in ['+', '-', '*', '=', '/', '^']

    def next_token(self):
        while self.index < len(self.input):
            current_char = self.input[self.index]

            if current_char.isspace():
                self.index += 1
                continue

            if self.is_digit(current_char):
                num = ""
                while self.index < len(self.input) and self.is_digit(self.input[self.index]):
                    num += self.input[self.index]
                    self.index += 1
                return Token("INTEGER", int(num))

            if self.is_operator(current_char):
                self.index += 1
                return Token("OPERATOR", current_char)

            if current_char == '(':
                self.index += 1
                return Token("L_PAREN", current_char)

            if current_char == ')':
                self.index += 1
                return Token("R_PAREN", current_char)

            raise ValueError(f"Unknown token: {current_char}")

        return Token("EOF", "")

    def tokenize(self):
        tokens = []
        next_token = self.next_token()
        while next_token.type != "EOF":
            tokens.append(next_token)
            next_token = self.next_token()
        return tokens


input_expr = input("Enter an arithmetic expression: ")
lexer = Lexer(input_expr)
tokens = lexer.tokenize()

for token in tokens:
    print(token.type, token.value)
