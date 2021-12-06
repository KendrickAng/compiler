from lex import *
from ast import *
from typing import List, Set, Dict, Tuple, Optional, Callable, Optional, Any, Union
from operator import itemgetter

########################################################
######################## ERRORS ########################
########################################################

class Error(lex.Error):
    def __init__(self, name: str, desc: str, error_pos: lex.LexerPosition):
        super().__init__(name, desc, error_pos)

class IllegalSyntaxError(Error):
    def __init__(self, desc: str, error_pos: lex.LexerPosition):
        super().__init__("IllegalSyntaxError", desc, error_pos)

########################################################
######################## PARSER ########################
########################################################

# cst node, error (if any), dict of info for astt building
ParseResult = Tuple[CstNode, Optional[Error], Optional[AstNode], Any]

class Parser:
    def __init__(self, tokens: List[lex.Token]):
        self.tokens = tokens
        self.cursor = 0
        self.curr_token: lex.Token = tokens[0] if len(tokens) > 0 else None

    def advance(self):
        self.cursor += 1
        self.curr_token = self.tokens[self.cursor] if self.cursor < len(self.tokens) else None
        return self.curr_token

    def save_cursor(self) -> int:
        return deepcopy(self.cursor)

    def backtrack(self, cursor: int):
        self.cursor = cursor
        self.curr_token = self.tokens[self.cursor]

    def parse(self) -> Tuple[CstNode, Optional[Error], Optional[Program], Any]:
        cst, err, astt, _ = self.eat_program()
        if not err and self.curr_token.type != lex.TT_EOF:
            return cst, IllegalSyntaxError("Invalid Syntax", self.curr_token.lexed_pos), astt, _
        return cst, err, astt, _

    """
    ######################## PRODUCTIONS (NON-TERMINALS) ########################
    """

    def eat_program(self) -> Tuple[CstNode, Optional[Error], Optional[Program], Any]:
        """NO BACKTRACKING
        Program -> MainClass Program1
        """
        n1, err, a1, _ = self.eat_mainclass() # mainclass node
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_program1() # classdecls node
        if err is not None: return n2, err, a1, _

        cst = CstNode(name=CST_PROGRAM, children=[n1,n2])
        astt = AstNode.make_program(a1, a2)

        return cst, None, astt, None

    def eat_program1(self) -> Tuple[CstNode, Optional[Error], Optional[ClassDecls], Any]:
        """BACKTRACKING
        Program1 -> ClassDecl Program1
                | ''
        """
        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_program11()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_program12()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        # backtracking didn't work, return error
        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_program11(self) -> Tuple[CstNode, Optional[Error], Optional[ClassDecls], Any]:
        """no backtracking
        Program1 -> ClassDecl Program1
        """
        node1, err, a1, _ = self.eat_classdecl() # single classdecl node
        if err is not None: return node1, err, a1, _

        node2, err, a2, _ = self.eat_program1() # classdecls node
        if err is not None: return node2, err, a2, _

        cst = CstNode(name=CST_PROGRAM1, children=[node1, node2])
        astt = AstNode.make_classdecls([a1] + a2.children)

        return cst, None, astt, None

    def eat_program12(self) -> ParseResult:
        """no backtracking
        Program1 -> ''
        """
        cst = CstNode(name=CST_PROGRAM1, children=[CstNode.epsilon()])
        astt = AstNode.make_classdecls([])
        return cst, None, astt, None

    def eat_mainclass(self) -> Tuple[CstNode, Optional[Error], Optional[MainClass], Any]:
        """no backtracking
        MainClass -> class cname { Void main ( FmlList ) MdBody }
        """
        # check for "class"
        node1, err, _, _ = self.eat_class()
        if err is not None: return node1, err, _, _

        # check for <cname>
        node2, err, a2, _ = self.eat_cname()
        if err is not None: return node2, err, a2, _

        # check for '{'
        node3, err, _, _ = self.eat_l_curly_brace()
        if err is not None: return node3, err, _, _

        # check for 'void'
        node4, err, a4, _ = self.eat_void_type()
        if err is not None: return node4, err, a4, _

        # check for 'main'
        node5, err, a5, _ = self.eat_id()
        if err is not None: return node5, err, a5, _

        # check for '('
        node6, err, _, _ = self.eat_l_paren()
        if err is not None: return node6, err, _, _

        # check for FmlList
        node7, err, a7, _ = self.eat_fmllist()
        if err is not None: return node7, err, a7, _

        # check for ')'
        node8, err, _, _ = self.eat_r_paren()
        if err is not None: return node8, err, _, _

        # check for MdBody
        node9, err, a9, _ = self.eat_mdbody()
        if err is not None: return node9, err, a9, _

        # check for '}'
        node10, err, _, _ = self.eat_r_curly_brace()
        if err is not None: return node10, err, _, _

        cst = CstNode(name=CST_MAINCLASS, children=[node1,node2,node3,node4,node5,node6,node7,node8,node9,node10])
        mainmd = AstNode.make_mddecl(type=a4, id=a5, fmllist=a7, mdbody=a9)
        astt = AstNode.make_mainclass(cname=a2, mainmd=mainmd)

        return cst, None, astt, None

    def eat_classdecl(self) -> ParseResult:
        """ClassDecl -> class cname { ClassDecl1 ClassDecl2 }"""
        # check 'class'
        n1, err, _, _ = self.eat_class()
        if err is not None: return n1, err, _, _

        # check 'cname'
        n2, err, a2, _ = self.eat_cname() # cname node
        if err is not None: return n2, err, a2, _

        # check '{'
        n3, err, _, _ = self.eat_l_curly_brace()
        if err is not None: return n2, err, _, _

        # check ClassDecl1
        n4, err, a4, _ = self.eat_classdecl1() # vardecls node
        if err is not None: return n4, err, a4, _

        # check ClassDecl2
        n5, err, a5, _ = self.eat_classdecl2() # mddecls node
        if err is not None: return n5, err, a5, _

        # check '}'
        n6, err, _, _ = self.eat_r_curly_brace()
        if err is not None: return n6, err, _, _

        cst = CstNode(name=CST_CLASSDECL, children=[n1,n2,n3,n4,n5,n6])
        astt = AstNode.make_classdecl(a2, a4, a5)

        return cst, None, astt, None

    def eat_classdecl1(self) -> ParseResult:
        """ClassDecl1 -> VarDecl ClassDecl1 | '' """
        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_classdecl11()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_classdecl12()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_classdecl11(self) -> Tuple[CstNode, Optional[Error], Optional[VarDecls], Any]:
        """ClassDecl1 -> VarDecl ClassDecl1"""
        # check VarDecl
        n1, err, a1, _ = self.eat_vardecl() # single vardecl node
        if err is not None: return n1, err, None, _

        # check ClassDecl1
        n2, err, a2, _ = self.eat_classdecl1() # vardecls node
        if err is not None: return n2, err, None, _

        cst = CstNode(name=CST_CLASSDECL1, children=[n1,n2])
        astt = AstNode.make_vardecls([a1] + a2.children)

        return cst, None, astt, None

    def eat_classdecl12(self) -> Tuple[CstNode, Optional[Error], Optional[VarDecls], Any]:
        """ClassDecl1 -> '' """
        cst = CstNode(name=CST_CLASSDECL1, children=[CstNode.epsilon()])
        astt = AstNode.make_vardecls([])
        return cst, None, astt, None

    def eat_classdecl2(self) -> ParseResult:
        """ClassDecl2 -> MdDecl ClassDecl2 | '' """
        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_classdecl21()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_classdecl22()
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_classdecl21(self) -> Tuple[CstNode, Optional[Error], Optional[MdDecls], Any]:
        """ClassDecl2 -> MdDecl ClassDecl2"""
        # MdDecl
        n1, err, a1, _ = self.eat_mddecl() # single mddecl
        if err is not None: return n1, err, None, _

        # ClassDecl2
        n2, err, a2, _ = self.eat_classdecl2() # mddels node
        if err is not None: return n2, err, None, _

        cst = CstNode(name=CST_CLASSDECL2, children=[n1,n2])
        astt = AstNode.make_mddecls([a1] + a2.children)

        return cst, None, astt, None

    def eat_classdecl22(self) -> ParseResult:
        """ClassDecl2 -> '' """
        cst = CstNode(name=CST_CLASSDECL2, children=[CstNode.epsilon()])
        astt = AstNode.make_mddecls([])
        return cst, None, astt, None

    def eat_vardecl(self) -> ParseResult:
        """VarDecl -> Type id ; """
        # Type
        n1, err, a1, _ = self.eat_type()
        if err is not None: return n1, err, a1, _

        # id
        n2, err, a2, _ = self.eat_id()
        if err is not None: return n2, err, a2, _

        # ;
        n3, err, a3, _ = self.eat_semicolon()
        if err is not None: return n3, err, a3, _

        cst = CstNode(name=CST_VARDECL, children=[n1,n2,n3])
        astt = AstNode.make_vardecl(a1, a2)

        return cst, None, astt, None

    def eat_mddecl(self) -> Tuple[CstNode, Optional[Error], Optional[MdDecl], Any]:
        """MdDecl -> Type id ( FmlList ) MdBody"""
        # Type
        n1, err, a1, info = self.eat_type()
        if err is not None: return n1, err, a1, info

        # id
        n2, err, a2, info = self.eat_id()
        if err is not None: return n2, err, a2, info

        # (
        n3, err, a3, info = self.eat_l_paren()
        if err is not None: return n3, err, a3, info

        # Fmllist
        n4, err, a4, info = self.eat_fmllist()
        if err is not None: return n4, err, a4, info

        # )
        n5, err, a5, info = self.eat_r_paren()
        if err is not None: return n5, err, a5, info

        # MdBody
        n6, err, a6, info = self.eat_mdbody()
        if err is not None: return n6, err, a6, info

        cst = CstNode(name=CST_MDDECL, children=[n1,n2,n3,n4,n5,n6])
        astt = AstNode.make_mddecl(a1, a2, a4, a6)

        return cst, None, astt, {}

    def eat_fmllist(self) -> Tuple[CstNode, Optional[Error], Optional[FmlList], Any]:
        """FmlList -> Type id FmlList1 | '' """
        cursor = self.save_cursor()
        node, err, astt, info = self.eat_fmllist01() # list of fml
        if err is None: return node, err, astt, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, info = self.eat_fmllist02() # empty list of fml
        if err is None: return node, err, astt, info
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, {}

    def eat_fmllist01(self) -> ParseResult:
        """FmlList -> Type id FmlList1"""
        n1, err, a1, info = self.eat_type() # type node
        if err is not None: return n1, err, a1, info

        n2, err, a2, info = self.eat_id() # id node
        if err is not None: return n2, err, a2, info

        n3, err, a3, info = self.eat_fmllist1() #  list of fml
        if err is not None: return n3, err, a3, info

        cst = CstNode(name=CST_FMLLIST, children=[n1,n2,n3])
        astt = AstNode.make_fmllist([AstNode.make_fml(a1, a2)] + a3.children)

        return cst, None, astt, {}

    def eat_fmllist02(self) -> ParseResult:
        """FmlList -> '' """
        cst = CstNode(name=CST_FMLLIST, children=[CstNode.epsilon()])
        astt = AstNode.make_fmllist([])
        return cst, None, astt, {}

    def eat_fmllist1(self) -> ParseResult:
        """FmlList1 -> FmlRest FmlList1 | '' """
        cursor = self.save_cursor()
        node, err, astt, info = self.eat_fmllist11() # list of fml
        if err is None: return node, err, astt, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, info = self.eat_fmllist12() # empty list
        if err is None: return node, err, astt, info
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, {}

    def eat_fmllist11(self) -> ParseResult:
        """FmlList1 -> FmlRest FmlList1"""
        n1, err, a1, info = self.eat_fmlrest() # fml node
        if err is not None: return n1, err, a1, info

        n2, err, a2, info = self.eat_fmllist1() # list of fml
        if err is not None: return n2, err, a1, info

        cst = CstNode(name=CST_FMLLIST1, children=[n1,n2])
        astt = AstNode.make_fmllist([a1] + a2.children)

        return cst, None, astt, {}

    def eat_fmllist12(self) -> ParseResult:
        """FmlList1 -> '' """
        cst = CstNode(name=CST_FMLLIST1, children=[CstNode.epsilon()])
        astt = AstNode.make_fmllist([])
        return cst, None, astt, {}

    def eat_fmlrest(self) -> Tuple[CstNode, Optional[Error], Optional[Fml], Any]:
        """FmlRest -> , Type id"""
        n1, err, a1, info = self.eat_comma()
        if err is not None: return n1, err, a1, info

        n2, err, a2, info = self.eat_type()
        if err is not None: return n2, err, a2, info

        n3, err, a3, info = self.eat_id()
        if err is not None: return n3, err, a3, info

        cst = CstNode(name=CST_FMLREST, children=[n1,n2,n3])
        astt = AstNode.make_fml(a2, a3)

        return cst, None, astt, {}

    def eat_type(self) -> Tuple[CstNode, Optional[Error], Optional['AstType'], Any]:
        """Type -> Int | Bool | String | Void | cname"""
        cursor = self.save_cursor()
        node, err, a1, info = self.eat_int_type()
        if err is None: return node, err, a1, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, a1, info= self.eat_bool_type()
        if err is None: return node, err, a1, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, a1, info = self.eat_str_type()
        if err is None: return node, err, a1, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, a1, info = self.eat_void_type()
        if err is None: return node, err, a1, info
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, a1, info = self.eat_cname()
        if err is None: return node, err, a1, info
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, {}

    def eat_mdbody(self) -> Tuple[CstNode, Optional[Error], Optional[MdBody], Any]:
        """MdBody -> { MdBody1 Stmt MdBody2 }"""
        n1, err, a1, _ = self.eat_l_curly_brace()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_mdbody1() # vardecls node
        if err is not None: return n2, err, a2, _

        n3, err, a3, _ = self.eat_stmt() # stmts node
        if err is not None: return n3, err, a3, _

        n4, err, a4, _ = self.eat_mdbody2() # stmts node
        if err is not None: return n4, err, a4, _

        n5, err, a5, _ = self.eat_r_curly_brace()
        if err is not None: return n5, err, a5, _

        cst = CstNode(name=CST_MDBODY, children=[n1,n2,n3,n4,n5])
        tmp = AstNode.make_stmts(a3.children + a4.children)
        astt = AstNode.make_mdbody(a2, tmp)

        return cst, None, astt, None

    def eat_mdbody1(self) -> Tuple[CstNode, Optional[Error], Optional[VarDecls], Any]:
        """MdBody1 -> VarDecl MdBody1 | '' """
        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_mdbody11() # vardecls node
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_mdbody12() # vardecls node
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_mdbody11(self) -> Tuple[CstNode, Optional[Error], Optional[VarDecls], Any]:
        """MdBody1 -> VarDecl MdBody1"""
        n1, err, a1, _ = self.eat_vardecl() # node w/ single child [vardecl]
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_mdbody1() # node w/ children [vardecl]
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_MDBODY1, children=[n1,n2])
        astt = AstNode.make_vardecls([a1] + a2.children)

        return cst, None, astt, None

    def eat_mdbody12(self) -> Tuple[CstNode, Optional[Error], Optional[VarDecls], Any]:
        """MdBody1 -> '' """
        cst = CstNode(name=CST_MDBODY1, children=[CstNode.epsilon()])
        astt = AstNode.make_vardecls([])
        return cst, None, astt, None

    def eat_mdbody2(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """MdBody2 -> Stmt MdBody2 | '' """
        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_mdbody21() # stmts node
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        cursor = self.save_cursor()
        node, err, astt, _ = self.eat_mdbody22() # stmts node
        if err is None: return node, err, astt, _
        self.backtrack(cursor)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_mdbody21(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """MdBody2 -> Stmt MdBody2"""
        n1, err, a1, _ = self.eat_stmt() # stmts node
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_mdbody2() # stmts node
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_MDBODY2, children=[n1,n2])
        astt = AstNode.make_stmts(a1.children + a2.children)

        return cst, None, astt, None

    def eat_mdbody22(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """MdBody2 -> '' """
        cst = CstNode(name=CST_MDBODY2, children=[CstNode.epsilon()])
        astt = AstNode.make_stmts([])
        return cst, None, astt, None

    def eat_stmt(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """
        Stmt -> if ( Exp ) { Stmt Stmt1 } else { Stmt Stmt1 }
            | while ( Exp ) { Stmt1 }
            | readln ( id ) ;
            | println ( Exp ) ;
            | id = Exp ;
            | Atom = Exp ; (atom is type field access_
            | Atom ; (atom is type member access)
            | Atom ( ) ;
            | return Exp ;
            | return ;
        """
        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt01() # if statement node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt02() # while statement
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt03() # readln
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt04() # println
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt05() # id = Exp;
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt06() # Atom . id = Exp;
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt07() # Atom ; (atom is type function call)
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt09() # return Exp;
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt010() # return;
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_stmt01(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> if ( Exp ) { Stmt Stmt1 } else { Stmt Stmt1 }"""
        n1, err, _, _ = self.eat_if()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_l_paren()
        if err is not None: return n2, err, _, _

        n3, err, a3, _ = self.eat_exp() # exp node
        if err is not None: return n3, err, a3, _

        n4, err, _, _ = self.eat_r_paren()
        if err is not None: return n4, err, _, _

        n5, err, _, _ = self.eat_l_curly_brace()
        if err is not None: return n5, err, _, _

        n6, err, a6, _ = self.eat_stmt() # stmts node
        if err is not None: return n6, err, a6, _

        n7, err, a7, _ = self.eat_stmt1() # stmts node
        if err is not None: return n6, err, a7, _

        n8, err, _, _ = self.eat_r_curly_brace()
        if err is not None: return n8, err, _, _

        n9, err, _, _ = self.eat_else()
        if err is not None: return n9, err, _, _

        n10, err, _, _ = self.eat_l_curly_brace()
        if err is not None: return n10, err, _, _

        n11, err, a11, _ = self.eat_stmt() # stmts ndoe
        if err is not None: return n11, err, a11, _

        n12, err, a12, _ = self.eat_stmt1() # stmts node
        if err is not None: return n12, err, a12, _

        n13, err, _, _ = self.eat_r_curly_brace()
        if err is not None: return n13, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13])
        if_stmts = AstNode.make_stmts(a6.children + a7.children)
        else_stmts = AstNode.make_stmts(a11.children + a12.children)
        astt = AstNode.make_stmts([AstNode.make_if_statement(a3, if_stmts, else_stmts)])

        return cst, None, astt, None

    def eat_stmt02(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> while ( Exp ) { Stmt1 }"""
        n1, err, _, _ = self.eat_while()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_l_paren()
        if err is not None: return n2, err, _, _

        n3, err, a3, _ = self.eat_exp()
        if err is not None: return n3, err, a3, _

        n4, err, _, _ = self.eat_r_paren()
        if err is not None: return n4, err, _, _

        n5, err, _, _ = self.eat_l_curly_brace()
        if err is not None: return n5, err, _, _

        n6, err, a6, _ = self.eat_stmt1()
        if err is not None: return n6 ,err, a6, _

        n7, err, _, _ = self.eat_r_curly_brace()
        if err is not None: return n7, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3,n4,n5,n6,n7])
        astt = AstNode.make_stmts([AstNode.make_while_statement(a3, a6)])

        return cst, None, astt, None

    def eat_stmt03(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> readln ( id ) ;"""
        n1, err, _, _ = self.eat_readln()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_l_paren()
        if err is not None: return n2, err, _, _

        n3, err, a3, _ = self.eat_id()
        if err is not None: return n3, err, a3, _

        n4, err, _, _ = self.eat_r_paren()
        if err is not None: return n4, err, _, _

        n5, err, _, _ = self.eat_semicolon()
        if err is not None: return n5, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3,n4,n5])
        astt = AstNode.make_stmts([AstNode.make_readln(a3)])

        return cst, None, astt, None

    def eat_stmt04(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> println ( Exp ) ;"""
        n1, err, _, _ = self.eat_println()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_l_paren()
        if err is not None: return n2, err, _, _

        n3, err, a3, _ = self.eat_exp()
        if err is not None: return n3, err, a3, _

        n4, err, _, _ = self.eat_r_paren()
        if err is not None: return n4, err, _, _

        n5, err, _, _ = self.eat_semicolon()
        if err is not None: return n5, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3,n4,n5])
        astt = AstNode.make_stmts([AstNode.make_println(a3)])

        return cst, None, astt, None

    def eat_stmt05(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> id = Exp ;"""
        n1, err, a1, _ = self.eat_id()
        if err is not None: return n1, err, a1, _

        n2, err, _, _ = self.eat_assign()
        if err is not None: return n2, err, _, _

        n3, err, a3, _ = self.eat_exp()
        if err is not None: return n3, err, a3, _

        n4, err, _, _ = self.eat_semicolon()
        if err is not None: return n4, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3,n4])
        astt = AstNode.make_stmts([AstNode.make_assignment_statement(a1, a3)])

        return cst, None, astt, None

    def eat_stmt06(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> Atom = Exp ; (atom is type field access)"""
        n1, err, a1, _ = self.eat_atom()
        if not a1 or a1.name != AST_FIELD_ACCESS:
            return n1, self.generic_syntax_err(), a1, _
        if err is not None: return n1, err, a1, _

        n4, err, _, _ = self.eat_assign()
        if err is not None: return n4, err, _, _

        n5, err, a5, _ = self.eat_exp()
        if err is not None: return n5, err, a5, _

        n6, err, _, _ = self.eat_semicolon()
        if err is not None: return n6, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n4,n5,n6])
        astt = AstNode.make_stmts([AstNode.make_assignment_statement(a1, a5)])

        return cst, None, astt, None

    def eat_stmt07(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> Atom ; (atom is type function call)"""
        n1, err, a1, _ = self.eat_atom()
        if not a1 or a1.name != AST_METHOD_CALL:
            return n1, self.generic_syntax_err(), a1, _
        if err is not None: return n1, err, a1, _

        n5, err, _, _ = self.eat_semicolon()
        if err is not None: return n5, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n5])
        astt = AstNode.make_stmts([a1])

        return cst, None, astt, None

    def eat_stmt09(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> return Exp ;"""
        n1, err, _, _ = self.eat_return()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_exp()
        if err is not None: return n2, err, a2, _

        n3, err, _, _ = self.eat_semicolon()
        if err is not None: return n3, err, _ , _

        cst = CstNode(name=CST_STMT, children=[n1,n2,n3])
        astt = AstNode.make_stmts([AstNode.make_return_statement(a2)])

        return cst, None, astt, None

    def eat_stmt010(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt -> return ;"""
        n1, err, _, _ = self.eat_return()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_semicolon()
        if err is not None: return n2, err, _, _

        cst = CstNode(name=CST_STMT, children=[n1,n2])
        astt = AstNode.make_stmts([AstNode.make_return_statement()])

        return cst, None, astt, None

    def eat_stmt1(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt1 -> Stmt Stmt1 | '' """
        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt11() # stmts node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_stmt12() # stmts node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_stmt11(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt1 -> Stmt Stmt1"""
        n1, err, a1, _ = self.eat_stmt() # stmts node, one child
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_stmt1() # stmts node, multiple children
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_STMT1, children=[n1,n2])
        astt = AstNode.make_stmts(a1.children + a2.children)

        return cst, None, astt, None

    def eat_stmt12(self) -> Tuple[CstNode, Optional[Error], Optional[Stmts], Any]:
        """Stmt1 -> '' """
        return CstNode(name=CST_STMT1, children=[CstNode.epsilon()]), None, AstNode.make_stmts([]), None

    def eat_exp(self) -> Tuple[CstNode, Optional[Error], Optional[Exp], Any]:
        """Exp -> BExp | AExp | SExp"""
        def backtrack_pick_longest(lst):
            ans = max(lst, key=itemgetter(0))
            self.backtrack(ans[0])
            return ans[1]

        c = self.save_cursor()
        bNode, bErr, bAst, _ = self.eat_bexp()
        bAns = (bNode, bErr, bAst, _)
        bPos = self.cursor # store how far we travelled
        self.backtrack(c)

        c = self.save_cursor()
        sNode, sErr, sAst, _ = self.eat_sexp()
        sAns = (sNode, sErr, sAst, _)
        sPos = self.cursor
        self.backtrack(c)

        c = self.save_cursor()
        aNode, aErr, aAst, _ = self.eat_aexp()
        aAns = (aNode, aErr, aAst, _)
        aPos = self.cursor
        self.backtrack(c)

        # all paths failed
        if bErr and sErr and aErr:
            return CstNode.empty(), self.generic_syntax_err(), None, None

        # else, pick the longest path
        lst = [(bPos, bAns), (sPos, sAns), (aPos, aAns)]
        return backtrack_pick_longest(lst)

    def eat_bexp(self) -> ParseResult:
        """BExp -> Conj BExp1"""
        n1, err, a1, _ = self.eat_conj() # conj node
        if err is not None: return n1, err, a1, _

        n2, err, a2, conjs = self.eat_bexp1() # empty node, conjs list
        if err is not None: return n2, err, a2, conjs

        def generate(lst):
            if len(lst) == 1:
                return lst[0]
            return AstNode.make_or_op(generate(lst[:-1]), lst[-1])

        new_conjs = [a1] + conjs
        astt = generate(new_conjs)
        cst = CstNode(name=CST_BEXP, children=[n1,n2])

        return cst, None, astt, None

    def eat_bexp1(self) -> ParseResult:
        """BExp1 -> || Conj BExp1 | '' """
        c = self.save_cursor()
        node, err, astt, rexps = self.eat_bexp11()
        if err is None: return node, err, astt, rexps
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, rexps = self.eat_bexp12()
        if err is None: return node, err, astt, rexps
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None


    def eat_bexp11(self) -> ParseResult:
        """BExp1 -> || Conj BExp1"""
        n1, err, _, _ = self.eat_or()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_conj()
        if err is not None: return n2, err, a2, _

        n3, err, _, conjs = self.eat_bexp1()
        if err is not None: return n3, err, _, conjs

        cst = CstNode(name=CST_BEXP1, children=[n1,n2,n3])
        astt = None
        rexps = [a2] + conjs

        return cst, None, astt, rexps

    def eat_bexp12(self) -> ParseResult:
        """BExp1 -> '' """
        return CstNode(name=CST_BEXP1, children=[CstNode.epsilon()]), None, None, []

    def eat_conj(self) -> ParseResult:
        """Conj -> RExp Conj1"""
        n1, err, a1, _ = self.eat_rexp() # rexp node
        if err is not None: return n1, err, a1, _

        n2, err, _, rexps = self.eat_conj1() # && node, may have no children (epsilon)
        if err is not None: return n2, err, _, rexps

        def generate(lst):
            if len(lst) == 1:
                return lst[0]
            return AstNode.make_and_op(generate(lst[:-1]), lst[-1])

        new_rexps = [a1] + rexps
        astt = generate(new_rexps)
        cst = CstNode(name=CST_CONJ, children=[n1,n2])

        return cst, None, astt, None

    def eat_conj1(self) -> ParseResult:
        """Conj1 -> && RExp Conj1 | '' """
        c = self.save_cursor()
        node, err, astt, rexps = self.eat_conj11()
        if err is None: return node, err, astt, rexps
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, rexps = self.eat_conj12()
        if err is None: return node, err, astt, rexps
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_conj11(self) -> ParseResult:
        """Conj1 -> && RExp Conj1"""
        n1, err, _, _ = self.eat_and()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_rexp()
        if err is not None: return n2, err, a2, _

        n3, err, a3, rexps = self.eat_conj1()
        if err is not None: return n3, err, a3, rexps

        rexp_nodes = [a2] + rexps
        cst = CstNode(name=CST_CONJ1, children=[n1,n2,n3])

        return cst, None, None, rexp_nodes

    def eat_conj12(self) -> ParseResult:
        """Conj1 -> '' """
        return CstNode(name=CST_CONJ1, children=[CstNode.epsilon()]), None, None, []

    def eat_rexp(self) -> ParseResult:
        """RExp -> AExp BOp AExp | BGrd"""
        c = self.save_cursor()
        node, err, astt, _ = self.eat_rexp01() # bop node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_rexp02() # bgrd node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_rexp01(self) -> ParseResult:
        """RExp -> AExp BOp AExp"""
        n1, err, a1, _ = self.eat_aexp()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_bop() # terminal > < >= <= == != node
        if err is not None: return n2, err, a2, _

        n3, err, a3, _ = self.eat_aexp()
        if err is not None: return n3, err, a3, _

        cst = CstNode(name=CST_REXP, children=[n1,n2,n3])
        astt = a2
        astt.set_left_child(a1)
        astt.set_right_child(a3)
        # astt.children.extend([a1, a3]) ######## THE ORDER HERE MATTERS!!! ########

        return cst, None, astt, None

    def eat_rexp02(self) -> ParseResult:
        """RExp -> BGrd"""
        n1, err, astt, _ = self.eat_bgrd() # bgrd node
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_REXP, children=[n1]), None, astt, None

    def eat_bop(self) -> ParseResult:
        """BOp -> < | > | <= | >= | == | !="""
        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop01()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop02()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop03()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop04()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop05()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bop06()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_bop01(self) -> Tuple[CstNode, Optional[Error], Optional[Lt], Any]:
        """BOp -> < """
        n1, err, astt, _ = self.eat_lt()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bop02(self) -> Tuple[CstNode, Optional[Error], Optional[Gt], Any]:
        """BOp -> > """
        n1, err, astt, _ = self.eat_gt()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bop03(self) -> Tuple[CstNode, Optional[Error], Optional[Le], Any]:
        """BOp -> <= """
        n1, err, astt, _ = self.eat_le()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bop04(self) -> Tuple[CstNode, Optional[Error], Optional[Ge], Any]:
        """BOp -> >= """
        n1, err, astt, _ = self.eat_ge()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bop05(self) -> Tuple[CstNode, Optional[Error], Optional[Eq], Any]:
        """BOp -> == """
        n1, err, astt, _ = self.eat_dbl_eq()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bop06(self) -> Tuple[CstNode, Optional[Error], Optional[Ne], Any]:
        """BOp -> != """
        n1, err, astt, _ = self.eat_ne()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BOP, children=[n1]), None, astt, None

    def eat_bgrd(self) -> ParseResult:
        """BGrd -> ! BGrd | true | false | Atom"""
        c = self.save_cursor()
        node, err, astt, _ = self.eat_bgrd01() # negate node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bgrd02() # actual true terminal node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bgrd03() # actual false terminal node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_bgrd04() # Atom node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_bgrd01(self) -> Tuple[CstNode, Optional[Error], Optional[Complement], Any]:
        """BGrd -> ! BGrd"""
        n1, err, a1, _ = self.eat_exclamation()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_bgrd() # actual bgrd/true/false/Atom
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_BGRD, children=[n1,n2])
        astt = AstNode.make_complement(a2)

        return cst, None, astt, None

    def eat_bgrd02(self) -> Tuple[CstNode, Optional[Error], Optional[TrueLit], Any]:
        """Bgrd -> true"""
        n1, err, astt, _ = self.eat_true()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BGRD, children=[n1]), None, astt, None

    def eat_bgrd03(self) -> Tuple[CstNode, Optional[Error], Optional[FalseLit], Any]:
        """Bgrd -> false"""
        n1, err, astt, _ = self.eat_false()
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BGRD, children=[n1]), None, astt, None

    def eat_bgrd04(self) -> ParseResult:
        """Bgrd -> Atom"""
        n1, err, astt, _ = self.eat_atom() # Atom node
        if err is not None: return n1, err, astt, _

        return CstNode(name=CST_BGRD, children=[n1]), None, astt, None

    def eat_aexp(self) -> ParseResult:
        """AExp -> Term AExp1"""
        n1, err, a1, _ = self.eat_term() # term node
        if err is not None: return n1, err, a1, _

        n2, err, a2, ops = self.eat_aexp1() # (operators, terms)
        if err is not None: return n2, err, a2, ops

        def generate(operators, terms):
            if len(operators) == 0 and len(terms) == 1:
                return terms[0]
            if operators[-1] == "+":
                return AstNode.make_plus_op(generate(operators[:-1], terms[:-1]), terms[-1])
            return AstNode.make_minus_op(generate(operators[:-1], terms[:-1]), terms[-1])

        cst = CstNode(name=CST_AEXP, children=[n1,n2])
        operators: List[str] = ops[0]
        terms = [a1] + ops[1]
        if len(operators) == 0 and len(terms) == 0:
            astt = a1 # only term
        else:
            astt = generate(operators, terms)

        return cst, None, astt, None

    def eat_aexp1(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """AExp1 -> + Term AExp1 | - Term AExp1 | '' """
        c = self.save_cursor()
        node, err, astt, ops = self.eat_aexp11()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, ops = self.eat_aexp12()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, ops = self.eat_aexp13()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_aexp11(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """AExp1 -> + Term AExp1"""
        n1, err, a1, _ = self.eat_plus()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_term()
        if err is not None: return n2, err, a2, _

        n3, err, a3, ops = self.eat_aexp1() # empty node, (operators, terms)
        if err is not None: return n3, err, a3, ops

        cst = CstNode(name=CST_AEXP1, children=[n1,n2,n3])
        operators = ["+"] + ops[0]
        terms = [a2] + ops[1]

        return cst, None, None, (operators, terms)

    def eat_aexp12(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """AExp1 -> - Term AExp1"""
        n1, err, a1, _ = self.eat_minus()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_term()
        if err is not None: return n2, err, a2, _

        n3, err, a3, ops = self.eat_aexp1()
        if err is not None: return n3, err, a3, ops

        cst = CstNode(name=CST_AEXP1, children=[n1,n2,n3])
        operators = ["-"] + ops[0]
        terms = [a2] + ops[1]

        return cst, None, None, (operators, terms)

    def eat_aexp13(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """AExp1 -> '' """
        cst = CstNode(name=CST_AEXP1, children=[CstNode.epsilon()])
        return cst, None, None, ([], [])

    def eat_term(self) -> ParseResult:
        """Term -> Ftr Term1"""
        n1, err, a1, ops = self.eat_ftr()
        if err is not None: return n1, err, a1, ops

        n2, err, a2, ops = self.eat_term1()
        if err is not None: return n2, err, a2, ops

        def generate(operators, factors):
            if len(operators) == 0 and len(factors) == 1:
                return factors[0]
            if operators[-1] == "*":
                return AstNode.make_mult_op(generate(operators[:-1], factors[:-1]), factors[-1])
            return AstNode.make_div_op(generate(operators[:-1], factors[:-1]), factors[-1])

        cst = CstNode(name=CST_TERM, children=[n1,n2])
        operators: List[str] = ops[0]
        factors: List[AstNode] = [a1] + ops[1]
        if len(operators) == 0 and len(factors) == 0:
            astt = a1 # only factor
        else:
            astt = generate(operators, factors)

        return cst, None, astt, None

    def eat_term1(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """Term1 -> * Ftr Term1 | / Ftr Term1 | '' """
        c = self.save_cursor()
        node, err, astt, ops = self.eat_term11()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, ops = self.eat_term12()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, ops = self.eat_term13()
        if err is None: return node, err, astt, ops
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_term11(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """Term1 -> * Ftr Term1 """
        n1, err, a1, _ = self.eat_mult()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_ftr()
        if err is not None: return n2, err, a2, _

        n3, err, a3, ops = self.eat_term1()
        if err is not None: return n3, err, a3, ops

        cst = CstNode(name=CST_TERM1, children=[n1,n2,n3])
        operators = ["*"] + ops[0]
        factors = [a2] + ops[1]

        return cst, None, None, (operators, factors)

    def eat_term12(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """Term1 -> / Ftr Term1 """
        n1, err, a1, _ = self.eat_div()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_ftr()
        if err is not None: return n2, err, a2, _

        n3, err, a3, ops = self.eat_term1()
        if err is not None: return n3, err, a3, ops

        cst = CstNode(name=CST_TERM1, children=[n1,n2,n3])
        operators = ["/"] + ops[0]
        factors = [a2] + ops[1]

        return cst, None, None, (operators, factors)

    def eat_term13(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        """Term1 -> '' """
        cst = CstNode(name=CST_TERM1, children=[CstNode.epsilon()])
        return cst, None, None, ([], [])

    def eat_ftr(self) -> ParseResult:
        """Ftr -> integer_literal | - Ftr | Atom"""
        c = self.save_cursor()
        node, err, astt, _ = self.eat_ftr01()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_ftr02()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_ftr03()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_ftr01(self) -> Tuple[CstNode, Optional[Error], Optional[IntegerLiteral], Any]:
        """Ftr -> integer_literal"""
        n1, err, a1, _ = self.eat_int_literal()
        if err is not None: return n1, err, a1, _

        return CstNode(name=CST_FTR, children=[n1]), None, a1, None

    def eat_ftr02(self) -> Tuple[CstNode, Optional[Error], Optional[Unegative], Any]:
        """Ftr -> - Ftr"""
        n1, err, a1, _ = self.eat_minus()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_ftr()
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_FTR, children=[n1,n2])
        astt = AstNode.make_unegative(a2)

        return cst, None, astt, None

    def eat_ftr03(self) -> ParseResult:
        """Ftr -> Atom"""
        n1, err, a1, _ = self.eat_atom()
        if err is not None: return n1, err, a1, _

        return CstNode(name=CST_FTR, children=[n1]), None, a1, None

    def eat_sexp(self) -> ParseResult:
        """SExp -> string_literal SExp1 | Atom SExp1"""
        c = self.save_cursor()
        node, err, astt, _ = self.eat_sexp01()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_sexp02()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_sexp01(self) -> ParseResult:
        """SExp -> string_literal SExp1"""
        n1, err, a1, _ = self.eat_str_literal()
        if err is not None: return n1, err, a1, _

        n2, err, a2, astt_nodes = self.eat_sexp1() # astt_nodes = list of AstNode of string_literal or Atom
        if err is not None: return n2, err, a2, astt_nodes

        def generate(s):
            if len(s) == 1:
                return s[0]
            return AstNode.make_plus_op(generate(s[:-1]), s[-1])

        new_sexps = [a1] + astt_nodes
        astt = generate(new_sexps)
        cst = CstNode(name=CST_SEXP, children=[n1,n2])

        return cst, None, astt, new_sexps

    def eat_sexp02(self) -> ParseResult:
        """SExp -> Atom SExp1"""
        n1, err, a1, _ = self.eat_atom()
        if err is not None: return n1, err, a1, _

        n2, err, a2, astt_nodes = self.eat_sexp1()
        if err is not None: return n2, err, a2, astt_nodes

        def generate(s):
            if len(s) == 1:
                return s[0]
            return AstNode.make_plus_op(generate(s[:-1]), s[-1])

        new_sexps = [a1] + astt_nodes
        astt = generate(new_sexps)
        cst = CstNode(name=CST_SEXP, children=[n1,n2])

        return cst, None, astt, new_sexps

    def eat_sexp1(self) -> ParseResult:
        """SExp1 -> + SExp SExp1 | '' """
        c = self.save_cursor()
        node, err, astt, sexps = self.eat_sexp11()
        if err is None: return node, err, astt, sexps
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, sexps = self.eat_sexp12()
        if err is None: return node, err, astt, sexps
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_sexp11(self) -> ParseResult:
        """SExp1 -> + SExp SExp1"""
        n1, err, a1, _ = self.eat_plus()
        if err is not None: return n1, err, a1, _

        n2, err, a2, sexps2 = self.eat_sexp()
        if err is not None: return n2, err, a2, _

        n3, err, a3, sexps3 = self.eat_sexp1()
        if err is not None: return n3, err, a3, sexps3

        cst = CstNode(name=CST_SEXP1, children=[n1,n2,n3])
        astt = None

        return cst, None, astt, sexps2+sexps3

    def eat_sexp12(self) -> ParseResult:
        """SExp1 -> '' """
        cst = CstNode(name=CST_SEXP1, children=[CstNode.epsilon()])
        return cst, None, None, []

    def eat_atom(self) -> ParseResult:
        """
        Atom -> this Atom1
            | id Atom1
            | new cname ( ) Atom1
            | ( Exp ) Atom1
            | null Atom1
        """
        c = self.save_cursor()
        node, err, astt, _ = self.eat_atom01()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_atom02()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_atom03()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_atom04()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_atom05()
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_atom01(self) -> ParseResult:
        """Atom -> this Atom1"""
        n1, err, a1, _ = self.eat_this()
        if err is not None: return n1, err, a1, _

        n2, err, a2, head = self.eat_atom1()
        if err is not None: return n2, err, a2, head

        cst = CstNode(name=CST_ATOM, children=[n1,n2])

        if a2.name == AST_EPSILON:
            astt = a1
        else:
            a2.set_left_child(a1)
            astt = head

        return cst, None, astt, None

    def eat_atom02(self) -> ParseResult:
        """Atom -> id Atom1"""
        n1, err, a1, _ = self.eat_id()
        if err is not None: return n1, err, a1, _

        n2, err, a2, head = self.eat_atom1()
        if err is not None: return n2, err, a2, head

        cst = CstNode(name=CST_ATOM, children=[n1,n2])

        if a2.name == AST_EPSILON:
            astt = a1
        else:
            a2.set_left_child(a1)
            astt = head

        return cst, None, astt, None

    def eat_atom03(self) -> ParseResult:
        """Atom -> new cname ( ) Atom1"""
        n1, err, a1, _ = self.eat_new()
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_cname()
        if err is not None: return n2, err, a2, _

        n3, err, a3, _ = self.eat_l_paren()
        if err is not None: return n3, err, a3, _

        n4, err, a4, _ = self.eat_r_paren()
        if err is not None: return n4, err, a4, _

        n5, err, a5, head = self.eat_atom1()
        if err is not None: return n5, err, a5, head

        cst = CstNode(name=CST_ATOM, children=[n1,n2,n3,n4,n5])

        if a5.name == AST_EPSILON:
            astt = AstNode.make_class_instance_creation(a2)
        else:
            a5.set_left_child(AstNode.make_class_instance_creation(a2))
            astt = head

        return cst, None, astt, None

    def eat_atom04(self) -> ParseResult:
        """Atom -> ( Exp ) Atom1 """
        n1, err, _, _ = self.eat_l_paren()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_exp()
        if err is not None: return n2, err, a2, _

        n3, err, _, _ = self.eat_r_paren()
        if err is not None: return n3, err, _, _

        n4, err, a4, head = self.eat_atom1()
        if err is not None: return n4, err, a4, head

        cst = CstNode(name=CST_ATOM, children=[n1,n2,n3,n4])

        if a4.name == AST_EPSILON:
            astt = a2
        else:
            a4.set_left_child(a2)
            astt = head

        return cst, None, astt, None

    def eat_atom05(self) -> ParseResult:
        """Atom -> null Atom1 """
        n1, err, a1, _ = self.eat_null()
        if err is not None: return n1, err, a1, _

        n2, err, a2, head = self.eat_atom1()
        if err is not None: return n2, err, a2, head

        cst = CstNode(name=CST_ATOM, children=[n1,n2])

        if a2.name == AST_EPSILON:
            astt = a1
        else:
            a2.set_left_child(a1)
            astt = head

        return cst, None, astt, None

    def eat_atom1(self) -> ParseResult:
        """Atom1 -> . id Atom1 | ( ExpList ) Atom1 | ( ) Atom1 | '' """
        # try to eat the most at each step
        c = self.save_cursor()
        node, err, astt, head = self.eat_atom11()
        if err is None: return node, err, astt, head
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, head = self.eat_atom12()
        if err is None: return node, err, astt, head
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, head = self.eat_atom13()
        if err is None: return node, err, astt, head
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, head = self.eat_atom14()
        if err is None: return node, err, astt, head
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_atom11(self) -> ParseResult:
        """Atom1 -> . id Atom1"""
        n1, err, _, _ = self.eat_dot()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_id()
        if err is not None: return n2, err, a2, _

        n3, err, a3, head = self.eat_atom1()
        if err is not None: return n3, err, a3, head

        cst = CstNode(name=CST_ATOM1, children=[n1, n2, n3])
        if a3.name == AST_EPSILON:
            astt = AstNode.make_field_access(None, a2)
            head = astt
        else:
            # replace the left child (should be None)
            astt = AstNode.make_field_access(None, a2)
            a3.set_left_child(astt)

        return cst, None, astt, head

    def eat_atom12(self) -> ParseResult:
        """Atom1 -> ( ExpList ) Atom1"""
        n1, err, _, _ = self.eat_l_paren()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_explist()
        if err is not None: return n2, err, a2, _

        n3, err, _, _ = self.eat_r_paren()
        if err is not None: return n3, err, _, _

        n4, err, a4, head = self.eat_atom1()
        if err is not None: return n4, err, a4, head

        if a4.name == AST_EPSILON:
            astt = AstNode.make_method_call(None, a2)
            head = astt
        else:
            # replace the left child (should be None)
            astt = AstNode.make_method_call(None, a2)
            a4.set_left_child(astt)

        cst = CstNode(name=CST_ATOM1, children=[n1, n2, n3, n4])

        return cst, None, astt, head

    def eat_atom13(self) -> ParseResult:
        """Atom1 -> ( ) Atom1"""
        n1, err, _, _ = self.eat_l_paren()
        if err is not None: return n1, err, _, _

        n2, err, _, _ = self.eat_r_paren()
        if err is not None: return n2, err, _, _

        n3, err, a3, head = self.eat_atom1()
        if err is not None: return n3, err, a3, head

        if a3.name == AST_EPSILON:
            astt = AstNode.make_method_call(None, AstNode.make_explist([]))
            head = astt
        else:
            # replace the left child (should be None)
            astt = AstNode.make_method_call(None, AstNode.make_explist([]))
            a3.set_left_child(astt)

        cst = CstNode(name=CST_ATOM1, children=[n1, n2, n3])

        return cst, None, astt, head

    def eat_atom14(self) -> ParseResult:
        """Atom1 -> '' """
        return CstNode(name=CST_ATOM1, children=[CstNode.epsilon()]), None, AstNode.epsilon(), None

    def eat_explist(self) -> Tuple[CstNode, Optional[Error], Optional[ExpList], Any]:
        """ExpList -> Exp ExpList1 """
        n1, err, a1, _ = self.eat_exp()
        if err is not None: return n1, err, a1, _ # exp node

        n2, err, a2, _ = self.eat_explist1() # explist node
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_EXPLIST, children=[n1,n2])
        astt = AstNode.make_explist([a1] + a2.children)

        return cst, None, astt, None

    def eat_explist1(self) -> Tuple[CstNode, Optional[Error], Optional[ExpList], Any]:
        """"ExpList1 -> ExpRest ExpList1 | '' """
        c = self.save_cursor()
        node, err, astt, _ = self.eat_explist11() # explist node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        c = self.save_cursor()
        node, err, astt, _ = self.eat_explist12() # explist node
        if err is None: return node, err, astt, _
        self.backtrack(c)

        return CstNode.empty(), self.generic_syntax_err(), None, None

    def eat_explist11(self) -> Tuple[CstNode, Optional[Error], Optional[ExpList], Any]:
        """ExpList1 -> ExpList ExpList1"""
        n1, err, a1, _ = self.eat_exprest() # explist node
        if err is not None: return n1, err, a1, _

        n2, err, a2, _ = self.eat_explist1() # explist node
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_EXPLIST1, children=[n1,n2])
        astt = AstNode.make_explist(a1.children + a2.children)

        return cst, None, astt, None

    def eat_explist12(self) -> Tuple[CstNode, Optional[Error], Optional[ExpList], Any]:
        """ExpList1 -> '' """
        return CstNode(name=CST_EXPLIST1, children=[CstNode.epsilon()]), None, AstNode.make_explist([]), None

    def eat_exprest(self) -> Tuple[CstNode, Optional[Error], Optional[ExpList], Any]:
        """ExpRest -> , Exp"""
        n1, err, _, _ = self.eat_comma()
        if err is not None: return n1, err, _, _

        n2, err, a2, _ = self.eat_exp()
        if err is not None: return n2, err, a2, _

        cst = CstNode(name=CST_EXPREST, children=[n1,n2])
        astt = AstNode.make_explist([a2])

        return cst, None, astt, None

    """
    ######################## PRODUCTIONS (TERMINALS) ########################
    """
    def eat_class(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_class():
            return CstNode.empty(), self.syntax_err(f"expected 'class', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.class_kw(tok), None, None, None

    def eat_cname(self) -> Tuple[CstNode, Optional[Error], Optional[Cname], Any]:
        tok = self.curr_token
        if not self.is_cname_type():
            return CstNode.empty(), self.syntax_err(f"expected <classname>, got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.cname_type(tok), None, AstNode.make_cname(tok), None

    def eat_int_type(self) -> Tuple[CstNode, Optional[Error], Optional[Int], Any]:
        tok = self.curr_token
        if not self.is_int_type():
            return CstNode.empty(), self.syntax_err(f"expected 'Int', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.int_type(tok), None, AstNode.make_int(), None

    def eat_bool_type(self) -> Tuple[CstNode, Optional[Error], Optional[Bool], Any]:
        tok = self.curr_token
        if not self.is_bool_type():
            return CstNode.empty(), self.syntax_err(f"expected 'Bool', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.bool_type(tok), None, AstNode.make_bool(), None

    def eat_str_type(self) -> Tuple[CstNode, Optional[Error], Optional[String], Any]:
        tok = self.curr_token
        if not self.is_str_type():
            return CstNode.empty(), self.syntax_err(f"expected 'String', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.str_type(tok), None, AstNode.make_string(), None

    def eat_void_type(self) -> Tuple[CstNode, Optional[Error], Optional[Void], Any]:
        tok = self.curr_token
        if not self.is_void_type():
            return CstNode.empty(), self.syntax_err(f"expected 'Void', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.void_type(tok), None, AstNode.make_void(), None

    def eat_l_curly_brace(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_l_curly_brace():
            return CstNode.empty(), self.syntax_err(f"expected '{{', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.l_curly_brace(tok), None, None, None

    def eat_r_curly_brace(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_r_curly_brace():
            return CstNode.empty(), self.syntax_err(f"expected '}}', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.r_curly_brace(tok), None, None, None

    def eat_l_paren(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_l_paren():
            return CstNode.empty(), self.syntax_err(f"expected '(', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.l_paren(tok), None, None, None

    def eat_r_paren(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_r_paren():
            return CstNode.empty(), self.syntax_err(f"expected ')', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.r_paren(tok), None, None, None

    def eat_semicolon(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_semicolon():
            return CstNode.empty(), self.syntax_err(f"expected ';', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.semicolon(tok), None, None, None

    def eat_comma(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_comma():
            return CstNode.empty(), self.syntax_err(f"expected ',', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.comma(tok), None, None, None

    def eat_dot(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_dot():
            return CstNode.empty(), self.syntax_err(f"expected '.', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.dot(tok), None, None, None

    def eat_id(self) -> Tuple[CstNode, Optional[Error], Optional[Id], Any]:
        tok = self.curr_token
        if not self.is_id():
            return CstNode.empty(), self.syntax_err(f"expected <id>, got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.id(tok), None, AstNode.make_id(tok), None

    def eat_plus(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_plus():
            return CstNode.empty(), self.syntax_err(f"expected '+', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.plus(tok), None, None, None

    def eat_minus(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_minus():
            return CstNode.empty(), self.syntax_err(f"expected '-', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.minus(tok), None, None, None

    def eat_mult(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_mult():
            return CstNode.empty(), self.syntax_err(f"expected '*', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.mult(tok), None, None, None

    def eat_div(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_div():
            return CstNode.empty(), self.syntax_err(f"expected '/', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.div(tok), None, None, None

    def eat_assign(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_assign():
            return CstNode.empty(), self.syntax_err(f"expected '=', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.assign(tok), None, None, None

    def eat_dbl_eq(self) -> Tuple[CstNode, Optional[Error], Optional[Eq], Any]:
        tok = self.curr_token
        if not self.is_dbl_eq():
            return CstNode.empty(), self.syntax_err(f"expected '==', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.dbl_eq(tok), None, AstNode.make_eq(), None

    def eat_lt(self) -> Tuple[CstNode, Optional[Error], Optional[Lt], Any]:
        tok = self.curr_token
        if not self.is_lt():
            return CstNode.empty(), self.syntax_err(f"expected '<', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.lt(tok), None, AstNode.make_lt(), None

    def eat_gt(self) -> Tuple[CstNode, Optional[Error], Optional[Gt], Any]:
        tok = self.curr_token
        if not self.is_gt():
            return CstNode.empty(), self.syntax_err(f"expected '>', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.gt(tok), None, AstNode.make_gt(), None

    def eat_le(self) -> Tuple[CstNode, Optional[Error], Optional[Le], Any]:
        tok = self.curr_token
        if not self.is_le():
            return CstNode.empty(), self.syntax_err(f"expected '<=', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.le(tok), None, AstNode.make_le(), None

    def eat_ge(self) -> Tuple[CstNode, Optional[Error], Optional[Ge], Any]:
        tok = self.curr_token
        if not self.is_ge():
            return CstNode.empty(), self.syntax_err(f"expected '>=', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.ge(tok), None, AstNode.make_ge(), None

    def eat_ne(self) -> Tuple[CstNode, Optional[Error], Optional[Ne], Any]:
        tok = self.curr_token
        if not self.is_ne():
            return CstNode.empty(), self.syntax_err(f"expected '!=', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.ne(tok), None, AstNode.make_ne(), None

    def eat_if(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_if():
            return CstNode.empty(), self.syntax_err(f"expected 'if', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.if_kw(tok), None, None, None

    def eat_else(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_else():
            return CstNode.empty(), self.syntax_err(f"expected 'else', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.else_kw(tok), None, None, None

    def eat_while(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_while():
            return CstNode.empty(), self.syntax_err(f"expected 'while', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.while_kw(tok), None, None, None

    def eat_readln(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_readln():
            return CstNode.empty(), self.syntax_err(f"expected 'readln', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.readln_kw(tok), None, None, None # not a terminal astt since may accept args

    def eat_println(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_println():
            return CstNode.empty(), self.syntax_err(f"expected 'println', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.println_kw(tok), None, None, None # not a terminal astt since may accept args

    def eat_return(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_return():
            return CstNode.empty(), self.syntax_err(f"expected 'return', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.return_kw(tok), None, None, None # since return may include exp, not considered as terminal

    def eat_true(self) -> Tuple[CstNode, Optional[Error], Optional[TrueLit], Any]:
        tok = self.curr_token
        if not self.is_true():
            return CstNode.empty(), self.syntax_err(f"expected 'true', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.true_kw(tok), None, AstNode.make_true(tok), None

    def eat_false(self) -> Tuple[CstNode, Optional[Error], Optional[FalseLit], Any]:
        tok = self.curr_token
        if not self.is_false():
            return CstNode.empty(), self.syntax_err(f"expected 'false', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.false_kw(tok), None, AstNode.make_false(tok), None

    def eat_this(self) -> Tuple[CstNode, Optional[Error], Optional[This], Any]:
        tok = self.curr_token
        if not self.is_this():
            return CstNode.empty(), self.syntax_err(f"expected 'this', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.this_kw(tok), None, AstNode.make_this(tok), None

    def eat_new(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_new():
            return CstNode.empty(), self.syntax_err(f"expected 'new', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.new_kw(tok), None, None, None

    def eat_null(self) -> Tuple[CstNode, Optional[Error], Optional[Null], Any]:
        tok = self.curr_token
        if not self.is_null():
            return CstNode.empty(), self.syntax_err(f"expected 'null', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.null_kw(tok), None, AstNode.make_null(tok), None

    def eat_or(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_or():
            return CstNode.empty(), self.syntax_err(f"expected '||', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.boolean_or(tok), None, None, None

    def eat_and(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_and():
            return CstNode.empty(), self.syntax_err(f"expected '&&', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.boolean_and(tok), None, None, None

    def eat_exclamation(self) -> Tuple[CstNode, Optional[Error], None, Any]:
        tok = self.curr_token
        if not self.is_exclamation():
            return CstNode.empty(), self.syntax_err(f"expected '!', got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.exclamation(tok), None, None, None

    def eat_int_literal(self) -> Tuple[CstNode, Optional[Error], Optional[IntegerLiteral], Any]:
        tok = self.curr_token
        if not self.is_int_literal():
            return CstNode.empty(), self.syntax_err(f"expected <int_literal>, got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.int_literal(tok), None, AstNode.make_integer_literal(tok), None

    def eat_str_literal(self) -> Tuple[CstNode, Optional[Error], Optional[StringLiteral], Any]:
        tok = self.curr_token
        if not self.is_str_literal():
            return CstNode.empty(), self.syntax_err(f"expected <str_literal>, got {self.curr_token}", self.curr_token), None, None
        self.advance()
        return CstNode.str_literal(tok), None, AstNode.make_string_literal(tok), None

    """
    ######################## HELPERS ########################
    """
    def is_class(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == CLASS

    def is_if(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == IF

    def is_else(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == ELSE

    def is_while(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == WHILE

    def is_readln(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == READLN

    def is_println(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == PRINTLN

    def is_return(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == RETURN

    def is_true(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == TRUE

    def is_false(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == FALSE

    def is_this(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == THIS

    def is_new(self) -> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == NEW

    def is_null(self)-> bool:
        return self.curr_token.type == TT_KEYWORD and self.curr_token.value == NULL

    def is_cname_type(self) -> bool:
        return self.curr_token.type == TT_TYPE and self.curr_token.value not in (INT, BOOL, STRING, VOID)

    def is_int_type(self):
        return self.curr_token.type == TT_TYPE and self.curr_token.value == INT

    def is_bool_type(self):
        return self.curr_token.type == TT_TYPE and self.curr_token.value == BOOL

    def is_str_type(self):
        return self.curr_token.type == TT_TYPE and self.curr_token.value == STRING

    def is_void_type(self):
        return self.curr_token.type == TT_TYPE and self.curr_token.value == VOID

    def is_l_curly_brace(self) -> bool:
        return self.curr_token.type == TT_L_CURLY_BRACE

    def is_r_curly_brace(self) -> bool:
        return self.curr_token.type == TT_R_CURLY_BRACE

    def is_l_paren(self) -> bool:
        return self.curr_token.type == TT_L_PAREN

    def is_r_paren(self) -> bool:
        return self.curr_token.type == TT_R_PAREN

    def is_semicolon(self) -> bool:
        return self.curr_token.type == TT_SEMICOLON

    def is_comma(self) -> bool:
        return self.curr_token.type == TT_COMMA

    def is_dot(self) -> bool:
        return self.curr_token.type == TT_DOT

    def is_id(self) -> bool:
        return self.curr_token.type == TT_ID

    def is_plus(self) -> bool:
        return self.curr_token.type == TT_PLUS

    def is_minus(self) -> bool:
        return self.curr_token.type == TT_MINUS

    def is_mult(self) -> bool:
        return self.curr_token.type == TT_MULT

    def is_div(self) -> bool:
        return self.curr_token.type == TT_DIV

    def is_assign(self) -> bool:
        return self.curr_token.type == TT_ASSIGNMENT

    def is_dbl_eq(self) -> bool:
        return self.curr_token.type == TT_EQUAL

    def is_lt(self) -> bool:
        return self.curr_token.type == TT_LESS_THAN

    def is_gt(self) -> bool:
        return self.curr_token.type == TT_GREATER_THAN

    def is_le(self) -> bool:
        return self.curr_token.type == TT_LESS_EQ

    def is_ge(self) -> bool:
        return self.curr_token.type == TT_GREATER_EQ

    def is_ne(self) -> bool:
        return self.curr_token.type == TT_NOT_EQ

    def is_or(self) -> bool:
        return self.curr_token.type == TT_OR

    def is_and(self) -> bool:
        return self.curr_token.type == TT_AND

    def is_exclamation(self) -> bool:
        return self.curr_token.type == TT_EXCLAMATION

    def is_int_literal(self) -> bool:
        return self.curr_token.type == TT_INT

    def is_str_literal(self) -> bool:
        return self.curr_token.type == TT_STR

    def generic_syntax_err(self):
        return IllegalSyntaxError(desc="invalid syntax", error_pos=self.curr_token.lexed_pos)

    def syntax_err(self, desc: str, token: Token=None):
        return IllegalSyntaxError(desc=desc, error_pos=token.lexed_pos)

def run(text: str, filename: str):
    # generate tokens
    lexer = Lexer(text, filename)
    tokens, err = lexer.lex()
    if err:
        return tokens, err

    return tokens, None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse.py <filename>")
        exit(1)

    filename = sys.argv[1]

    # open file, lex input text, print out all tokens
    with open(filename) as f:
        text = f.read()

        tokens, err = run(text, filename)
        if err is not None:
            print(err)
            return

        print(tokens)

if __name__ == "__main__":
    main()