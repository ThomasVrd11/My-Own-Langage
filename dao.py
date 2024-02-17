"""Tokens for the dao language"""

# Integer token type
from typing import Any


TT_INT = 'TT_INT'
# Float token type
TT_FLOAT = 'FLOAT'
# Plus token type
TT_PLUS = 'PLUS'
# Minus token type
TT_MINUS = 'MINUS'
# Multiply token type
TT_MUL = 'MUL'
# Divide token type
TT_DIV = 'DIV'
# Left parenthesis token type
TT_LPAREN = 'LPAREN'
# Right parenthesis token type
TT_RPAREN = 'RPAREN'



class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
"""Lexer class for the dao language"""

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    """iteration through the text to get the tokens"""
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    """return the tokens"""
    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, self.current_char))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, self.current_char))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, self.current_char))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, self.current_char))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, self.current_char))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, self.current_char))
                self.advance()
                
        return tokens