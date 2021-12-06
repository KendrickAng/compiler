import sys
from copy import deepcopy
from typing import List, Set, Dict, Tuple, Optional, Callable, Optional, Any

########################################################
######################## TOKENS ########################
########################################################

ESCAPE_CHARS = {"\"", "\\", "t", "b", "r", "f", "n"}
DIGITS = set("1234567890")
WHITESPACE = set(" \t\n")
UPPERCASE = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOWERCASE = set("abcdefghijklmnopqrstuvwxyz")
LETTERS = UPPERCASE.union(LOWERCASE)
LETTERS_DIGITS_UNDERSCORE = LETTERS.union(DIGITS).union(set("_"))

CLASS = "class"
IF = "if"
ELSE = "else"
WHILE = "while"
READLN = "readln"
PRINTLN = "println"
RETURN = "return"
TRUE = "true"
FALSE = "false"
THIS = "this"
NEW = "new"
NULL = "null"
RESERVED_KEYWORDS = {CLASS, IF,
                     ELSE, WHILE, READLN,
                     PRINTLN, RETURN, TRUE,
                     FALSE, THIS, NEW,
                     NULL}

INT = "Int"
BOOL = "Bool"
STRING = "String"
VOID = "Void"

# Literals
TT_INT = "INTEGER_LITERAL"
TT_STR = "STRING_LITERAL"

TT_KEYWORD = "KEYWORD"
TT_ID = "IDENTIFIER"

# Binary arithmetic operators
TT_PLUS = "PLUS"
TT_MINUS = "MINUS" # also unary negative
TT_MULT = "MULT"
TT_DIV = "DIV"

# Binary boolean operators
TT_AND = "AND"
TT_OR = "OR"

# Binary relation operators
TT_LESS_EQ = "LE"
TT_LESS_THAN = "LT"
TT_GREATER_EQ = "GE"
TT_GREATER_THAN = "GT"
TT_EQUAL = "EQ"
TT_NOT_EQ = "NE"

# Unary operators
TT_EXCLAMATION = "EXCLAMATION"

# Class names
TT_TYPE = "TYPE"
TT_CNAME = "CNAME"
TT_ASSIGNMENT = "ASSIGNMENT"
TT_L_CURLY_BRACE = "L_CURLY_BRACE"
TT_R_CURLY_BRACE = "R_CURLY_BRACE"
TT_L_PAREN = "L_PAREN"
TT_R_PAREN = "R_PAREN"
TT_SEMICOLON = "SEMICOLON"
TT_COMMA = "COMMA"
TT_DOT = "DOT"
TT_COMMENT = "COMMENT"
TT_EPSILON = "EPSILON"
TT_EOF = "EOF"
TT_EMPTY = "##EMPTY_TOKEN##"

class Token:
    @classmethod
    def empty(cls):
        return Token(TT_EMPTY)

    def __init__(self, token_type: str, value: Any=None, lexed_pos: 'LexerPosition'=None):
        self.type = token_type
        self.value = value
        self.lexed_pos = lexed_pos

    def __repr__(self):
        if self.value:
            return f"Token({self.type},{self.value})"
        return f"Token({self.type})"

    def __eq__(self, other):
        return self.type == other.make_type \
               and self.value == other.value

########################################################
######################## ERRORS ########################
########################################################

class Error:
    def __init__(self, name: str, desc: str, error_pos: 'LexerPosition'):
        self.name = name
        self.desc = desc
        self.error_pos = error_pos

    def __str__(self) -> str:
        filename, row, col = self.error_pos.filename, self.error_pos.row, self.error_pos.col
        return f"\n{self.name}: {self.desc}\n"\
               f"File {filename}, row {row}, col {col}\n"

class InvalidSyntaxError(Error):
    def __init__(self, desc: str, error_pos: 'LexerPosition'):
        super().__init__("InvalidSyntaxError", desc, error_pos)

class IllegalTokenError(Error):
    def __init__(self, desc: str, error_pos: 'LexerPosition'):
        super().__init__("IllegalTokenError", desc, error_pos)

class IllegalEscapeError(Error):
    def __init__(self, desc: str, error_pos: 'LexerPosition'):
        super().__init__("IllegalEscapeError", desc, error_pos)

################################################################
######################## LEXER POSITION ########################
################################################################

class LexerPosition:
    def __init__(self, idx: int, row: int, col: int, filename: str):
        self.idx = idx
        self.row = row
        self.col = col
        self.filename = filename

    # moves the currently tracked position based on token read
    def advance(self, c: str) -> None:
        self.idx += 1
        self.col += 1
        if c == '\n':
            self.row += 1
            self.col = 0

    def copy(self) -> 'LexerPosition':
        return deepcopy(self)

#######################################################
######################## LEXER ########################
#######################################################

class Lexer:
    def __init__(self, text: str, filename: str):
        self.text = text + "\n" # edge case: file ends with comment but no newline
        self.filename = filename
        self.curr_token = text[0] if text else None
        self.pos = LexerPosition(idx=0, row=1, col=1, filename=filename)

    # move the current position and loads the next token to be processed
    def advance(self) -> None:
        self.pos.advance(self.curr_token) # mark current token as consumed
        try:
            self.curr_token = self.text[self.pos.idx]
        except IndexError:
            self.curr_token = None

    # converts the input text into a list of Tokens
    def lex(self) -> Tuple[List[Token], Optional[Error]]:
        tokens = []

        while self.curr_token is not None:
            token = self.curr_token

            if token == "+": # binop arithmetic
                tokens.append(Token(TT_PLUS, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == "-": # binop arithmetic
                tokens.append(Token(TT_MINUS, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == "*": # binop arithmetic
                tokens.append(Token(TT_MULT, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == "{":
                tokens.append(Token(TT_L_CURLY_BRACE, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == "}":
                tokens.append(Token(TT_R_CURLY_BRACE, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == "(":
                tokens.append(Token(TT_L_PAREN, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == ")":
                tokens.append(Token(TT_R_PAREN, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == ";":
                tokens.append(Token(TT_SEMICOLON, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == ",":
                tokens.append(Token(TT_COMMA, lexed_pos=self.pos.copy()))
                self.advance()
            elif token == ".":
                tokens.append(Token(TT_DOT, lexed_pos=self.pos.copy()))
                self.advance()
            elif token in WHITESPACE: # whitespace
                self.advance()
            elif token in DIGITS: # integer literal
                token, err = self.lex_digits()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token in UPPERCASE: # class name
                token, err = self.lex_cname()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token in LOWERCASE: # identifier OR boolean literal
                token, err = self.lex_identifier_or_keyword()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token == "/": # comment
                token, err = self.lex_comment_or_div()
                if err is not None:
                    return tokens, err
                if token.type != TT_EMPTY:
                    tokens.append(token)
            elif token == "\"": # string literal
                token, err = self.lex_string_literal()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token == "&": # binary boolean AND
                token, err = self.lex_boolean_and()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token == "|": # binary boolean OR
                token, err = self.lex_boolean_or()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            elif token in "<>=!": # binary relational op
                token, err = self.lex_relational_op_or_unegation_or_assign()
                if err is not None:
                    return tokens, err
                tokens.append(token)
            else:
                return [], IllegalTokenError(f"'{token}'", self.pos.copy())

        tokens.append(Token(TT_EOF))
        return tokens, None

    def lex_digits(self) -> Tuple[Token, Optional[Error]]:
        digits_str = ""
        start_pos = self.pos.copy()

        while self.curr_token in DIGITS:
            digits_str += self.curr_token
            self.advance()

        return Token(TT_INT, int(digits_str), lexed_pos=start_pos), None

    def lex_cname(self) -> Tuple[Token, Optional[Error]]:
        # start off with uppercase letter
        cname_str = self.curr_token
        start_pos = self.pos.copy()

        # consume uppercase letter and read
        self.advance()
        while self.curr_token in LETTERS_DIGITS_UNDERSCORE:
            cname_str += self.curr_token
            self.advance()

        return Token(TT_TYPE, cname_str, lexed_pos=start_pos), None

    def lex_comment_or_div(self) -> Tuple[Token, Optional[Error]]:
        start_pos = self.pos.copy()
        self.advance()

        # edge case - '/' then EOF
        if self.curr_token == "*": # multiline comment
            # consume multiline comment, read until find end of block comemnt
            self.advance()
            stk = []

            while self.curr_token is not None:
                stk.append(self.curr_token)
                self.advance()
                if len(stk) >= 2 and stk[-2] == '*' and stk[-1] == '/': # found end of comment
                    return Token.empty(), None

            return Token.empty(), InvalidSyntaxError( # couldn't find end of comment
                f"expected end of comment */",
                error_pos=self.pos
            )

        elif self.curr_token == "/":
            # consume single-line comment
            self.advance()
            while self.curr_token is not None and self.curr_token != "\n":
                self.advance()
            return Token.empty(), None

        else:
            # assume we mean division
            return Token(TT_DIV, lexed_pos=self.pos.copy()), None

    def lex_string_literal(self) -> Tuple[Token, Optional[Error]]:
        string_lit = ""
        start_pos = self.pos.copy()

        isEscape = False
        esc_char_to_seq = {
            "t": "\t",
            "b": "\b",
            "r": "\r",
            "f": "\f",
            "n": "\n",
            "\\": "\\",
            "\"": "\""
        }

        self.advance() # consume leading "
        while self.curr_token != "\"":
            # no multiline comments allowed
            if self.curr_token == "\n":
                return Token.empty(), InvalidSyntaxError(
                    "illegal line end in string literal",
                    error_pos=self.pos.copy()
                )
            elif self.curr_token == "\\": # backslash, starting an escape
                self.advance()
                if self.curr_token not in ESCAPE_CHARS.union({'x', '0'}): # escaping unknown char
                    return Token.empty(), IllegalEscapeError(
                        f"illegal escape character '{self.curr_token}'",
                        self.pos
                    )
                elif self.curr_token in {'x', '0'}: # decimal or hex escape
                    isDecimal = self.curr_token == '0'
                    digit = ""

                    self.advance()
                    while self.curr_token in DIGITS:
                        digit += self.curr_token
                        self.advance()
                    ordinal = int(digit, base=10) if isDecimal else int(digit, base=16) # paste the converted char into the string

                    if ordinal >= 128:
                        return Token.empty(), IllegalEscapeError(
                            f"decimal/hex ascii character translates to >= 128",
                            self.pos
                        )

                    string_lit += chr(ordinal)
                else: # if known escape sequence, add it immediately
                    string_lit += esc_char_to_seq[self.curr_token]
                    self.advance()
            else:
                string_lit += self.curr_token
                self.advance()

        self.advance() # consume remaining "
        return Token(TT_STR, string_lit, lexed_pos=start_pos), None

    def lex_identifier_or_keyword(self) -> Tuple[Token, Optional[Error]]:
        id_str = f"{self.curr_token}"
        start_pos = self.pos.copy()

        self.advance()
        while self.curr_token in LETTERS_DIGITS_UNDERSCORE:
            id_str += self.curr_token
            self.advance()

        # check if reserved keyword (boolean literal)
        if id_str in RESERVED_KEYWORDS:
            return Token(TT_KEYWORD, id_str, lexed_pos=start_pos), None

        return Token(TT_ID, id_str, lexed_pos=start_pos), None

    def lex_boolean_and(self) -> Tuple[Token, Optional[Error]]:
        start_pos = self.pos.copy()

        self.advance()
        if self.curr_token != "&":
            return Token.empty(), InvalidSyntaxError(
                f"expected '&', got '{self.curr_token}'",
                error_pos=self.pos
            )
        self.advance() # consume the second '&'

        return Token(TT_AND, lexed_pos=start_pos), None

    def lex_boolean_or(self) -> Tuple[Token, Optional[Error]]:
        start_pos = self.pos.copy()

        self.advance()
        if self.curr_token != "|":
            return Token.empty(), InvalidSyntaxError(
                f"expected '|', got {self.curr_token}",
                error_pos=self.pos
            )
        self.advance() # consume the second '|'

        return Token(TT_OR, lexed_pos=start_pos), None

    def lex_relational_op_or_unegation_or_assign(self) -> Tuple[Token, Optional[Error]]:
        start_pos = self.pos.copy()
        start_token = self.curr_token

        self.advance()
        if self.curr_token == "=": # LE, GE, NE, EQ
            self.advance() # consume the '='
            if start_token == ">":
                return Token(TT_GREATER_EQ, lexed_pos=start_pos), None
            elif start_token == "<":
                return Token(TT_LESS_EQ, lexed_pos=start_pos), None
            elif start_token == "!":
                return Token(TT_NOT_EQ, lexed_pos=start_pos), None
            elif start_token == "=":
                return Token(TT_EQUAL, lexed_pos=start_pos), None
            else:
                raise AssertionError("should not be here 2")

        if start_token == ">":
            return Token(TT_GREATER_THAN, lexed_pos=start_pos), None
        elif start_token == "<":
            return Token(TT_LESS_THAN, lexed_pos=start_pos), None
        elif start_token == "!":
            return Token(TT_EXCLAMATION, lexed_pos=start_pos), None
        elif start_token == "=":
            return Token(TT_ASSIGNMENT, lexed_pos=start_pos), None
        else:
            raise AssertionError("should not be here 1")

def run(text: str, filename: str) -> Tuple[List[Token], Optional[Error]]:
    lexer = Lexer(text, filename)
    return lexer.lex()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 lex.py <filename>")
        exit(1)

    filename = sys.argv[1]

    # open file, lex input text, print out all tokens
    with open(filename) as f:
        text = f.read()

        tokens, err = run(text, filename)
        if err is not None:
            return print(err)

        for token in tokens:
            print(token)

if __name__ == "__main__":
    main()