from lex import *

def main():
    source = "LET foobar = 123"
    lexer = Lexer(source)

    while lexer.peek() != '\0':
        print(lexer.cur_char)
        lexer.next_char()

if __name__ == "__main__":
    main()