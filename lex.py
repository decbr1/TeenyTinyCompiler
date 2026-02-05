# https://austinhenley.com/blog/teenytinycompiler1.html
# https://github.com/AZHenley/teenytinycompiler
# MIT License (c) 2020 Austin Henley
# MIT License (c) 2026 Declan Brooks
import enum
import sys

class Lexer:
    def __init__(self, source):
        self.source = source + '\n'  # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.cur_char = ''  # Current character in the string
        self.cur_pos = -1  # Current position in the string
        self.next_char()
    
    def next_char(self):
        """Process the next character."""
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'  # end of file
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        """Return the lookahead character."""
        if self.cur_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos + 1]
    
    def abort(self, message):
        """Invalid token found, print error message and exit."""
        sys.exit("Lexing error. " + message)

    def skip_whitespace(self):
        """Skip whitespace except newlines, which we will use to indicate the end of a statement."""
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()


    def skip_comment(self):
        """Skip comments in the code."""
        pass

    def get_token(self):
        """Return the next token."""
        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest
        self.skip_whitespace()
        token = None

        match self.cur_char:
            case '+':
                token = Token(self.cur_char, TokenType.PLUS)
            case '-':
                token = Token(self.cur_char, TokenType.MINUS)
            case '*':
                token = Token(self.cur_char, TokenType.ASTERISK)
            case '/':
                token = Token(self.cur_char, TokenType.SLASH)
            case '\n':
                token = Token(self.cur_char, TokenType.NEWLINE)
            case '\0':
                token = Token(self.cur_char, TokenType.EOF)
            case _:
                self.abort("Unknown token: " + self.cur_char)

        self.next_char()
        return token


class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text  # literal
        self.kind = token_kind  # type classification


class TokenType(enum.Enum):
    """Enum for all the types of tokens"""
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211