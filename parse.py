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

        while self.check_token(TokenType.NEWLINE):
            self.next_token()
        while not self.check_token(TokenType.EOF):
            self.statement()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # must be at least one comparison operator and another expression
        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.cur_token.text)

        # can have 0 or more comparison operator and expressions
        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def is_comparison_operator(self):
        return (self.check_token(TokenType.GT)
                or self.check_token(TokenType.GTEQ)
                or self.check_token(TokenType.LT)
                or self.check_token(TokenType.LTEQ)
                or self.check_token(TokenType.EQEQ)
                or self.check_token(TokenType.NOTEQ))

    def expression(self):
        print("EXPRESSION")

        self.term()
        # can have 0 or more +/- and expressions.
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # can have 0 or more *// and expressions
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.next_token()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # option unary +/-
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    def primary(self):
        print("PRIMARY (" + self.cur_token.text + ")")

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            self.next_token()
        else:
            # error
            self.abort("Unexpected token at " + self.cur_token.text)

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

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # Zero or more statements in the body
            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # zero or more statements in the loop body
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()
            self.match(TokenType.IDENT)

        # error if not valid statement
        else:
            self.abort("Invalid statement at " + self.cur_token.text + " (" + self.cur_token.kind.name + ")")

        self.nl()

    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")

        # require at least one newline
        self.match(TokenType.NEWLINE)
        # allow extra newlines
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

