from lex import *
from parse import *

def main():
    print("teeny tiny compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compilor needs source file as argument")
    with open(sys.argv[1], 'r') as input_file:
        source = input_file.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()  # start the parser
    print("Parsing completed.")

if __name__ == "__main__":
    main()