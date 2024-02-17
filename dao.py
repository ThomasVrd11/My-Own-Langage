"""Tokens for the dao language"""

# Integer token
TT_INT = 'TT_INT'
# Float token
TT_FLOAT = 'FLOAT'
# Plus token
TT_PLUS = 'PLUS'
# Minus token
TT_MINUS = 'MINUS'
# Multiply token
TT_MUL = 'MUL'
# Divide token
TT_DIV = 'DIV'
# Left parenthesis token
TT_LPAREN = 'LPAREN'
# Right parenthesis token
TT_RPAREN = 'RPAREN'



class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'