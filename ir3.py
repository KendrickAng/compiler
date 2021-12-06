"""
Class definitions for the intermediate code (IR3) tree
"""
from typing import List, Set, Dict, Tuple, Optional, Callable, Optional, Any, Union

# starting method
def run(tree) -> 'Program3':
    return tree.ir3({})

def format_label(num: int):
    return f"Label{str(num)}"

######################################################################
########################### IR3 TREE NODES ###########################
######################################################################
class IR3Node:
    label_id = 1
    temporary_id = 1

    @classmethod
    def new_label(cls) -> str:
        ret = format_label(IR3Node.label_id)
        IR3Node.label_id += 1
        return ret

    @classmethod
    def new_temporary(cls) -> str:
        ret = str(IR3Node.temporary_id)
        IR3Node.temporary_id += 1
        return f"_t{ret}"

    @classmethod
    def mangle_method_name(cls, cname: str, mname: str) -> str:
        return f"_{cname}_{mname}"

    @classmethod
    # Given some statement i: x = y + z, extract these vars (x, y, z)
    def extract_vars(cls, ir3: 'IR3Node') -> Tuple[List, List]:
        def readln(x: Stmt3Readln):
            return [x.id3_str], []
        def println(x: Stmt3Println):
            return [], [x.idc3_node.var_name]
        def assignment(x: Stmt3Assignment):
            return [x.id3_name], x.exp3_names
        def field_access_assignment(x: Stmt3FieldAccessAssignment):
            return [x.lhs_left_id], [x.rhs_id] if x.rhs_id else []
        def return_stmt(x: Stmt3Return):
            return [], [x.ret_id] if x.ret_id else []
        def method_call(x: Stmt3MethodCall):
            return [], [y.var_name for y in x.vlist3_node.idc3_list if y.var_name is not None]
        d = {
            Stmt3Readln: readln,
            Stmt3Println: println,
            Stmt3Assignment: assignment,
            Stmt3FieldAccessAssignment: field_access_assignment,
            Stmt3Return: return_stmt,
            Stmt3MethodCall: method_call,
        }
        if type(ir3) in d:
            fn = d[type(ir3)]
            return fn(ir3)
        return [], []

class Program3(IR3Node):
    def __init__(self, cdata3: List['CData3'], cmtd3: List['CMtd3']):
        self.cdata3 = cdata3
        self.cmtd3 = cmtd3

    @property
    def cdata3_list(self) -> List['CData3']:
        return self.cdata3

    @property
    def cmtd3_list(self) -> List['CMtd3']:
        return self.cmtd3

    def __str__(self):
        strings = ["\n======= CData3 =======\n"]
        for cd3 in self.cdata3: strings.append(str(cd3))
        strings.append("\n======= CMtd3 =======\n")
        for cm3 in self.cmtd3: strings.append(str(cm3))
        return "\n".join(strings)

class VarDecl3(IR3Node):
    def __init__(self, type3, id3: str):
        self.type3 = type3 # JliteType
        self.id3 = id3

    def __str__(self):
        return f"{self.type3} {self.id3};"

class CData3(IR3Node):
    def __init__(self, cname: str, vardecls: List[VarDecl3]):
        self.cname = cname
        self.vardecls = vardecls

    def __str__(self):
        strings = [f"class {self.cname} {{"]
        for vardecl in self.vardecls:
            strings.append(f"\t{str(vardecl)}")
        strings.append("}")
        return "\n".join(strings)

class CMtd3(IR3Node):
    def __init__(self, type3, id3: str, fmllist3: 'FmlList3', mdbody3: 'MdBody3'):
        self.type3 = type3 # JLiteType
        self.id3 = id3
        self.fmllist3 = fmllist3
        self.mdbody3 = mdbody3

    def stmts_list(self) -> List['IR3Node']:
        return self.mdbody3.stmt3

    def __str__(self):
        strings = [f"{self.type3} {self.id3} {str(self.fmllist3)} {{"]
        strings.append(str(self.mdbody3))
        strings.append("}")
        return "\n".join(strings)

class FmlList3(IR3Node):
    def __init__(self, cname3: str, fml3_list: List['Fml3']):
        self.cname3 = cname3
        self.fml3_list = fml3_list

    def __str__(self):
        fmls = ", ".join(str(x) for x in self.fml3_list)
        return "(" + f"{fmls}" + ")"

class Fml3(IR3Node):
    def __init__(self, type3, id3: str):
        self.type3 = type3
        self.id3 = id3

    def __str__(self):
        return f"{self.type3} {self.id3}"

class MdBody3(IR3Node):
    def __init__(self, vardecl3: List[VarDecl3], stmt3: List['IR3Node']):
        self.vardecl3 = vardecl3
        self.stmt3 = stmt3

    def __str__(self):
        vardecls = ["\t"+str(x) for x in self.vardecl3]
        stmts = ["\t"+str(x) for x in self.stmt3]
        return "\n".join(vardecls + stmts)

class Stmt3LabelSemicolon(IR3Node):
    def __init__(self, label: str):
        self.label = label

    @property
    def label_name(self) -> str:
        return self.label

    @label_name.setter
    def label_name(self, val):
        self.label = val

    def __str__(self):
        return f"{self.label}:"

class Stmt3IfGoto(IR3Node):
    def __init__(self, if_temporary: str, goto_label: str):
        self.if_temporary = if_temporary
        self.goto_label = goto_label

    @property
    def label(self) -> str:
        return self.goto_label

    @label.setter
    def label(self, val):
        self.goto_label = val

    @property
    def temporary(self) -> str:
        return self.if_temporary

    def __str__(self):
        return f"if ({self.if_temporary}) goto {self.goto_label};"

class Stmt3GotoLabel(IR3Node):
    def __init__(self, label: str):
        self.target_label = label

    @property
    def label(self) -> str:
        return self.target_label

    @label.setter
    def label(self, val):
        self.target_label = val

    def __str__(self):
        return f"goto {self.label};"

class Stmt3Readln(IR3Node):
    def __init__(self, id3: str):
        self.id3 = id3

    @property
    def id3_str(self) -> str:
        return self.id3

    def __str__(self):
        return f"readln {self.id3};"

class Stmt3Println(IR3Node):
    def __init__(self, idc3: 'Idc3'):
        self.idc3 = idc3

    @property
    def idc3_node(self) -> 'Idc3':
        return self.idc3

    def __str__(self):
        return f"println {str(self.idc3)};"

class Stmt3Assignment(IR3Node):
    def __init__(self, id3: str, exp3: IR3Node, jliteType):
        self.id3 = id3
        self.exp3 = exp3 # should be Exp3...
        self.jLiteType = jliteType

    @property
    def id3_name(self) -> str:
        return self.id3

    @property
    def lhs_type(self):
        return self.jLiteType

    @property
    # returns the IDs used in each expression, e.g a > b returns [a, b]
    def exp3_names(self) -> List[str]:
        return self.exp3.names # property of all Exp3<..> nodes

    def __str__(self):
        return f"{self.id3} = {str(self.exp3)};"

class Stmt3FieldAccessAssignment(IR3Node):
    def __init__(self, id3_left: str, id3_right: str, idc3: 'Idc3'):
        self.id3_left = id3_left
        self.id3_right = id3_right
        self.idc3 = idc3

    @property
    def lhs_left_id(self) -> str:
        return self.id3_left

    @property
    def lhs_right_id(self) -> str:
        return self.id3_right

    @property
    def rhs_id(self) -> Optional[str]:
        return self.idc3.var_name

    def __str__(self):
        return f"{self.id3_left}.{self.id3_right} = {str(self.idc3)}"

class Stmt3MethodCall(IR3Node):
    def __init__(self, id3: str, vlist3: 'VList3'):
        self.exp3 = Exp3MethodCall(id3, vlist3) # basically the same thing
        self.id3 = id3
        self.vlist3 = vlist3

    @property
    def vlist3_node(self) -> 'VList3':
        return self.vlist3

    def __str__(self):
        return f"{self.id3}{str(self.vlist3)};"

class Stmt3Return(IR3Node):
    def __init__(self, id3: Optional[str]=None):
        self.id3 = id3

    @property
    def ret_id(self) -> Optional[str]:
        return self.id3

    def __str__(self):
        return f"return {self.id3};" if self.id3 else "return;"

class Exp3Relop(IR3Node):
    def __init__(self, left_idc3: 'Idc3', relop3: 'RelOp3', right_idc3: 'Idc3'):
        self.left_idc3 = left_idc3
        self.relop3 = relop3
        self.right_idc3 = right_idc3

    @property
    def names(self) -> List[str]:
        ret = []
        if self.left_idc3.var_name: ret.append(self.left_idc3.var_name)
        if self.right_idc3.var_name: ret.append(self.right_idc3.var_name)
        return ret

    def __str__(self):
        return f"{str(self.left_idc3)} {str(self.relop3)} {str(self.right_idc3)}"

class Exp3Bop(IR3Node):
    def __init__(self, l_idc3: 'Idc3', bop3: 'Bop3', r_idc3: 'Idc3'):
        self.l_idc3 = l_idc3
        self.bop3 = bop3
        self.r_idc3 = r_idc3

    @property
    def names(self) -> List[str]:
        ret = []
        if self.l_idc3.var_name: ret.append(self.l_idc3.var_name)
        if self.r_idc3.var_name: ret.append(self.r_idc3.var_name)
        return ret

    def __str__(self):
        return f"{str(self.l_idc3)} {str(self.bop3)} {str(self.r_idc3)}"

class Exp3Uop(IR3Node):
    def __init__(self, uop3: 'Uop3', idc3: 'Idc3'):
        self.uop3 = uop3
        self.idc3 = idc3

    @property
    def names(self) -> List[str]:
        return [self.idc3.var_name] if self.idc3.var_name else []

    def __str__(self):
        return f"{str(self.uop3)}{str(self.idc3)}"

class Exp3FieldAccess(IR3Node):
    def __init__(self, l_id3: str, r_id3: str):
        self.l_id3 = l_id3
        self.r_id3 = r_id3

    @property
    def names(self) -> List[str]:
        # a.b - ONLY a is used
        return [self.l_id3]

    def __str__(self):
        return f"{self.l_id3}.{self.r_id3}"

class Exp3MethodCall(IR3Node):
    def __init__(self, id3: str, vlist3: 'VList3'):
        self.id3 = id3
        self.vlist3 = vlist3

    @property
    def names(self) -> List[str]:
        # all function call vars are considered "used"
        return [x.var_name for x in self.vlist3.idc3_list if x.var_name is not None]

    def __str__(self):
        return f"{self.id3}{str(self.vlist3)}"

class Exp3ClassInstanceCreation(IR3Node):
    def __init__(self, cname3: str):
        self.cname3 = cname3

    @property
    def names(self) -> List[str]:
        # no variables are used in class instance creation
        return []

    def __str__(self):
        return f"new {self.cname3}()"

class RelOp3(IR3Node):
    @classmethod
    def lt(cls): return RelOp3("<")

    @classmethod
    def gt(cls): return RelOp3(">")

    @classmethod
    def le(cls): return RelOp3("<=")

    @classmethod
    def ge(cls): return RelOp3(">=")

    @classmethod
    def eq(cls): return RelOp3("==")

    @classmethod
    def ne(cls): return RelOp3("!=")

    def __init__(self, op: str):
        self.op = op

    def is_lt(self):
        return self.op == "<"

    def is_gt(self):
        return self.op == ">"

    def is_le(self):
        return self.op == "<="

    def is_ge(self):
        return self.op == ">="

    def is_eq(self):
        return self.op == "=="

    def is_ne(self):
        return self.op == "!="

    def __str__(self):
        return self.op

class Bop3(IR3Node):
    @classmethod
    def and_op(cls): return Bop3("&&")

    @classmethod
    def or_op(cls): return Bop3("||")

    @classmethod
    def mult_op(cls): return Bop3("*")

    @classmethod
    def div_op(cls): return Bop3("/")

    @classmethod
    def plus_op(cls): return Bop3("+")

    @classmethod
    def minus_op(cls): return Bop3("-")

    def __init__(self, op: str):
        self.op = op

    def is_and(self):
        return self.op == "&&"

    def is_or(self):
        return self.op == "||"

    def is_mult(self):
        return self.op == "*"

    def is_div(self):
        return self.op == "/"

    def is_plus(self):
        return self.op == "+"

    def is_minus(self):
        return self.op == "-"

    def __str__(self):
        return self.op

class Uop3(IR3Node):
    @classmethod
    def complement(cls): return Uop3("!")

    @classmethod
    def unegative(cls): return Uop3("-")

    def __init__(self, op: str):
        self.op = op

    def is_complement(self):
        return self.op == "!"

    def is_unegative(self):
        return self.op == "-"

    def __str__(self):
        return self.op

class VList3(IR3Node):
    def __init__(self, idc3_list: List['Idc3']):
        self.idc3_list = idc3_list

    def __str__(self):
        return "(" + ", ".join([str(x) for x in self.idc3_list]) + ")"

class VRest3(IR3Node):
    pass

class Idc3(IR3Node):
    def __init__(self, id3_or_const):
        self.id3_or_const = id3_or_const

    # returns True if underlying type is a variable name or temporary
    def is_var(self) -> bool:
        return type(self.id3_or_const) == str

    # returns true if underlying type is an integer
    def is_int(self) -> bool:
        return type(self.id3_or_const) == Const and type(self.id3_or_const.value) == int

    def is_bool(self) -> bool:
        return type(self.id3_or_const) == Const and type(self.id3_or_const.value) == bool

    def is_string(self) -> bool:
        return type(self.id3_or_const) == Const and type(self.id3_or_const.value) == str

    # returns None if const, otherwise returns the variable name
    @property
    def var_name(self) -> Optional[str]:
        if type(self.id3_or_const) == str:
            return self.id3_or_const
        elif type(self.id3_or_const) == Const:
            return None
        raise RuntimeError(f"Idc3 must only have Id3 or Const, got {type(self.id3_or_const)}")

    # returns the actual underlying value of the Idc3 (if int or string), None otherwise
    @property
    def var_value(self) -> Optional[Union[str, int, bool]]:
        if type(self.id3_or_const) == Const:
            self.id3_or_const: Const
            return self.id3_or_const.value
        return None

    def __str__(self):
        return str(self.id3_or_const)

class Const(IR3Node):
    def __init__(self, value: Union[bool, int, str]):
        self.value = value

    def __str__(self):
        if self.value == "NULL":
            return "NULL"
        elif type(self.value) == str:
            return f"\"{self.value}\""
        else:
            return str(self.value)

IR3Result = Tuple[List[IR3Node], Optional[Union[str, Const]]]