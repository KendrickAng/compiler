import sys

import lex
import parse
import ir3
import backend

def main():
    # verify user input
    if len(sys.argv) != 2:
        print("Usage: python3 compile.py <filename>")
        exit(1)

    # execute main logic
    filename = sys.argv[1]
    with open(filename) as f:
        content = f.read()
        run(content, filename)

def run(text: str, filename: str):
    # lexing - extract tokens
    tokens, err = lex.Lexer(text, filename).lex()
    if err: return print(err)

    # parsing - generate AST
    cst, err, astt, _ = parse.Parser(tokens).parse()
    if err: return print(err)

    # static checking
    try:
        astt.static_check()
    except Exception as err:
        print("Error during static checking!")
        return print(err)

    #print(astt)

    # intermediate code generation
    ir: ir3.Program3 = ir3.run(astt)

    #print(ir)

    # backend - generate assembly code
    asm = backend.Arm(ir).run()

    print("\n".join(asm))

    # write assembly code to disk
    fname = filename.split(".")[0]
    with open(f"{fname}.s", "w") as f:
        f.write("\n".join(asm))

if __name__ == "__main__":
    main()