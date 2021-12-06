import lex
from ir3 import *
from typing import List, Set, Dict, Tuple, Optional, Callable, Optional, Any, Union, Type

######################################################################
######################## ABSTRACT SYNTAX TREE ########################
######################################################################

AST_PROGRAM = "PROGRAM"
AST_MAINCLASS = "MAINCLASS"
AST_CLASSDECL = "CLASSDECL"
AST_CLASSDECLS = "CLASSDECLS"
AST_CNAME = "CNAME"
AST_MDDECL = "MDDECL"
AST_MDDECLS = "MDDECLS"
AST_BLOCK = "BLOCK"
AST_VARDECLS = "VARDECLS"
AST_VARDECL = "VARDECL"
AST_STMTS = "STMTS"
AST_ID = "ID"
AST_FMLLIST = "PARAMETERS"
AST_MDBODY = "MDBODY"
AST_FML = "PARAMETER"
AST_TYPE = "TYPE"
AST_INT = "INT"
AST_BOOL = "BOOL"
AST_STRING = "STRING"
AST_VOID = "VOID"
AST_IF_STATEMENT = "IF"
AST_CONDITIONAL_EXP = "CONDITIONAL"
AST_IF_BODY = "IF_BODY"
AST_ELSE_BODY = "ELSE_BODY"
AST_WHILE = "WHILE"
AST_WHILE_BODY = "WHILE_BODY"
AST_READLN = "READLN"
AST_PRINTLN = "PRINTLN"
AST_METHOD_CALL = "METHOD_CALL"
AST_EXPLIST = "EXPLIST"
AST_RETURN = "RETURN"
AST_FIELD_ACCESS = "FIELD_ACCESS"
AST_EXP = "EXP"
AST_BEXP = "BEXP"
AST_SEXP = "SEXP"
AST_CONJ = "CONJ"
AST_AND = "&&"
AST_OR = "||"
AST_REXP = "REXP"
AST_BGRD = "BGRD"
AST_BOP = "BOP"
AST_LT = "<"
AST_GT = ">"
AST_LE = "<="
AST_GE = ">="
AST_EQ = "=="
AST_NE = "!="
AST_TRUE = "TRUE"
AST_FALSE = "FALSE"
AST_ATOM = "ATOM"
AST_TERM = "TERM"
AST_NEGATE = '!'
AST_PLUS = "+ ADD"
AST_MINUS = "- MINUS"
AST_MULT = "*"
AST_DIV = "/"
AST_FACTOR = "FTR"
AST_INT_LITERAL = "INT_LITERAL"
AST_STR_LITERAL = "STR_LITERAL"
AST_CONCAT = "+ CONCAT"
AST_EPSILON = "EPSILON"
AST_UNEGATIVE = "- UNEG"
AST_THIS = "THIS"
AST_CLASS_INSTANCE_CREATION = "CLASS_INSTANCE_CREATION"
AST_NULL = "NULL"
AST_RETURN_STATEMENT = "RETURN_STATEMENT"
AST_ASSIGNMENT_STATEMENT = "ASSIGNMENT_STATEMENT"

# Hack to retrieve all string literals associated with a program
string_literals = []
def get_string_literals():
    return string_literals

class AstNode:

    @classmethod
    def epsilon(cls) -> 'AstNode':
        return AstNode(AST_EPSILON)

    ######################### NONTERMINALS #########################
    @classmethod
    def make_program(cls, mainclass: 'MainClass', classdecls: 'ClassDecls') -> 'Program':
        return Program(mainclass, classdecls)

    @classmethod
    def make_mainclass(cls, cname: 'Cname', mainmd: 'MdDecl') -> 'MainClass':
        return MainClass(cname, mainmd)

    @classmethod
    def make_classdecls(cls, classdecls: List['ClassDecl']) -> 'ClassDecls':
        return ClassDecls(classdecls)

    @classmethod
    def make_classdecl(cls, cname: 'Cname', vardecls: 'VarDecls', mddecls: 'MdDecls') -> 'ClassDecl':
        return ClassDecl(cname, vardecls, mddecls)

    @classmethod
    def make_mddecls(cls, mddecls: List['MdDecl']) -> 'MdDecls':
        return MdDecls(mddecls)

    @classmethod
    def make_mddecl(cls, type: 'AstType', id: 'Id', fmllist: 'FmlList', mdbody: 'MdBody') -> 'MdDecl':
        return MdDecl(type, id, fmllist, mdbody)

    @classmethod
    def make_fmllist(cls, fmls: List['Fml']) -> 'FmlList':
        return FmlList(fmls)

    @classmethod
    def make_fml(cls, type_node: 'AstType', id_node: 'Id') -> 'Fml':
        return Fml(type_node, id_node)

    @classmethod
    def make_mdbody(cls, vardecls: 'VarDecls', stmts: 'Stmts') -> 'MdBody':
        return MdBody(vardecls, stmts)

    @classmethod
    def make_vardecls(cls, vardecls: List['VarDecl']) -> 'VarDecls':
        return VarDecls(vardecls)

    @classmethod
    def make_vardecl(cls, type: 'AstType', id: 'Id') -> 'VarDecl':
        return VarDecl(type, id)

    @classmethod
    def make_stmts(cls, stmts: List['AstNode']) -> 'Stmts':
        return Stmts(stmts)

    @classmethod
    def make_if_statement(cls, conditional: 'Exp', if_body: 'Stmts', else_body: 'Stmts') -> 'IfStatement':
        return IfStatement(conditional, if_body, else_body)

    @classmethod
    def make_while_statement(cls, conditional: 'AstNode', while_body: 'AstNode') -> 'WhileStatement':
        return WhileStatement(conditional, while_body)

    @classmethod
    def make_exp(cls, actual_exp: 'AstNode') -> 'Exp':
        return Exp(actual_exp)

    @classmethod
    def make_explist(cls, exps: List['Exp']) -> 'ExpList':
        return ExpList(exps)

    @classmethod
    def make_complement(cls, bgrd_atom_true_false: 'AstNode') -> 'Complement':
        return Complement(bgrd_atom_true_false)

    @classmethod
    def make_and_op(cls, left: 'AstNode', right: 'AstNode') -> 'AndOp':
        return AndOp(left, right)

    @classmethod
    def make_or_op(cls, left: 'AstNode', right: 'AstNode') -> 'OrOp':
        return OrOp(left, right)

    @classmethod
    def make_plus_op(cls, left: 'AstNode', right: 'AstNode') -> 'PlusOp':
        return PlusOp(left, right)

    @classmethod
    def make_minus_op(cls, left: 'AstNode', right: 'AstNode') -> 'MinusOp':
        return MinusOp(left, right)

    @classmethod
    def make_mult_op(cls, left: 'AstNode', right: 'AstNode') -> 'MultOp':
        return MultOp(left, right)

    @classmethod
    def make_div_op(cls, left: 'AstNode', right: 'AstNode') -> 'DivOp':
        return DivOp(left, right)

    @classmethod
    def make_unegative(cls, factor: 'AstNode') -> 'Unegative':
        return Unegative(factor)

    @classmethod
    def make_class_instance_creation(cls, cname: 'Cname') -> 'ClassInstanceCreation':
        return ClassInstanceCreation(cname)

    @classmethod
    # due to how we construct the ast, left may be None, but the final ast won't have None.
    def make_field_access(cls, left: Optional['AstNode'], id: 'Id') -> 'FieldAccess':
        return FieldAccess(left, id)

    @classmethod
    # due to how we construct the ast, left may be None, but the final ast won't have None.
    def make_method_call(cls, left: Optional['AstNode'], explist: 'ExpList') -> 'MethodCall':
        return MethodCall(left, explist)

    @classmethod
    def make_return_statement(cls, exp: Optional['AstNode']=None) -> 'ReturnStatement':
        return ReturnStatement(exp)

    @classmethod
    def make_assignment_statement(cls, left: 'AstNode', right: 'AstNode') -> 'AssignmentStatement':
        return AssignmentStatement(left, right)

    @classmethod
    def make_println(cls, exp: 'AstNode') -> 'Println':
        return Println(exp)

    @classmethod
    def make_readln(cls, idd: 'Id')-> 'Readln':
        return Readln(idd)

    @classmethod
    def make_lt(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Lt':
        return Lt(lhs, rhs)

    @classmethod
    def make_gt(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Gt':
        return Gt(lhs, rhs)

    @classmethod
    def make_le(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Le':
        return Le(lhs, rhs)

    @classmethod
    def make_ge(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Ge':
        return Ge(lhs, rhs)

    @classmethod
    def make_eq(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Eq':
        return Eq(lhs, rhs)

    @classmethod
    def make_ne(cls, lhs: 'AstNode'=None, rhs: 'AstNode'=None) -> 'Ne':
        return Ne(lhs, rhs)

    ######################### TERMINALS #########################

    @classmethod
    def make_int(cls) -> 'Int':
        return Int()

    @classmethod
    def make_bool(cls) -> 'Bool':
        return Bool()

    @classmethod
    def make_string(cls) -> 'String':
        return String()

    @classmethod
    def make_void(cls) -> 'Void':
        return Void()

    @classmethod
    def make_cname(cls, tok: lex.Token) -> 'Cname':
        # except the first letter, uppercase letters are not distinguished from lowercase
        tok.value = tok.value.lower().capitalize()
        return Cname(tok)

    @classmethod
    def make_id(cls, tok: lex.Token) -> 'Id':
        # except the first letter, uppercase letters are not distinguished from lowercase
        tok.value = tok.value.lower()
        return Id(tok)

    @classmethod
    def make_true(cls, tok: lex.Token) -> 'TrueLit':
        return TrueLit(tok)

    @classmethod
    def make_false(cls, tok: lex.Token) -> 'FalseLit':
        return FalseLit(tok)

    @classmethod
    def make_integer_literal(cls, tok: lex.Token) -> 'IntegerLiteral':
        return IntegerLiteral(tok)

    @classmethod
    def make_string_literal(cls, tok: lex.Token) -> 'StringLiteral':
        return StringLiteral(tok)

    @classmethod
    def make_this(cls, tok: lex.Token) -> 'This':
        return This(tok)

    @classmethod
    def make_null(cls, tok: lex.Token) -> 'Null':
        return Null(tok)

    def __init__(self, name: str, value: lex.Token=None, children=None):
        if children is None:
            children = []
        self.name = name
        self.value = value
        self.children = children

    def set_left_child(self, node: 'AstNode'):
        if len(self.children) != 2:
            raise AssertionError("set_left_child")
        self.children[0] = node

    def set_right_child(self, node: 'AstNode'):
        if len(self.children) != 2:
            raise AssertionError("set_right_child")
        self.children[1] = node

    # must be overriden
    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        raise RuntimeError("static_check not defined on AstNode")

    # must be overriden
    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError("ir3 not defined on AstNode")

    def __repr__(self):
        if self.value:
            return f"AstNode({self.name}, {self.value})"
        return f"AstNode({self.name})"

    def __str__(self):
        return print_tree(self, 0)

########################### NONTERMINAL AST NODES ###########################

class Program(AstNode):
    def __init__(self, mainclass: 'MainClass', classdecls: 'ClassDecls'):
        super().__init__(name=AST_PROGRAM, children=[mainclass,classdecls])
        # persist the type env for ir3 later
        self.type_env = None

    @property
    def mainclass(self) -> 'MainClass':
        return self.children[0]

    @property
    def classdecls(self) -> 'ClassDecls':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        # distinct name-checking done during initialization
        self.type_env = TypeEnvironment.initialize(self.mainclass, self.classdecls)
        # print(type_env)

        # type check
        self.mainclass.static_check(self.type_env, metadata)
        self.classdecls.static_check(self.type_env, metadata)

    def ir3(self, context: Dict[str, Any]) -> Program3:
        cdata3_list = []
        cmtd3_list = []

        # fill in main class
        main_class: MainClass = self.mainclass
        main_classname = main_class.cname.class_name
        # pass classname down to child nodes (e.g method call nodes need to mangle names too)
        context["classname"] = main_classname
        main_md: MdDecl = main_class.mainmd

        # fill in cdata3 of main class
        fds, msigs = self.type_env.class_lookup(main_classname)
        vardecls = [VarDecl3(type3, id3) for id3, type3 in fds.items()]
        cdata3_list.append(CData3(main_classname, vardecls))

        # fill in cmtd3 of main class
        for mname, msig in msigs.items():
            fmllist, rettype = msig
            fmllist3: FmlList3 = FmlList3(main_classname, [Fml3(JClass(main_classname), "this")] + [Fml3(type3, id3) for id3, type3 in fmllist])
            context["parameters"] = fmllist3.fml3_list
            context["localvars"] = main_md.mdbody.vardecls.vardecl_list
            # generate ir3 for a single method
            mdbody3: MdBody3 = main_md.mdbody.ir3(context)
            # generate mangled method name, e.g %Functional_f(a, b)
            mangled_mname = IR3Node.mangle_method_name(context["classname"], mname)
            cmtd3 = CMtd3(rettype, mangled_mname, fmllist3, mdbody3)
            cmtd3_list.append(cmtd3)

        # fill in class decls (and their methods)
        class_decls: ClassDecls = self.classdecls
        for class_decl_node in class_decls.classdecls:
            classname = class_decl_node.cname.class_name
            # pass classname down to child nodes (e.g method call nodes need to mangle names too)
            context["classname"] = classname
            md_decls: MdDecls = class_decl_node.mddecls

            # fill in cdata3 of current class
            fds, msigs = self.type_env.class_lookup(classname)
            vardecls = [VarDecl3(type3, id3) for id3, type3 in fds.items()]
            cdata3_list.append(CData3(classname, vardecls))

            # fill in cmtd3 of current class
            for md_decl_node in md_decls.mddecl_list:
                md_name = md_decl_node.id_node.id_name
                md_sig = msigs[md_name]
                md_fml_list, md_ret_type = md_sig
                fmllist3: FmlList3 = FmlList3(classname, [Fml3(JClass(classname), "this")] + [Fml3(type3, id3) for id3, type3 in md_fml_list])
                # fill in local variables (to handle "this")
                context["parameters"] = fmllist3.fml3_list
                context["localvars"] = md_decl_node.mdbody.vardecls.vardecl_list
                # generate ir3 for a single method
                mdbody3: MdBody3 = md_decl_node.mdbody.ir3(context)
                # generate mangled method name, e.g %Functional_f(a, b)
                mangled_mdname = IR3Node.mangle_method_name(context["classname"], md_name)
                cmtd3 = CMtd3(md_ret_type, mangled_mdname, fmllist3, mdbody3)
                cmtd3_list.append(cmtd3)

        return Program3(cdata3_list, cmtd3_list)

class MainClass(AstNode):
    def __init__(self, cname: 'Cname', mainmd: 'MdDecl'):
        super().__init__(name=AST_MAINCLASS, children=[cname,mainmd])

    @property
    def cname(self) -> 'Cname':
        return self.children[0]

    @property
    def mainmd(self) -> 'MdDecl':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        # retrieve details for current class
        cid = self.cname.class_name
        field_decls, mtd_sigs = type_env.class_lookup(cid)
        field_decls["this"] = JClass(cid)

        # fill a local environment with main method (basically follow the appendix)
        child_env = type_env.child_env()
        child_env.augment_fields(field_decls)
        child_env.augment_msigs(mtd_sigs)

        # then type check the main method
        self.mainmd.static_check(child_env, cid)

        # cleanup
        del field_decls["this"]

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class ClassDecls(AstNode):
    def __init__(self, classdecls: List['ClassDecl']):
        super().__init__(name=AST_CLASSDECLS, children=classdecls)

    @property
    def classdecls(self) -> List['ClassDecl']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        for classdecl in self.classdecls:
            classdecl.static_check(type_env, metadata)

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class ClassDecl(AstNode):
    def __init__(self, cname: 'Cname', vardecls: 'VarDecls', mddecls: 'MdDecls'):
        super().__init__(name=AST_CLASSDECL, children=[cname,vardecls,mddecls])

    @property
    def cname(self) -> 'Cname':
        return self.children[0]

    @property
    def vardecls(self) -> 'VarDecls':
        return self.children[1]

    @property
    def mddecls(self) -> 'MdDecls':
        return self.children[2]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        # retrieve details for current class
        cid = self.cname.class_name
        field_decls, mtd_sigs = type_env.class_lookup(cid)
        field_decls["this"] = JClass(cid)

        # create a new local environment for child class (has block)
        child_env = type_env.child_env()
        child_env.augment_fields(field_decls)
        child_env.augment_msigs(mtd_sigs)

        # check all methods are OK in the current environment
        self.mddecls.static_check(child_env, cid)

        # cleanup
        del field_decls["this"]

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class MdDecls(AstNode):
    def __init__(self, mddecls: List['MdDecl']):
        super().__init__(name=AST_MDDECLS, children=mddecls)

    @property
    def mddecl_list(self) -> List['MdDecl']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment'=None, cid=None):
        for mddecl in self.mddecl_list:
            mddecl.static_check(type_env, cid)

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class MdDecl(AstNode):
    def __init__(self, type_node: 'AstType',
                 id_node: 'Id',
                 fmllist: 'FmlList',
                 mdbody: 'MdBody'):
        super().__init__(name=AST_MDDECL, children=[type_node, id_node, fmllist, mdbody])
        self._type_env = None

    @property
    def type_node(self) -> 'AstType':
        return self.children[0]

    @property
    def id_node(self) -> 'Id':
        return self.children[1]

    @property
    def fmllist(self) -> 'FmlList':
        return self.children[2]

    @property
    def mdbody(self) -> 'MdBody':
        return self.children[3]

    def static_check(self, type_env: 'TypeEnvironment' = None, cid=None):
        # augment a new env with params and return type of method
        stuff = type_env.class_lookup(cid)
        if not stuff:
            raise TypeCheckError(f"unexpected cname '{cid}' in Mddecl")

        msigs: Dict[str, MethodSignature] = stuff[1]
        mid = self.id_node.id_name
        params_list, ret_type = msigs[mid]

        # add params and the special return type before checking MDecl
        child_env = type_env.child_env()
        child_env.augment_field("Ret", ret_type)
        for param_name, param_type in params_list:
            child_env.augment_field(param_name, param_type)

        # add local variable declarations before checking method body
        for vardecl_node in self.mdbody.vardecls.vardecl_list:
            localvar_type: JLiteType = node_to_type(vardecl_node.type_node)
            localvar_id = vardecl_node.id_node.id_name
            child_env.augment_field(localvar_id, localvar_type)

        # type-check the method body block
        mdbody_type = self.mdbody.static_check(child_env, cid)
        if mdbody_type != ret_type:
            raise TypeCheckError(f"types {mdbody_type} and {ret_type} must match for class {cid} method {mid}")

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class FmlList(AstNode):
    def __init__(self, fmls: List['Fml']):
        super().__init__(name=AST_FMLLIST, children=fmls)

    @property
    def fmls(self) -> List['Fml']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        pass

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Fml(AstNode):
    def __init__(self, type_node: 'AstType', id_node: AstNode):
        super().__init__(name=AST_FML, children=[type_node, id_node])

    @property
    def type_node(self) -> 'AstType':
        return self.children[0]

    @property
    def id_node(self) -> 'Id':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        pass

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class MdBody(AstNode):
    def __init__(self, vardecls: 'VarDecls', stmts: 'Stmts'):
        super().__init__(name=AST_MDBODY, children=[vardecls,stmts])
        self._type_env = None

    @property
    def vardecls(self) -> 'VarDecls':
        return self.children[0]

    @property
    def stmts(self) -> 'Stmts':
        return self.children[1]

    @property
    def type_env(self) -> 'TypeEnvironment':
        return self._type_env

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        self._type_env = type_env
        return self.stmts.static_check(type_env, metadata)

    def ir3(self, context: Dict[str, Any]) -> 'MdBody3':
        vardecl3_lst = []
        stmt3s_lst = []

        # load var decls
        for var_decl_node in self.vardecls.vardecl_list:
            var_id: str = var_decl_node.id_node.id_name
            var_type: JLiteType = self.type_env.field_lookup(var_id)
            vardecl3 = VarDecl3(var_type, var_id)
            vardecl3_lst.append(vardecl3)

        # load stmts (ir3 representation)
        stmts_code, _ = self.stmts.ir3(context)
        stmt3s_lst.extend(stmts_code)

        # add return type declaration (if any)
        if "return" in context:
            type3, id3 = context["return"]
            stmt3s_lst.insert(0, VarDecl3(type3, id3))
            del context["return"]

        return MdBody3(vardecl3_lst, stmt3s_lst)

class VarDecls(AstNode):
    def __init__(self, vardecls: List['VarDecl']):
        super().__init__(name=AST_VARDECLS, children=vardecls)

    @property
    def vardecl_list(self) -> List['VarDecl']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        pass

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class VarDecl(AstNode):
    def __init__(self, type_node: 'AstType', id_node: 'Id'):
        super().__init__(name=AST_VARDECL, children=[type_node, id_node])

    @property
    def type_node(self) -> 'AstType':
        return self.children[0]

    @property
    def id_node(self) -> 'Id':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        pass

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Stmts(AstNode):
    def __init__(self, stmts: List[AstNode]):
        super().__init__(name=AST_STMTS, children=stmts)

    @property
    def stmts(self) -> List['AstNode']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        if len(self.stmts) == 0:
            return JVoid()

        # the type of a bunch of statements is the last statement
        last_type = None

        # children are atoms, etc..
        for ast_node in self.stmts:
            last_type = ast_node.static_check(type_env, metadata)

        return last_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        code = []
        for stmt in self.stmts:
            tmp_code, _ = stmt.ir3(context)
            code.extend(tmp_code)
        return code, None

class IfStatement(AstNode):
    def __init__(self, conditional: 'Exp', if_body: 'Stmts', else_body: 'Stmts'):
        super().__init__(name=AST_IF_STATEMENT, children=[conditional,if_body,else_body])

    @property
    def conditional(self) -> 'Exp':
        return self.children[0]

    @property
    def if_body(self) -> 'Stmts':
        return self.children[1]

    @property
    def else_body(self) -> 'Stmts':
        return self.children[2]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # conditional should be bool type
        cond_type = self.conditional.static_check(type_env, metadata)
        if cond_type != JBool():
            raise TypeCheckError(f"expected type {JBool} in 'if' conditional, got {cond_type}")

        # if body and else body should match types
        if_env = type_env.child_env()
        if_type = self.if_body.static_check(if_env, metadata)
        else_env = type_env.child_env()
        else_type = self.else_body.static_check(else_env, metadata)
        if if_type != else_type:
            raise TypeCheckError(f"expected if body type {if_type} to match else body type {else_type}")

        return if_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        if (B) S1 else S2
        B.true = newlabel()
        B.next = newlabel()
        S.code =    B.code ||
                    if (B.label) goto B.true ||
                    S2.code ||
                    gen('goto' B.next) ||
                    B.true ||
                    S1.code ||
                    B.next ||
        """
        b_true = IR3Node.new_label()
        b_next = IR3Node.new_label()
        b_code, b_temp = self.conditional.ir3(context)
        s1_code, _ = self.if_body.ir3(context) # anchor should be None
        s2_code, _ = self.else_body.ir3(context) # anchor should be None

        code = []
        code.extend(b_code)
        code.append(Stmt3IfGoto(b_temp, b_true))
        code.extend(s2_code)
        code.append(Stmt3GotoLabel(b_next))
        code.append(Stmt3LabelSemicolon(b_true))
        code.extend(s1_code)
        code.append(Stmt3LabelSemicolon(b_next))

        return code, None

class WhileStatement(AstNode):
    def __init__(self, conditional: AstNode, while_body: AstNode):
        super().__init__(name=AST_WHILE, children=[conditional,while_body])

    @property
    def conditional(self):
        return self.children[0]

    @property
    def while_body(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # conditional should be bool type
        cond_type = self.conditional.static_check(type_env, metadata)
        if type(cond_type) != JBool:
            raise TypeCheckError(f"expected type {JBool} in 'while' conditional, got {cond_type}")

        # while body is final type
        while_env = type_env.child_env()
        while_type = self.while_body.static_check(while_env, metadata)

        return while_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        while (B) { S1 }
        B.temporary = new temporary()
        B.next = new label()
        B.true = new label()
        B.begin:
            B.code
            if (B.temporary) goto B.true
            goto B.next
        B.true:
            S1.code
            goto B.begin
        B.next:
        """
        b_begin = IR3Node.new_label()
        b_next = IR3Node.new_label()
        b_true = IR3Node.new_label()
        b_code, b_temp = self.conditional.ir3(context)
        s1_code, _ = self.while_body.ir3(context) # anchor should be None

        code = []
        code.append(Stmt3LabelSemicolon(b_begin))
        code.extend(b_code)
        code.append(Stmt3IfGoto(b_temp, b_true))
        code.append(Stmt3GotoLabel(b_next))
        code.append(Stmt3LabelSemicolon(b_true))
        code.extend(s1_code)
        code.append(Stmt3GotoLabel(b_begin))
        code.append(Stmt3LabelSemicolon(b_next))

        return code, None

class Exp(AstNode):
    def __init__(self, actual_exp: AstNode):
        super().__init__(name=AST_EXP, children=[actual_exp])

    @property
    def actual_exp(self):
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        return self.actual_exp.static_check(type_env, metadata)

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        # need use temporary if it exists, pass to BExp/AExp/SExp
        return self.actual_exp.ir3(context)

class ExpList(AstNode):
    def __init__(self, exps: List['Exp']):
        super().__init__(name=AST_EXPLIST, children=exps)

    @property
    def exps(self) -> List['Exp']:
        return self.children

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        # just make sure each expression is checked
        for node in self.exps:
            node.static_check(type_env, metadata)

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()


class Complement(AstNode):
    def __init__(self, bgrd_atom_true_false: AstNode):
        super().__init__(name=AST_NEGATE, children=[bgrd_atom_true_false])

    @property
    def bgrd_atom_true_false(self):
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
        child_type = self.bgrd_atom_true_false.static_check(type_env, metadata)
        if type(child_type) != JBool:
            raise TypeCheckError(f"expected type Bool in complement, got {child_type}")
        return child_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        ! B
        b_temp = new temporary()  // pass to B to use
        B.code
        ! b_temp
        """
        b_code, b_temp = self.bgrd_atom_true_false.ir3(context)

        code = []
        code.extend(b_code)

        # if a temporary is given, assign it to the result of this operation
        temporary = IR3Node.new_temporary()
        exp3 = Exp3Uop(Uop3.complement(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class AndOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_AND, children=[left, right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
        left_type = self.left.static_check(type_env, metadata)
        if type(left_type) != JBool:
            raise TypeCheckError(f"expected type Bool in '&&' LHS, got {left_type}")

        right_type = self.right.static_check(type_env, metadata)
        if type(right_type) != JBool:
            raise TypeCheckError(f"expected type Bool in '&&' RHS, got {right_type}")

        return left_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A && B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp && b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.and_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class OrOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_OR, children=[left,right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
        left_type = self.left.static_check(type_env, metadata)
        if type(left_type) != JBool:
            raise TypeCheckError(f"expected type Bool in '||' LHS, got {left_type}")

        right_type = self.right.static_check(type_env, metadata)
        if type(right_type) != JBool:
            raise TypeCheckError(f"expected type Bool in '||' RHS, got {right_type}")

        return left_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A || B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp || b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.or_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class PlusOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_PLUS, children=[left,right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # left, right types should be Int (Arith) or both String (String)
        left_type = self.left.static_check(type_env, metadata)
        right_type = self.right.static_check(type_env, metadata)

        if type(left_type) in (JNull, JString) and type(right_type) in (JNull, JString):
            return JString()

        if type(left_type) == JInt and type(right_type) == JInt:
            return JInt()

        raise TypeCheckError(f"expected lhs and rhs to be both Int or both String/Null in '+', got {left_type} and {right_type}")

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A + B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp + b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.plus_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JInt())) # JInt since we disallow string concatenation...

        return code, temporary

class MinusOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_MINUS, children=[left,right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JInt':
        # left, right types should be Int
        left_type = self.left.static_check(type_env, metadata)
        if type(left_type) != JInt:
            raise TypeCheckError(f"expected type Int in '-' LHS, got {left_type}")

        right_type = self.right.static_check(type_env, metadata)
        if type(right_type) != JInt:
            raise TypeCheckError(f"expected type Int in '-' RHS, got {right_type}")

        return left_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A - B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp - b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.minus_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JInt()))

        return code, temporary

class MultOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_MULT, children=[left,right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JInt':
        # left, right types should be Int
        left_type = self.left.static_check(type_env, metadata)
        if type(left_type) != JInt:
            raise TypeCheckError(f"expected type Int in '*' LHS, got {left_type}")

        right_type = self.right.static_check(type_env, metadata)
        if type(right_type) != JInt:
            raise TypeCheckError(f"expected type Int in '*' RHS, got {right_type}")

        return left_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A * B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp * b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.mult_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JInt()))

        return code, temporary

class DivOp(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_DIV, children=[left,right])

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JInt':
        # left, right types should be Int
        left_type = self.left.static_check(type_env, metadata)
        if type(left_type) != JInt:
            raise TypeCheckError(f"expected type Int in '/' LHS, got {left_type}")

        right_type = self.right.static_check(type_env, metadata)
        if type(right_type) != JInt:
            raise TypeCheckError(f"expected type Int in '/' RHS, got {right_type}")

        return left_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A / B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp / b_temp
        """
        a_code, a_temp = self.left.ir3(context)
        b_code, b_temp = self.right.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Bop(Idc3(a_temp), Bop3.div_op(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JInt()))

        return code, temporary

class Unegative(AstNode):
    def __init__(self, factor: AstNode):
        super().__init__(name=AST_UNEGATIVE, children=[factor])

    @property
    def factor(self):
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JInt':
        child_type = self.factor.static_check(type_env, metadata)
        if type(child_type) != JInt:
            raise TypeCheckError(f"expected type Int in 'Negation', got {child_type}")
        return child_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        - A
        a_temp = new temp()
        A.code  // pass a_temp
        - a_temp
        """
        a_code, a_temp = self.factor.ir3(context)

        code = []
        code.extend(a_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Uop(Uop3.unegative(), Idc3(a_temp))
        code.append(Stmt3Assignment(temporary, exp3, JInt()))

        return code, temporary

class ClassInstanceCreation(AstNode):
    def __init__(self, cname: 'Cname'):
        super().__init__(name=AST_CLASS_INSTANCE_CREATION, children=[cname])

    @property
    def cname(self) -> 'Cname':
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JClass':
        # class exists in class descriptor
        cid = self.cname.class_name
        if type_env.class_lookup(cid) is None:
            raise TypeCheckError(f"expected cname {cid} to exist when creating instance")
        return JClass(cid)

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        new <Cname3>()
        """
        code = []

        temporary = IR3Node.new_temporary()
        exp3 = Exp3ClassInstanceCreation(self.cname.class_name)
        code.append(Stmt3Assignment(temporary, exp3, JClass(self.cname.class_name)))

        return code, temporary

class FieldAccess(AstNode):
    def __init__(self, left: AstNode, id_node: 'Id'):
        super().__init__(name=AST_FIELD_ACCESS, children=[left, id_node])
        self.type_env = None
        self.left_type: Optional[JLiteType] = None

    @property
    def left(self):
        return self.children[0]

    @property
    def id_node(self) -> 'Id':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, parent_type=None) -> Union['JLiteType', 'MethodSignature']:
        # must be a field of the given class (left) - check class descriptor
        ctype: JClass = self.left.static_check(type_env, None)
        cid = ctype.cname
        class_info = type_env.class_lookup(cid)

        self.type_env = type_env

        if class_info is None:
            raise TypeCheckError(f"accessing non-existent class of type '{cid}'")

        # could be e.a() (msig) or e.a (field_decl)
        nid = self.id_node.id_name
        if parent_type == MethodCall:
            msigs: MethodSignatures = class_info[1]
            if nid not in msigs:
                raise TypeCheckError(f"accessing non-existent method '{nid}' in class of type {cid}")

            self.left_type = msigs[nid][1] # LHS type is return type of method

            # return type is method signature
            return msigs[nid]

        else:
            field_decls: FieldDeclarations = class_info[0]
            if nid not in field_decls:
                raise TypeCheckError(f"accessing non-existent field '{nid}' in class of type {cid}")

            self.left_type = field_decls[nid] # LHS type is type of field being accessed

            # return type is type of the field as in class descriptor
            return field_decls[nid]

    def ir3(self, context: Dict[str, Any]):
        """
        A.b
        a_temp = new temp()
        A.code // get a_temp
        a_temp.b
        """
        a_code, a_temp = self.left.ir3(context)
        code = []
        temporary = IR3Node.new_temporary()

        if type(self.left) == Id and not self.type_env.in_current_local_env(self.left.id_name):
            """
            if the current id is not in the current environment, it must be an instance variable, e.g
            class Person {
                String name;
                Person spouse;
                String writeLetter() {
                    return "Hi, " + spouse.name + "From: " + name;
                }
            }
            """
            this_temp = IR3Node.new_temporary()
            this_exp3 = Exp3FieldAccess("this", self.left.id_name)
            code.append(Stmt3Assignment(this_temp, this_exp3, self.left_type))
            exp3 = Exp3FieldAccess(this_temp, self.id_node.id_name)
            code.append(Stmt3Assignment(temporary, exp3, self.left_type))
        else:
            code.extend(a_code)
            exp3 = Exp3FieldAccess(a_temp, self.id_node.id_name)
            code.append(Stmt3Assignment(temporary, exp3, self.left_type))

        return code, temporary

class MethodCall(AstNode):
    def __init__(self, left: AstNode, explist: 'ExpList'):
        super().__init__(name=AST_METHOD_CALL, children=[left,explist])
        self.left_type = None
        self.cname = None # class that the method belongs to
        self.ret_type = None

    @property
    def left(self):
        return self.children[0]

    @property
    def explist(self) -> 'ExpList':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # if left is id, LocalCall, else GlobalCall
        if type(self.left) == Id:
            # bypass calling static_check on the LHS Id node
            mid = self.left.id_name
            msig: MethodSignature = type_env.msig_lookup(mid)
            if msig is None:
                raise TypeCheckError(f"unexpected id {mid} in 'MethodCall'")

            # hack: retrieve class of this method signature
            cname = type_env.cname_of_msig(msig)
            self.left_type = JClass(cname)
            self.cname = cname

            params, ret_type = msig[0], msig[1]
            self.ret_type = ret_type
            exps: List['Exp'] = self.explist.exps

            # number of args must match number of params
            if len(exps) != len(params):
                raise TypeCheckError(f"{mid}: expected {len(exps)} args, got {len(params)}")

            # each arg must match type of corresponding param
            for i, exp_node in enumerate(self.explist.exps):
                param_name, param_type = params[i][0], params[i][1]
                arg_type = exp_node.static_check(type_env, metadata)
                if param_type != arg_type:
                    raise TypeCheckError(f"{mid} {param_name}: expected {param_type}, got {arg_type}")

            # if all ok, type of local call is the return type
            return ret_type
        else:
            # declare to child type checking that we expect different behaviour
            # NOTE THE EXPLICIT ASKING FOR A METHOD SIGNATURE THROUGH 'METHODCALL'
            msig: MethodSignature = self.left.static_check(type_env, MethodCall)
            if msig is None:
                raise TypeCheckError(f"Left child {type(self.left)} has no method in 'MethodCall'")

            # hack: retrieve class of this method signature
            cname = type_env.cname_of_msig(msig)
            self.left_type = JClass(cname)
            self.cname = cname

            params, ret_type = msig
            self.ret_type = ret_type
            exps: List['Exp'] = self.explist.exps

            # number of args must match number of params
            if len(exps) != len(params):
                raise TypeCheckError(f"GlobalCall: expected {len(params)} args, got {len(exps)}")

            # each arg must match type of corresponding param
            for i, exp_node in enumerate(self.explist.exps):
                param_name, param_type = params[i][0], params[i][1]
                arg_type = exp_node.static_check(type_env, metadata)
                if param_type != arg_type:
                    raise TypeCheckError(f"GlobalCall: {param_name}: expected {param_type}, got {arg_type}")

            return ret_type

    def ir3(self, context: Dict[str, Any]):
        """
        A.a ( ExpList ) OR a ( ExpList ) OR this ( ExpList) OR (new Cname())( ExpList ) OR null ( ExpList )
        ExpList.code    // make a temporary for each exp
        A.code          // get a_temp
        b_temp = A.a
        b_temp ( VList3 ) // vlist3 consists of temporaries from ExpList
        """
        idc3_list = []
        code = []
        temporary = IR3Node.new_temporary()

        for exp_node in self.explist.exps:
            exp_code, exp_temp = exp_node.ir3(context)
            code.extend(exp_code)
            idc3_list.append(Idc3(exp_temp))

        if type(self.left) == Id:
            # local call, no 'this' object, e.g this(1, 2), toString(1, 2)
            mid = self.left.id_name

            # mangle method name
            # cname = context.get("classname")
            # if not cname:
            #     raise RuntimeError("classname should be present in current context")
            mangled_mid = IR3Node.mangle_method_name(self.cname, mid)

            exp3 = Exp3MethodCall(mangled_mid, VList3(idc3_list))
        elif type(self.left) == FieldAccess:
            # global call, need to get a temporary to 'this', e.g a.id(1, 2)
            id_code, id_temp = self.left.left.ir3(context)
            code.extend(id_code)

            # get and mangle the method name with classname, e.g %Class_methodname
            mid = self.left.id_node.id_name
            # cname = self.left_type.cname # for field access, the class name is the type of LHS

            mangled_mid = IR3Node.mangle_method_name(self.cname, mid)

            exp3 = Exp3MethodCall(mangled_mid, VList3([Idc3(id_temp)] + idc3_list))
        else:
            raise RuntimeError("should not be here")

        # differentiate void functions and those that return types
        if type(self.ret_type) == JVoid:
            code.append(Stmt3MethodCall(exp3.id3, exp3.vlist3))
        else:
            code.append(Stmt3Assignment(temporary, exp3, self.ret_type))

        return code, temporary


class ReturnStatement(AstNode):
    def __init__(self, exp: Optional[AstNode]=None):
        super().__init__(name=AST_RETURN_STATEMENT, children=([exp] if exp else []))
        self.exp_type = None

    @property
    def exp(self) -> Optional[AstNode]:
        return self.children[0] if self.children else None

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        if self.exp is None:
            # void return type
            type_env.augment_field("Ret", JVoid())
            self.exp_type = JVoid()
            return JVoid()
        else:
            ret_type = self.exp.static_check(type_env, metadata)
            self.exp_type = ret_type # save for ir3 code generation
            mtd_ret_type = type_env.field_lookup("Ret")

            if ret_type != mtd_ret_type:
                raise TypeCheckError(f"return type {ret_type} does not match method return type {mtd_ret_type}")
            return ret_type

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        return A

        JliteType a_temp; // declare type first
        A.code          // pass a_temp
        return a_temp   // or just return, if no exp
        """
        if not self.exp:
            return [Stmt3Return()], None

        a_code, a_temp = self.exp.ir3(context)
        if a_code:
            # declare a variable only if the return type is complex (not a constant)
            context["return"] = (self.exp_type, a_temp) # for top-level method decl node

        temporary = IR3Node.new_temporary()
        code = []
        code.extend(a_code)
        # a_temp can either be a temporary, or a Const
        if type(a_temp) == Const:
            code.append(Stmt3Assignment(temporary, Idc3(a_temp), self.exp_type))
            code.append(Stmt3Return(temporary))
        else:
            code.append(Stmt3Return(a_temp))

        return code, None


class AssignmentStatement(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        super().__init__(name=AST_ASSIGNMENT_STATEMENT, children=[left, right])
        self.left_type = None

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # if lhs and rhs types match, return void type
        lhs_type = self.left.static_check(type_env, metadata)
        rhs_type = self.right.static_check(type_env, metadata)
        if lhs_type != rhs_type:
            raise TypeCheckError(f"mismatch in lhs {lhs_type} and rhs {rhs_type} in 'AssignmentStatement'")

        self.left_type = lhs_type
        return JVoid()

    def ir3(self, context: Dict[str, Any]):
        """
        A = B
        A.code // get a_temp
        B.code // get b_temp
        a_temp = b_temp
        """
        code = []

        if type(self.left) == FieldAccess:
            # suppose this.a = 1;
            # we don't want t1 = this.a;
            #               t1 = 1;
            a_code, a_temp = self.left.left.ir3(context)
            b_code, b_temp = self.right.ir3(context)
            code.extend(a_code)
            code.extend(b_code)
            field_name: str = self.left.id_node.id_name
            code.append(Stmt3FieldAccessAssignment(a_temp, field_name, Idc3(b_temp)))
        elif type(self.left) == Id and type(self.right) == ClassInstanceCreation:
            code.append(Stmt3Assignment(self.left.id_name, Exp3ClassInstanceCreation(self.right.cname.class_name), self.left_type))
        elif type(self.left) == Id and type(self.right) == Id:
            code.append(Stmt3Assignment(self.left.id_name, Idc3(self.right.id_name), self.left_type))
        else:
            a_code, a_temp = self.left.ir3(context)
            b_code, b_temp = self.right.ir3(context)

            code.extend(a_code)
            code.extend(b_code)
            code.append(Stmt3Assignment(a_temp, Idc3(b_temp), self.left_type))

        return code, None


class Println(AstNode):
    def __init__(self,  exp: AstNode):
        super().__init__(name=AST_PRINTLN, children=[exp])

    @property
    def exp(self):
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # exp should be int or bool or string, if so, return void type
        exp_type = self.exp.static_check(type_env, metadata)
        if type(exp_type) not in (JInt, JBool, JString):
            raise TypeCheckError(f"expected Int/Bool/String for 'println', got {exp_type}")

        return JVoid()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        println A
        A.code // get a_temp
        println a_temp
        """
        a_code, a_temp = self.exp.ir3(context)

        code = []
        code.extend(a_code)
        code.append(Stmt3Println(Idc3(a_temp)))

        return code, None

class Readln(AstNode):
    def __init__(self, id_node: 'Id'):
        super().__init__(name=AST_READLN, children=[id_node])

    @property
    def id_node(self) -> 'Id':
        return self.children[0]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # id should be int or bool or string, if so, return void type
        id_type = self.id_node.static_check(type_env, metadata)
        if type(id_type) not in (JInt, JBool, JString):
            raise TypeCheckError(f"expected Int/Bool/String for 'println', got {id_type}")

        return JVoid()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        readln id
        """
        return [Stmt3Readln(self.id_node.id_name)], None

class Lt(AstNode):
    def __init__(self, lhs: AstNode, rhs: AstNode):
        super().__init__(name=AST_LT, children=[lhs, rhs])

    @property
    def lhs(self) -> AstNode:
        return self.children[0]

    @property
    def rhs(self) -> AstNode:
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Lt (<)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Lt (<)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A < B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp < b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.lt(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class Gt(AstNode):
    def __init__(self, lhs: 'AstNode', rhs: 'AstNode'):
        super().__init__(name=AST_GT, children=[lhs, rhs])

    @property
    def lhs(self) -> 'AstNode':
        return self.children[0]

    @property
    def rhs(self) -> 'AstNode':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Gt (>)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Gt (>)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A > B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp > b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.gt(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class Le(AstNode):
    def __init__(self, lhs: 'AstNode', rhs: 'AstNode'):
        super().__init__(name=AST_LE, children=[lhs, rhs])

    @property
    def lhs(self) -> 'AstNode':
        return self.children[0]

    @property
    def rhs(self) -> 'AstNode':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Le (<=)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Le (<=)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A <= B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp <= b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.ne(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class Ge(AstNode):
    def __init__(self, lhs: 'AstNode', rhs: 'AstNode'):
        super().__init__(name=AST_GE, children=[lhs, rhs])

    @property
    def lhs(self) -> 'AstNode':
        return self.children[0]

    @property
    def rhs(self) -> 'AstNode':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Ge (>=)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Ge (>=)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A >= B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp >= b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.ge(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class Eq(AstNode):
    def __init__(self, lhs: 'AstNode', rhs: 'AstNode'):
        super().__init__(name=AST_EQ, children=[lhs, rhs])

    @property
    def lhs(self) -> 'AstNode':
        return self.children[0]

    @property
    def rhs(self) -> 'AstNode':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Eq (==)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Eq (==)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A == B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp == b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.eq(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary

class Ne(AstNode):
    def __init__(self, lhs: 'AstNode', rhs: 'AstNode'):
        super().__init__(name=AST_NE, children=[lhs, rhs])

    @property
    def lhs(self) -> 'AstNode':
        return self.children[0]

    @property
    def rhs(self) -> 'AstNode':
        return self.children[1]

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        # LHS and RHS should be int, if so, return bool type
        lhs_type = self.lhs.static_check(type_env, metadata)
        if type(lhs_type) != JInt:
            raise TypeCheckError(f"expected lhs type of 'Ne (!=)' to be Int")

        rhs_type = self.rhs.static_check(type_env, metadata)
        if type(rhs_type) != JInt:
            raise TypeCheckError(f"expected rhs type of 'Ne (!=)' to be Int")

        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        A != B
        a_temp = new temp()
        b_temp = new temp()
        A.code // get a_temp
        B.code // get b_temp
        a_temp != b_temp
        """
        a_code, a_temp = self.lhs.ir3(context)
        b_code, b_temp = self.rhs.ir3(context)

        code = []
        code.extend(a_code)
        code.extend(b_code)

        temporary = IR3Node.new_temporary()
        exp3 = Exp3Relop(Idc3(a_temp), RelOp3.ne(), Idc3(b_temp))
        code.append(Stmt3Assignment(temporary, exp3, JBool()))

        return code, temporary


########################### TERMINAL AST NODES ###########################
class Int(AstNode):
    def __init__(self):
        super().__init__(name=AST_INT)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        return JInt()

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Bool(AstNode):
    def __init__(self):
        super().__init__(name=AST_BOOL)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        return JBool()

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class String(AstNode):
    def __init__(self):
        super().__init__(name=AST_STRING)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        return JString()

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Void(AstNode):
    def __init__(self):
        super().__init__(name=AST_VOID)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        return JVoid()

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Cname(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_CNAME, value=tok)

    @property
    def class_name(self) -> str:
        return self.value.value

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JClass':
        return JClass(self.value)

    def ir3(self, context: Dict[str, Any]):
        raise NotImplementedError()

class Id(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_ID, value=tok)

    @property
    def id_name(self) -> str:
        return self.value.value

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None):
        if metadata == MethodCall:
            return type_env.msig_lookup(self.id_name)
        return type_env.field_lookup(self.id_name)

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        """
        # if an id can't be found locally, it must be an instance variable
        local_vars: List[VarDecl] = context["localvars"]
        parameters: List[Fml3] = context["parameters"]
        local = set([x.id_node.id_name for x in local_vars] + [x.id3 for x in parameters])
        if self.id_name in local:
            return [], self.id_name
        return [], Exp3FieldAccess("this", self.id_name)
        """
        return [], self.id_name

class TrueLit(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_TRUE, value=tok)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], Const(True)

class FalseLit(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_FALSE, value=tok)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
        return JBool()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], Const(False)

class IntegerLiteral(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_INT_LITERAL, value=tok)

    @property
    def int_value(self) -> int:
        return self.value.value

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JInt':
        return JInt()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], Const(self.int_value)

class StringLiteral(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_STR_LITERAL, value=tok)

    @property
    def str_value(self) -> str:
        return self.value.value

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JString':
        global string_literals
        string_literals.append(self.str_value)
        return JString()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], Const(self.str_value)

class This(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_THIS, value=tok)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JLiteType':
        return type_env.field_lookup("this")

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], "this"

class Null(AstNode):
    def __init__(self, tok: lex.Token):
        super().__init__(name=AST_NULL, value=tok)

    def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JNull':
        # special null type
        return JNull()

    def ir3(self, context: Dict[str, Any]) -> IR3Result:
        return [], Const("NULL")

######################################################################
######################## CONCRETE SYNTAX TREE ########################
######################################################################

# non-terminals
CST_PROGRAM = "PROGRAM"
CST_PROGRAM1 = "PROGRAM1"
CST_MAINCLASS = "MAINCLASS"
CST_CLASSDECL = "CLASSDECL"
CST_CLASSDECL1 = "CLASSDECL1"
CST_CLASSDECL2 = "CLASSDECL2"
CST_VARDECL = "VARDECL"
CST_MDDECL = "MDDECL"
CST_FMLLIST = "FMLLIST"
CST_FMLLIST1 = "FMLLIST1"
CST_FMLREST = "FMLREST"
CST_TYPE = "TYPE"
CST_MDBODY = "MDBODY"
CST_MDBODY1 = "MDBODY1"
CST_MDBODY2 = "MDBODY2"
CST_STMT = "STMT"
CST_STMT1 = "STMT1"
CST_EXP = "EXP"
CST_BEXP = "BEXP"
CST_BEXP1 = "BEXP1"
CST_CONJ = "CONJ"
CST_CONJ1 = "CONJ1"
CST_REXP = "REXP"
CST_BOP = "BOP"
CST_BGRD = "BGRD"
CST_AEXP = "AEXP"
CST_AEXP1 = "AEXP1"
CST_TERM = "TERM"
CST_TERM1 = "TERM1"
CST_FTR = "FTR"
CST_SEXP = "SEXP"
CST_SEXP1 = "SEXP1"
CST_ATOM = "ATOM"
CST_ATOM1 = "ATOM1"
CST_EXPLIST = "EXPLIST"
CST_EXPLIST1 = "EXPLIST1"
CST_EXPREST = "EXPREST"

# terminals
CST_INT_LITERAL = "INTEGER_LITERAL"
CST_STR_LITERAL = "STRING_LITERAL"
CST_KEYWORD = "KEYWORD"
CST_ID = "ID"

# binary operators
CST_PLUS = "PLUS"
CST_MINUS = "MINUS"
CST_MULT = "MULT"
CST_DIV = "DIV"
CST_ASSIGN = "ASSIGN"
CST_DBL_EQ = "DBL_EQ"
CST_LT = "LT"
CST_GT = "GT"
CST_LE = "LE"
CST_GE = "GE"
CST_NE = "NE"
CST_OR = "OR"
CST_AND = "AND"

# unary operators
CST_EXCLAMATION = "NEGATE"

# keywords
CST_CLASS = "CLASS"
CST_IF = "IF"
CST_ELSE = "ELSE"
CST_WHILE = "WHILE"
CST_READLN = "READLN"
CST_PRINTLN = "PRINTLN"
CST_RETURN = "RETURN"
CST_TRUE = "TRUE"
CST_FALSE = "FALSE"
CST_THIS = "THIS"
CST_NEW = "NEW"
CST_NULL = "NULL"

CST_CNAME_TYPE = "CNAME"
CST_INT_TYPE = "INT"
CST_BOOL_TYPE = "BOOL"
CST_STRING_TYPE = "STRING"
CST_VOID_TYPE = "VOID"
CST_L_CURLY_BRACE = "L_CURLY_BRACE"
CST_R_CURLY_BRACE = "R_CURLY_BRACE"
CST_L_PAREN = "L_PAREN"
CST_R_PAREN = "R_PAREN"
CST_SEMICOLON = "SEMICOLON"
CST_COMMA = "COMMA"
CST_COMMENT = "COMMENT"
CST_DOT = "DOT"
CST_EPSILON = "EPSILON"

class CstNode:
    # class methods are for terminals only
    @classmethod
    def epsilon(cls):
        return CstNode(CST_EPSILON)

    @classmethod
    def empty(cls):
        return CstNode("EMPTY")

    @classmethod
    def class_kw(cls, tok: lex.Token):
        return CstNode(CST_CLASS, value=tok)
    @classmethod
    def if_kw(cls, tok: lex.Token):
        return CstNode(CST_IF, value=tok)
    @classmethod
    def else_kw(cls, tok: lex.Token):
        return CstNode(CST_ELSE, value=tok)
    @classmethod
    def while_kw(cls, tok: lex.Token):
        return CstNode(CST_WHILE, value=tok)
    @classmethod
    def readln_kw(cls, tok: lex.Token):
        return CstNode(CST_READLN, value=tok)
    @classmethod
    def println_kw(cls, tok: lex.Token):
        return CstNode(CST_PRINTLN, value=tok)
    @classmethod
    def return_kw(cls, tok: lex.Token):
        return CstNode(CST_RETURN, value=tok)
    @classmethod
    def true_kw(cls, tok: lex.Token):
        return CstNode(CST_TRUE, value=tok)
    @classmethod
    def false_kw(cls, tok: lex.Token):
        return CstNode(CST_FALSE, value=tok)
    @classmethod
    def this_kw(cls, tok: lex.Token):
        return CstNode(CST_THIS, value=tok)
    @classmethod
    def new_kw(cls, tok: lex.Token):
        return CstNode(CST_NEW, value=tok)
    @classmethod
    def null_kw(cls, tok: lex.Token):
        return CstNode(CST_NULL, value=tok)

    @classmethod
    def cname_type(cls, tok: lex.Token):
        return CstNode(CST_CNAME_TYPE, value=tok)

    @classmethod
    def int_type(cls, tok: lex.Token):
        return CstNode(CST_INT_TYPE, value=tok)

    @classmethod
    def bool_type(cls, tok: lex.Token):
        return CstNode(CST_BOOL_TYPE, value=tok)

    @classmethod
    def str_type(cls, tok: lex.Token):
        return CstNode(CST_STRING_TYPE, value=tok)

    @classmethod
    def void_type(cls, tok: lex.Token):
        return CstNode(CST_VOID_TYPE, value=tok)

    @classmethod
    def l_curly_brace(cls, tok: lex.Token):
        return CstNode(CST_L_CURLY_BRACE, value=tok)

    @classmethod
    def r_curly_brace(cls, tok: lex.Token):
        return CstNode(CST_R_CURLY_BRACE, value=tok)

    @classmethod
    def l_paren(cls, tok: lex.Token):
        return CstNode(CST_L_PAREN, value=tok)

    @classmethod
    def r_paren(cls, tok: lex.Token):
        return CstNode(CST_R_PAREN, value=tok)

    @classmethod
    def semicolon(cls, tok: lex.Token):
        return CstNode(CST_SEMICOLON, value=tok)

    @classmethod
    def comma(cls, tok: lex.Token):
        return CstNode(CST_COMMA, value=tok)

    @classmethod
    def dot(cls, tok: lex.Token):
        return CstNode(CST_DOT, value=tok)

    @classmethod
    def id(cls, tok: lex.Token):
        return CstNode(CST_ID, value=tok)

    @classmethod
    def plus(cls, tok: lex.Token):
        return CstNode(CST_PLUS, value=tok)

    @classmethod
    def minus(cls, tok: lex.Token):
        return CstNode(CST_MINUS, value=tok)

    @classmethod
    def mult(cls, tok: lex.Token):
        return CstNode(CST_MULT, value=tok)

    @classmethod
    def div(cls, tok: lex.Token):
        return CstNode(CST_DIV, value=tok)

    @classmethod
    def assign(cls, tok: lex.Token):
        return CstNode(CST_ASSIGN, value=tok)

    @classmethod
    def dbl_eq(cls, tok: lex.Token):
        return CstNode(CST_DBL_EQ, value=tok)

    @classmethod
    def lt(cls, tok: lex.Token):
        return CstNode(CST_LT, value=tok)

    @classmethod
    def gt(cls, tok: lex.Token):
        return CstNode(CST_GT, value=tok)

    @classmethod
    def le(cls, tok: lex.Token):
        return CstNode(CST_LE, value=tok)

    @classmethod
    def ge(cls, tok: lex.Token):
        return CstNode(CST_GE, value=tok)

    @classmethod
    def ne(cls, tok: lex.Token):
        return CstNode(CST_NE, value=tok)

    @classmethod
    def boolean_or(cls, tok: lex.Token):
        return CstNode(CST_OR, value=tok)

    @classmethod
    def boolean_and(cls, tok: lex.Token):
        return CstNode(CST_AND, value=tok)

    @classmethod
    def exclamation(cls, tok: lex.Token):
        return CstNode(CST_EXCLAMATION, value=tok)

    @classmethod
    def int_literal(cls, tok: lex.Token):
        return CstNode(CST_INT_LITERAL, value=tok)

    @classmethod
    def str_literal(cls, tok: lex.Token):
        return CstNode(CST_STR_LITERAL, value=tok)

    def __init__(self, name: str, value: lex.Token=None, children: List['CstNode']=None, parent: 'CstNode'=None):
        if children is None:
            children = []
        self.name = name
        self.value = value
        self.children = children
        self.parent = parent

    def add_child(self, node: 'CstNode'):
        self.children.append(node)

    def __repr__(self):
        if self.value:
            return f"CstNode({self.name}, {self.value})"
        return f"CstNode({self.name})"

    def __str__(self):
        return pretty_print_cst(self)
        # return print_tree(self, 0)


def print_tree(node: Union[AstNode, CstNode], level: int) -> str:
    if node is None: return ""

    s = " " * level
    if node.value and node.value.value:
        s += f"({node.name}, {node.value.value})"
    else:
        s += f"({node.name})"
    s += "\n"

    for c in node.children:
        s += print_tree(c, level + 4)

    return s

def pretty_print_cst(node: CstNode) -> str:
    def inorder(node: CstNode):
        if not node.children:
            if node.name != CST_EPSILON:
                tokens_inorder.append(node)
            return
        for child in node.children:
            inorder(child)
    def tokens_to_str(tokens: List[CstNode]):
        def translation(token: CstNode) -> str:
            def suffix() -> str:
                return " "
            name = token.name
            if name == CST_INT_LITERAL:
                return str(token.value.value) + suffix()
            elif name == CST_STR_LITERAL:
                return f"\"{token.value.value}\"" + suffix()
            elif name == CST_KEYWORD:
                return token.value.value + suffix()
            elif name == CST_ID:
                return token.value.value + suffix()
            elif name == CST_PLUS:
                return "+" + suffix()
            elif name == CST_MINUS:
                return "-" + suffix()
            elif name == CST_MULT:
                return "*" + suffix()
            elif name == CST_DIV:
                return "/" + suffix()
            elif name == CST_ASSIGN:
                return "=" + suffix()
            elif name == CST_DBL_EQ:
                return "==" + suffix()
            elif name == CST_LT:
                return "<" + suffix()
            elif name == CST_GT:
                return ">" + suffix()
            elif name == CST_LE:
                return "<=" + suffix()
            elif name == CST_GE:
                return ">=" + suffix()
            elif name == CST_NE:
                return "!=" + suffix()
            elif name == CST_OR:
                return "||" + suffix()
            elif name == CST_AND:
                return "&&" + suffix()
            elif name == CST_EXCLAMATION:
                return "!" + suffix()
            elif name == CST_CLASS:
                return "class" + suffix()
            elif name == CST_IF:
                return "if" + suffix()
            elif name == CST_ELSE:
                return "else" + suffix()
            elif name == CST_WHILE:
                return "while" + suffix()
            elif name == CST_READLN:
                return "readln" + suffix()
            elif name == CST_PRINTLN:
                return "println" + suffix()
            elif name == CST_RETURN:
                return "return" + suffix()
            elif name == CST_TRUE:
                return "true" + suffix()
            elif name == CST_FALSE:
                return "false" + suffix()
            elif name == CST_THIS:
                return "this" + suffix()
            elif name == CST_NEW:
                return "new" + suffix()
            elif name == CST_NULL:
                return "null" + suffix()
            elif name == CST_CNAME_TYPE:
                return token.value.value + suffix()
            elif name == CST_INT_TYPE:
                return "Int" + suffix()
            elif name == CST_BOOL_TYPE:
                return "Bool" + suffix()
            elif name == CST_STRING_TYPE:
                return "String" + suffix()
            elif name == CST_VOID_TYPE:
                return "Void" + suffix()
            elif name == CST_L_CURLY_BRACE:
                return "{\n"
            elif name == CST_R_CURLY_BRACE:
                return "}\n"
            elif name == CST_L_PAREN:
                return "(" + suffix()
            elif name == CST_R_PAREN:
                return ")" + suffix()
            elif name == CST_SEMICOLON:
                return ";\n"
            elif name == CST_COMMA:
                return "," + suffix()
            elif name == CST_DOT:
                return "." + suffix()

        return "".join(translation(token) for token in tokens)

    if not node:
        return ""

    tokens_inorder = []
    inorder(node)
    s = tokens_to_str(tokens_inorder)

    return s


#########################################################################
########################### SEMANTIC ANALYSIS ###########################
#########################################################################

##############################################################
########################### ERRORS ###########################
##############################################################

# TODO perhaps add in the position it was parsed/lexed
class StaticCheckError(RuntimeError):
    def __init__(self, desc: str):
        super().__init__(f"StaticCheckError: {desc}")

class TypeCheckError(RuntimeError):
    def __init__(self, desc: str):
        super().__init__(f"TypeCheckError: {desc}")

#######################################################################
########################### STATIC CHECKING ###########################
#######################################################################

AstType = Union[Int, String, Bool, Void, Cname]

class JLiteType:
    def __eq__(self, other):
        return type(self) == type(other)

class JInt(JLiteType):
    def __str__(self):
        return "Int"

    def __repr__(self):
        return "<JInt>"

class JString(JLiteType):
    def __str__(self):
        return "String"

    def __repr__(self):
        return "<JString>"

    def __eq__(self, other):
        # string can be the empty string or empty object
        return type(other) in (JString, JNull)

class JBool(JLiteType):
    def __str__(self):
        return "Bool"

    def __repr__(self):
        return "<JBool>"

class JVoid(JLiteType):
    def __str__(self):
        return "Void"

    def __repr__(self):
        return "<JVoid>"

class JClass(JLiteType):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid

    @property
    def cname(self):
        return self.tid

    def __str__(self):
        return self.tid

    def __repr__(self):
        return f"<JClass: {self.tid}>"

    def __eq__(self, other):
        # either class with same id, or null
        a = type(other) == JClass and self.tid == other.tid
        b = type(other) == JNull
        return a or b

    def __hash__(self):
        return hash(self.tid)

class JNull(JLiteType):
    def __str__(self):
        return "Null"

    def __repr__(self):
        return "<JNull>"

    def __eq__(self, other):
        # null can be the empty string or empty object, but not Void, Int, Bool
        a = type(other) in (JString, JNull)
        b = type(other) == JClass
        return a or b

FieldDeclarations = Dict[str, JLiteType]
MethodSignature = Tuple[List[Tuple[str, JLiteType]], JLiteType]
MethodSignatures = Dict[str, MethodSignature]

class TypeEnvironment:
    @classmethod
    def initialize(cls, mc: MainClass, cds: ClassDecls):
        class_descriptor = ClassDescriptor(mc, cds)
        env = Environment()
        return TypeEnvironment(class_descriptor, env)

    def __init__(self, cd: 'ClassDescriptor'=None, env: 'Environment'=None):
        self.cd = cd
        self.env = env

    # looks up the type of a variable/attribute from local environment
    # if not found in current env, looks at parent environments
    # if doesn't exist, returns None
    def field_lookup(self, var: str) -> Optional[JLiteType]:
        curr_env = self.env
        while curr_env is not None:
            # try to find var in the current env
            typ = curr_env.lookup_field(var)
            if typ is not None:
                return typ
            # otherwise, look at parent environment
            curr_env = curr_env.parent
        return None

    def msig_lookup(self, var: str) -> Optional[MethodSignature]:
        curr_env = self.env
        while curr_env is not None:
            typ = curr_env.lookup_msig(var)
            if typ is not None:
                return typ
            curr_env = curr_env.parent
        return None

    # give a class name, returns (dict of field decls, dict of methd decls)
    def class_lookup(self, cname: str) -> Optional[Tuple[FieldDeclarations, MethodSignatures]]:
        # custom hash using class name
        return self.cd.get_class(cname)

    # returns all classes
    def classes(self) -> List[Tuple[str, FieldDeclarations, MethodSignatures]]:
        return self.cd.get_classes()

    # augments the current environment with var -> type
    def augment_field(self, var: str, typ: JLiteType):
        self.env.augment_field(var, typ)

    def augment_msig(self, var: str, typ: MethodSignature):
        # preprend msgis with _ to differentiate m.a and m.a()
        self.env.augment_msig(var, typ)

    # augments the Environment with given fields
    def augment_fields(self, fields: FieldDeclarations):
        for name, sig in fields.items():
            self.augment_field(name, sig)

    # augments the Environment with given method signatures
    def augment_msigs(self, msigs: MethodSignatures):
        for name, sigs in msigs.items():
            self.augment_msig(name, sigs)

    def child_env(self) -> 'TypeEnvironment':
        return TypeEnvironment(self.cd, self.env.child_env())

    def in_current_local_env(self, name: str) -> bool:
        return self.env.in_current_env(name)

    def cname_of_msig(self, msig: MethodSignature):
        for cname, field_decls, msigs in self.cd.get_classes():
            if msig in msigs.values():
                return cname
        raise RuntimeError()

    def __str__(self):
        ret = ["**** Type Environment ****", str(self.cd), str(self.env), "**** Type Environment ****"]
        return "\n".join(ret)

# all nodes go through here
def node_to_type(node: AstType) -> JLiteType:
    if type(node) == Int:
        return JInt()
    elif type(node) == String:
        return JString()
    elif type(node) == Bool:
        return JBool()
    elif type(node) == Void:
        return JVoid()
    else:
        return JClass(node.class_name)

def unpack_fields(vardecls: List[VarDecl]) -> FieldDeclarations:
    field_mapping = {}
    for vardecl in vardecls:
        name = vardecl.id_node.id_name
        typ = node_to_type(vardecl.type_node)
        field_mapping[name] = typ
    return field_mapping

# returns param types and return type
def unpack_method(mddecl: MdDecl) -> Tuple[str, List[Tuple[str, JLiteType]], JLiteType]:
    mtd_name = mddecl.id_node.id_name
    param_types = []
    ret_type = node_to_type(mddecl.type_node)
    for fml in mddecl.fmllist.fmls:
        param_name = fml.id_node.id_name
        param_type = node_to_type(fml.type_node)
        param_types.append((param_name, param_type))
    return mtd_name, param_types, ret_type

def unpack_methods(mddecls: List[MdDecl]) -> MethodSignatures:
    mtd_mapping = {}
    # unpack method
    for mddecl in mddecls:
        name, param_types, ret_type = unpack_method(mddecl)
        mtd_mapping[name] = (param_types, ret_type)
    return mtd_mapping

def distinct_name_check(main_class: MainClass, class_decls: ClassDecls):
    # [(cname, [(mtdname,
    #               [(field1 name, field1 type), (field2 name, field2 type)...],
    #               [(param1 name, param1 type), (p2 name, p2 type)...]
    #               )]), ...]]
    cnameMethods: List[Tuple[str, List[Tuple[str, JLiteType]], List[Tuple[str, List[Tuple[str, JLiteType]]]]]] = []

    # add main class
    main_cname: str = main_class.cname.class_name
    main_mtdname: str = main_class.mainmd.id_node.id_name
    main_params: List[Tuple[str, JLiteType]] = []
    for fml in main_class.mainmd.fmllist.fmls:
        param_name = fml.id_node.id_name
        param_type = node_to_type(fml.type_node)
        main_params.append((param_name, param_type))
    cnameMethods.append((main_cname, [], [(main_mtdname, main_params)]))

    # add class decls
    for cdecl_node in class_decls.classdecls:
        cname = cdecl_node.cname.class_name

        # get all fields for a class
        vardecls = []
        for vardecl_node in cdecl_node.vardecls.vardecl_list:
            var_name = vardecl_node.id_node.id_name
            var_type = node_to_type(vardecl_node.type_node)
            vardecls.append((var_name, var_type))

        # get all methods for a class
        mthds = []
        for mdecl_node in cdecl_node.mddecls.mddecl_list:
            mtd_name = mdecl_node.id_node.id_name
            mtd_params = []
            # get all param names and types for a method
            for fml_node in mdecl_node.fmllist.fmls:
                param_name = fml_node.id_node.id_name
                param_type = node_to_type(fml_node.type_node)
                mtd_params.append((param_name, param_type))
            mthds.append((mtd_name, mtd_params))

        cnameMethods.append((cname, vardecls, mthds))

    def all_cnames_distinct():
        seen_cnames = set()
        for cname, _, _ in cnameMethods:
            if cname in seen_cnames:
                raise StaticCheckError(f"duplicate class name {cname}")
            seen_cnames.add(cname)

    def all_fields_in_class_distinct():
        for cname, vardecls, _ in cnameMethods:
            seen_fields = set()
            for fieldname, fieldtype in vardecls:
                if fieldname in seen_fields:
                    raise StaticCheckError(f"duplicate field {fieldname} in {cname}")
                seen_fields.add(fieldname)

    def all_mtd_names_in_class_distinct():
        for cname, _, methods in cnameMethods:
            seen_mtd_names = set()
            for mtdname, _ in methods:
                if mtdname in seen_mtd_names:
                    raise StaticCheckError(f"duplicate method {mtdname} in {cname}")
                seen_mtd_names.add(mtdname)

    def all_param_names_in_mtd_distinct():
        for cname, _, methods in cnameMethods:
            for mtdname, mtdparams in methods:
                seen_param_names = set()
                for pname, _ in mtdparams:
                    if pname in seen_param_names:
                        raise StaticCheckError(f"duplicate param {pname} in {cname} {mtdname}")
                    seen_param_names.add(pname)

    # No two classes in a program with same class name
    all_cnames_distinct()

    # No two fields in a class with same name
    all_fields_in_class_distinct()

    # No two methods in a class declaration with same name
    all_mtd_names_in_class_distinct()

    # No two params in a method declaration with same name
    all_param_names_in_mtd_distinct()

class ClassDescriptor:
    def __init__(self, main_class: MainClass, class_decls: ClassDecls):
        # static check done first since we use dicts, which don't allow multiple same keys
        # so we can't construct the class descriptor then check for duplicate names etc
        distinct_name_check(main_class, class_decls)

        self.descriptor = {}    # maps a class name to (field decs, mtd decs)
        self.add_main_class(main_class)
        for other_class in class_decls.classdecls:
            self.add_class(other_class)

    def get_class(self, cname: str) -> Optional[Tuple[FieldDeclarations, MethodSignatures]]:
        # since __hash__ is overriden, need to wrap with class first
        return self.descriptor.get(cname)

    def get_classes(self) -> List[Tuple[str, FieldDeclarations, MethodSignatures]]:
        return [(cname, tup[0], tup[1]) for cname, tup in self.descriptor.items()]

    def add_main_class(self, main_class: MainClass):
        # get class name, field declarations, method declarations
        name = main_class.cname.class_name
        field_mapping = unpack_fields([]) # no fields in main method
        mtd_mapping = unpack_methods([main_class.mainmd])
        self.descriptor[name] = (field_mapping, mtd_mapping)

    def add_class(self, classdecl: ClassDecl):
        name = classdecl.cname.class_name
        field_mapping = unpack_fields(classdecl.vardecls.vardecl_list)
        mtd_mapping = unpack_methods(classdecl.mddecls.mddecl_list)
        self.descriptor[name] = (field_mapping, mtd_mapping)

    def __str__(self):
        ret = ["###### Class Descriptor ######"]
        for cname, tup in self.descriptor.items():
            ret.append(f"{cname}")
            field_map, mtd_map = tup

            ret.append(f"###### fields ######")
            for key, val in field_map.items():
                ret.append(f"{key} -> {val}")

            ret.append(f"###### methods ######")
            for key, val in mtd_map.items():
                ret.append(f"{key} -> {val}")

            ret.append("\n")

        return "\n".join(ret)

class Environment:
    def __init__(self, parent: 'Environment'=None):
        self.field_mapping = {}
        self.msigs_mapping = {}
        self.parent = parent

    def lookup_msig(self, var: str) -> Optional[MethodSignature]:
        return self.msigs_mapping[var] if var in self.msigs_mapping else None

    def lookup_field(self, var: str) -> Optional[JLiteType]:
        return self.field_mapping[var] if var in self.field_mapping else None

    def augment_field(self, name: str, typ: JLiteType):
        self.field_mapping[name] = typ

    def augment_msig(self, name: str, sig: MethodSignature):
        self.msigs_mapping[name] = sig

    def child_env(self) -> 'Environment':
        child = Environment()
        child.parent = self
        return child

    def in_current_env(self, name: str):
        return (name in self.field_mapping) or (name in self.msigs_mapping)

    def __str__(self):
        ret = ["###### Environment ######", f"parent: {self.parent}"]
        for key, val in self.field_mapping.items():
            ret.append(f"{key} -> {val}")
        for key, val in self.msigs_mapping.items():
            ret.append(f"{key} -> {val}")
        return "\n".join(ret)