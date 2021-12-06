from lex import *
import unittest

class TestArithmetic(unittest.TestCase):
    def test_arithmetic_success_1(self):
        tokens, err = run(" 123 + 201 -343* 46   / 5", "test_arithmetic_success_1")
        self.assertTrue(err is None)

    def test_arithmetic_success_2(self):
        tokens, err = run("/", "test_arithmetic_success_2")
        self.assertTrue(err is None)

class TestClassName(unittest.TestCase):
    def test_cname_success_1(self):
        tokens, err = run(" Lexer Parser Bonjovi ", "test_cname_success_1")
        self.assertTrue(err is None)

class TestIntegerLiteral(unittest.TestCase):
    def test_int_success_1(self):
        tokens, err = run("094831", "test_int_success_1")
        print(tokens)
        self.assertTrue(err is None)

class TestStringLiteral(unittest.TestCase):
    def test_str_success_1(self):
        tokens, err = run(r'"hi\065\x42 " "another"', "test_str_success_1")
        print(tokens)
        print(err)
        self.assertTrue(err is None)

class TestBoolLiteral(unittest.TestCase):
    def test_bool_success_1(self):
        tokens, err = run("true false True False", "test_bool_success_1")
        print(tokens)
        self.assertTrue(err is None)

class TestComment(unittest.TestCase):
    def test_comment_success_1(self):
        tokens, err = run("// single line comment ", "test_comment_success_1")
        print(tokens)
        self.assertTrue(err is None)

    def test_comment_success_2(self):
        tokens, err = run("/* multi \n line \n comment */", "test_comment_success_2")
        print(tokens)
        print(err)
        self.assertTrue(err is None)

    def test_comment_success_3(self):
        tokens, err = run("// /* this comment \n will fail */", "test_comment_success_3")
        print(tokens)
        self.assertEquals(tokens[0], Token(TT_ID, "will"))
        self.assertTrue(err is None)

class TestIdentifierKeyword(unittest.TestCase):
    def test_id_success_1(self):
        tokens, err = run("iaA0_ iAAA_12345 ", "test_id_success_1")
        print(tokens)
        self.assertTrue(err is None)

    def test_keyword_success_1(self):
        tokens, err = run("class main if else while readln println return true false this new null", "test_keyword_success_1")
        print(tokens)
        self.assertTrue(err is None)

class TestBooleanOp(unittest.TestCase):
    def test_boolop_success_1(self):
        tokens, err = run("&& ||", "test_boolop_success_1")
        print(err)
        self.assertTrue(err is None)

    def test_boolop_failure_1(self):
        tokens, err = run("& | ", "test_boolop_failure_1")
        print(tokens)
        self.assertTrue(err is not None)

class TestRelOpUnegation(unittest.TestCase):
    def test_relop_success_1(self):
        tokens, err = run("< > <= >= == !=", "test_relop_success_1")
        print(tokens)
        self.assertTrue(err is None)

    def test_unegation_success_1(self):
        tokens, err = run("! !! !!! !!!!", "test_unegation_success_1")
        print(tokens)
        self.assertTrue(err is None)

if __name__ == "__main__":
    unittest.main(verbosity=2)