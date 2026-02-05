import sys
from lex import *

class Parser:
    """Parser object keeps track of current token and checks if the code matches the grammer"""
    def __init__(self, lexer):
        self.lexer = lexer
        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()  # twice to initialise current and peek

    def check_token(self, kind):
        """return true if the current token matches"""
        return kind == self.cur_token.kind

    def check_peek(self, kind):
        """return true if the next token matches."""
        return kind == self.peek_token.kind

    def match(self, kind):
        """try to match the current token. if not, error. advances the current token."""
        if not self.check_token(kind):
            self.abort(f"Expected {kind.name}, got {self.cur_token.kind.name}")
        self.next_token()

    def next_token(self):
        """advances the current token"""
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()
        # lexer handles eof

    def abort(self, message):
        sys.exit("Error. " + message)

    # production rules
    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # parse all the statements in the program
        while not self.check_token(TokenType.EOF):
            self.statement()

    # one of the following statements
    def statement(self):
        # check the first token to see what kind of statement this is

        # 'PRINT' (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()

        self.nl()

    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")

        # require at least one newline
        self.match(TokenType.NEWLINE)
        # allow extra newlines
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def expression(self):
        pass
