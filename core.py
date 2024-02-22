#######################################
""" Implements the core of the language.
    It includes the following:
    - Constants for the language
    - Errors management for the language
    - Position class for the language
    - Tokens for the language
    - Lexer class for the language
    - Nodes for the language
    """
#######################################

from highlight_error_location import *
import string

#######################################
""" CONSTANTS FOR THE LANGUAGE
    (DIGITS, LETTERS, LETTERS_DIGITS)
    TO KEEP TRACK OF THE CHARACTERS IN THE FILE
    (DIGITS: 0-9, LETTERS: a-z, A-Z, LETTERS_DIGITS: a-z, A-Z, 0-9)
    """
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
""" ERRORS MANAGEMENT FOR THE LANGUAGE
    (ILLEGAL CHARACTER, EXPECTED CHARACTER, INVALID SYNTAX, RUNTIME ERROR)
    IT ALSO IMPLEMENTS THE ERROR CLASS
    TO KEEP TRACK OF THE ERRORS IN THE FILE
    (POSITION START, POSITION END, ERROR NAME, DETAILS)
    """
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + \
            highlight_error_location(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + \
            highlight_error_location(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

#######################################
""" POSITION CLASS FOR THE LANGUAGE, 
    TO KEEP TRACK OF THE POSITION OF THE 
    CHARACTERS IN THE FILE 
    (LINE NUMBER, COLUMN NUMBER, FILE NAME, FILE TEXT) 
    """
#######################################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
""" TOKENS FOR THE LANGUAGE 
    (INTEGER, FLOAT, IDENTIFIER, KEYWORD, OPERATORS, PARENTHESIS, EOF)
    AND KEYWORDS 
    (VAR, AND, OR, NOT, IF, ELIF, ELSE, THEN, FOR, WHILE) 
    IT ALSO IMPLEMENTS THE TOKEN CLASS
    TO KEEP TRACK OF THE TOKENS IN THE FILE
    (TYPE, VALUE, POSITION START, POSITION END)
    """
#######################################


TT_INT = 'INT'                # Integer
TT_FLOAT = 'FLOAT'            # Floating point
TT_IDENTIFIER = 'IDENTIFIER'  # Variable name
TT_KEYWORD = 'KEYWORD'        # Language keyword
TT_PLUS = 'PLUS'              # Addition
TT_MINUS = 'MINUS'            # Subtraction
TT_MUL = 'MUL'                # Multiplication
TT_DIV = 'DIV'                # Division
TT_POW = 'POW'                # Power
TT_EQ = 'EQ'                  # Equals
TT_LPAREN = 'LPAREN'          # Left parenthesis
TT_RPAREN = 'RPAREN'          # Right parenthesis
TT_EE = 'EE'                  # Equality
TT_NE = 'NE'                  # Inequality
TT_LT = 'LT'                  # Less than
TT_GT = 'GT'                  # Greater than
TT_LTE = 'LTE'                # Less/equal
TT_GTE = 'GTE'                # Greater/equal
TT_EOF = 'EOF'                # End of File


KEYWORDS = [
    'VAR',
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELIF',
    'ELSE', 
    'THEN', 
    'FOR', 
    'WHILE',
    'TO',
    'STEP' 
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
""" LEXER CLASS FOR THE LANGUAGE 
    TO IMPLEMENT THE LEXICAL ANALYSIS 
    OF THE FILE
    (GETTING THE TOKENS FROM THE FILE)
    """
#######################################


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

