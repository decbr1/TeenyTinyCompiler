# https://austinhenley.com/blog/teenytinycompiler1.html
# https://github.com/AZHenley/teenytinycompiler
# MIT License (c) 2020 Austin Henley
# MIT License (c) 2026 Declan Brooks

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
        pass

    def skip_whitespace(self):
        """Skip whitespace except newlines, which we will use to indicate the end of a statement."""
        pass

    def skip_comment(self):
        """Skip comments in the code."""
        pass

    def get_token(self):
        """Return the next token."""
        pass
