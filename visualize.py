import graphviz
from parse import *

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 visualize.py <input_filename>")
        print("You must also have Graphviz installed.")
        exit(1)

    text = read_file(sys.argv[1])

    lexer = Lexer(text, sys.argv[1])
    tokens, err = lexer.lex()
    if err: return CstNode.empty(), err, None, None

    parser = Parser(tokens)
    cst, err, astt, _ = parser.parse()
    if err: return cst, err, astt, _

    if err is not None:
        return print(err)

    visualize(cst, "images/graphviz_cst")
    visualize(astt, "images/graphviz_ast")

def visualize(node: Union[AstNode, CstNode], filename: str):
    dot = graphviz.Digraph()
    nid = 0
    node_to_id = {}

    def label_nodes(node):
        nonlocal nid
        nid += 1
        node_to_id[node] = str(nid)
        for c in node.children:
            label_nodes(c)
    def visualize_helper(node):
        nonlocal node_to_id
        if node.value is not None and node.value.value is not None:
            s = f"{node.name}\n{node.value.value}"
        else:
            s = f"{node.name}"
        dot.node(node_to_id[node], s)
        for c in node.children:
            dot.edge(node_to_id[node], node_to_id[c])
            visualize_helper(c)

    label_nodes(node)
    visualize_helper(node)
    dot.render(filename, format="png")


def read_file(filename: str) -> str:
    with open(filename) as f:
        text = f.read()
    return text

if __name__ == "__main__":
    main()