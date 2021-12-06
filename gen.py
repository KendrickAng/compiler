import sys

import lex
import parse
import ir3

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gen.py <filename>")
        exit(1)

    filename = sys.argv[1]

    # open file, lex input text, print out all tokens
    with open(filename) as f:
        run(f.read(), filename)

def run(text: str, filename: str):
    # generate tokens
    lexer = lex.Lexer(text, filename)
    tokens, err = lexer.lex()
    if err: return print(err)

    # generate AST
    parser = parse.Parser(tokens)
    cst, err, astt, _ = parser.parse()
    if err: return print(err)

    # if parse succeeds, proceed to static checking
    try:
        astt.static_check()
    except Exception as err:
        print("Error during static checking!")
        return print(err)

    #print(astt)

    # if typecheck succeeds, proceed to intermediate code generation
    ir: ir3.Program3 = ir3.run(astt)
    print(ir)

    return cst, err, astt, _

if __name__ == "__main__":
    main()