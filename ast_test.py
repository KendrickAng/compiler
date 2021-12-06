import unittest
from parse import run

class TestSemantics(unittest.TestCase):
    def test(self):
        # open file, lex input text, print out all tokens
        with open("test/semantics/sample.in") as f:
            text = f.read()

            cst, err, astt, _ = run(text, "semantics/sample.in")
            if err is not None:
                print(err)
                return

            astt.static_check()


if __name__ == "__main__":
    unittest.main()