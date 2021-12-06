"""
Parses IR3 code into ARM assembly code
"""
from ast import *
from collections import defaultdict, namedtuple

"""Dependencies
SymbolTable
    ClassInfo
        NameType
    MethodInfo
        StackInfo
        NameType
"""
# order in which function variable are stored
FUNCTION_REGS = ["a1", "a2", "a3", "a4", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
TEMPORARY_SIZE_BYTES = 4
ClassInfo = namedtuple("ClassInfo", ["name", "fields", "size_bytes"])
MethodInfo = namedtuple("MethodInfo", ["name", "params", "local_vars", "stack_info"])
StackInfo = namedtuple("StackInfo", ["name", "type", "size", "fp_offset"])
NameType = namedtuple("NameType", ["name", "type", "size"])
class SymbolTable:
    LABEL_NUMBER = 1
    INT_FORMAT_LABEL_NAME = "IntegerFormat"
    INT_FORMAT_STRING = ".asciz \"%i\""

    def __init__(self):
        self.classes = defaultdict(ClassInfo)
        self.methods = defaultdict(MethodInfo)
        self.strings = {} # string to label

    def add_class(self, cdata3: CData3):
        name = cdata3.cname
        fields = []
        size_bytes = 0
        for v in cdata3.vardecls:
            size_bytes += type_to_bytes(v.type3)
            fields.append(NameType(v.id3, v.type3, type_to_bytes(v.type3)))
        self.classes[name] = ClassInfo(name, fields, size_bytes)

    def add_method(self, cmtd3: CMtd3):
        name = cmtd3.id3
        params = [NameType(fml.id3, fml.type3, type_to_bytes(fml.type3)) for fml in cmtd3.fmllist3.fml3_list]
        local_vars = [NameType(v.id3, v.type3, type_to_bytes(v.type3)) for v in cmtd3.mdbody3.vardecl3]
        stack_info: Dict[str, StackInfo] = defaultdict(lambda: StackInfo(None, None, None, None))
        self.methods[name] = MethodInfo(name, params, local_vars, stack_info)

    def add_string(self, s: str) -> str:
        label = f"L{self.LABEL_NUMBER}"
        self.strings[s] = label
        self.LABEL_NUMBER += 1
        return label

    def get_string_label(self, s: str) -> str:
        return self.strings[s]

    def has_class(self, name: str):
        return name in self.classes

    def get_method_info(self, name: str) -> MethodInfo:
        return self.methods[name]

    def get_stack_info(self, method_name: str) -> Dict[str, StackInfo]:
        return self.get_method_info(method_name).stack_info

    def set_stack_info(self, method_name: str, var: str, info: StackInfo):
        self.get_method_info(method_name).stack_info[var] = info

    def get_class_info(self, name: str) -> ClassInfo:
        return self.classes[name]

    def get_fp_offset(self, method_name: str, var_name: str) -> int:
        stack_info = self.get_stack_info(method_name)
        return stack_info[var_name].fp_offset * -1 # descending stack

    def get_fp_field_offset(self, method_name: str, var: str, field_name: str) -> int:
        stack_info = self.get_stack_info(method_name)
        offset = stack_info[var].fp_offset * -1
        t = stack_info[var].type
        if type(t) != JClass:
            raise AssertionError()
        t: JClass
        class_info = self.get_class_info(t.cname)
        field: NameType
        for field in class_info.fields:
            if field.name == field_name:
                return offset
            offset -= field.size
        raise RuntimeError(f"get_fp_field_offset: {method_name} {var} {field_name} not found")

    def get_field_offset(self, method_name: str, var: str, field_name: str):
        # get underlying type of given var, then calculate its offset
        t = self.get_stack_info(method_name)[var].type
        if type(t) != JClass:
            raise AssertionError()
        t: JClass
        class_info = self.get_class_info(t.cname)
        offset = 0
        field: NameType
        for field in class_info.fields:
            if field.name == field_name:
                return offset
            offset -= field.size
        raise RuntimeError(f"get_field_offset: {method_name} {var} {field_name} not found")

    def get_type(self, method_name: str, var_name: str) -> JLiteType:
        stack_info = self.get_stack_info(method_name)
        return stack_info[var_name].type

symbol_table = SymbolTable()

def type_to_bytes(type_obj: JLiteType):
    global symbol_table
    if type(type_obj) in (JInt, JBool, JString, JClass):
        # JString - memory location to place in .data
        # JClass - memory location to heap memory
        return 4
    raise RuntimeError(f"{type_obj} has no supported size")

class Arm:
    def __init__(self, ir: Program3):
        self.ir = ir
        self.asm = []

    # returns a list of assembly code
    def run(self):
        # fill up symbol table with CData3
        self.fill_symbol_table()
        # form flow graph
        self.asm = self.construct_asm()
        self.postprocess()
        return self.asm

    def postprocess(self):
        main_mangled = IR3Node.mangle_method_name("Main", "main")
        processed = []
        for arm_code in self.asm:
            processed.append(arm_code.replace(main_mangled, "main"))
        self.asm = processed

    def construct_asm(self):
        global symbol_table
        # construct flow graph for each individual function
        ret = []
        cmtd3_list: List[CMtd3] = self.ir.cmtd3_list

        # construct data portion
        ret.append(".data")
        ret.append(f"{SymbolTable.INT_FORMAT_LABEL_NAME}:")
        ret.append(SymbolTable.INT_FORMAT_STRING)
        for string in get_string_literals(): # get_string_literals from ast.py
            label = symbol_table.add_string(string)
            ret.append(f"{label}:")
            ret.append(f".asciz \"{repr(string)[1:-1]}\"") # convert to raw string

        ret.append("") # leave a space
        ret.append(".text")
        ret.append(f".global main")
        ret.append(f".type main, %function")

        # construct text portion
        main_exit = [] # place main method's exit at the very end
        for i, cmtd3 in enumerate(cmtd3_list):
            ret.append("") # leave a line
            method_name = cmtd3.id3
            curr_offset = 0 # offset from frame pointer, always points to next FREE space

            # add offsets for stack registers
            registers = ["_fp", "_lr", "_v1", "_v2", "_v3", "_v4", "_v5"]
            for reg in registers:
                symbol_table.set_stack_info(method_name, reg, StackInfo(reg, None, 4, curr_offset))
                curr_offset += 4

            minfo: MethodInfo = symbol_table.get_method_info(method_name)

            # get space needed + generate stack space for params in the method
            param_info: NameType
            for param_info in minfo.params:
                name, typ, size = param_info.name, param_info.type, param_info.size
                info = StackInfo(name, typ, size, curr_offset)
                symbol_table.set_stack_info(method_name, name, info)
                #print(f"{name} allocated offset {curr_offset} to {curr_offset + size}")
                curr_offset += type_to_bytes(typ)

            # get space needed + generate stack space for local variables in the method
            local_var: NameType
            seen = set()
            for local_var in minfo.local_vars:
                seen.add(local_var.name)
                # initialize stack information for this local var
                name, typ, size = local_var.name, local_var.type, type_to_bytes(local_var.type)
                info = StackInfo(name, typ, size, curr_offset)
                symbol_table.set_stack_info(method_name, name, info)
                #print(f"{name} allocated offset {curr_offset} to {curr_offset + size}")
                curr_offset += type_to_bytes(typ)

            # get space needed + generate stack space for temporaries in the method
            temporaries = []
            for stmt3 in cmtd3.mdbody3.stmt3:
                stmt3: Stmt3Assignment # PEP 526
                if type(stmt3) == Stmt3Assignment and stmt3.id3_name not in seen:
                    name = stmt3.id3_name
                    temporaries.append(name)
                    seen.add(name)

                    # assume temporaries (t1, t2...) all have size 4 bytes
                    size = type_to_bytes(stmt3.lhs_type)
                    info = StackInfo(name, stmt3.lhs_type, size, curr_offset)
                    #print(f"{name} allocated offset {curr_offset} to {curr_offset + size}")
                    symbol_table.set_stack_info(method_name, name, info)
                    curr_offset += TEMPORARY_SIZE_BYTES

            # add function label and save all registers
            entry_label = f"{method_name}:"
            ret.append(entry_label)
            ret.append("stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}")
            ret.append("add fp,sp,#24")
            ret.append(f"sub sp,fp,#{curr_offset}")

            # if the method has any params, store them in from their corresponding register
            param_info: NameType
            for idx, param_info in enumerate(minfo.params):
                reg = FUNCTION_REGS[idx]
                name = param_info.name
                ret.append(f"str {reg},[fp,#{symbol_table.get_fp_offset(method_name, name)}]")

            # store all required variables
            exit_label_name = f"{method_name}exit"
            exit_label = f"{exit_label_name}:"
            flow_graph = self.construct_flow_graph(cmtd3, exit_label_name)
            #print(flow_graph)
            asm_list = self.construct_asm_from_graph(flow_graph)
            ret.extend(asm_list)
            ret.append(f"b {exit_label_name}") # once function is done, jump to exit

            # save the method method's exit for last
            tmp = main_exit if i == 0 else ret
            tmp.append("") # leave a line
            tmp.append(exit_label)
            tmp.append("sub sp,fp,#24")
            tmp.append("ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}")

        ret.extend(main_exit)
        ret.append("") # newline at end of file
        return ret

    @staticmethod
    def construct_flow_graph(cmtd3: CMtd3, exit_label: str) -> 'FlowGraph':
        method_name: str = cmtd3.id3

        # flatten into a list three-address instructions
        stmts: List[IR3Node] = cmtd3.stmts_list()
        Metadata = namedtuple("Metadata", "is_leader")
        stmts_info = {}

        # for mapping labels to their indexes
        label_to_idx = {}
        for i, stmt in enumerate(stmts):
            if type(stmt) == Stmt3LabelSemicolon:
                stmt: Stmt3LabelSemicolon
                label_to_idx[stmt.label_name] = i

        # 1. find leaders
        is_next_leader = False
        for i, stmt in enumerate(stmts):
            if i not in stmts_info:
                stmts_info[i] = Metadata(False)

            # first three-address instruction in ir3 is a leader
            if i == 0:
                stmts_info[i] = Metadata(True)

            # any instruction that immediately follows a conditional or unconditional jump is a leader
            if is_next_leader:
                stmts_info[i] = Metadata(True)

            # any instruction that's the target of a conditional or unconditional jump is a leader
            if type(stmt) in (Stmt3IfGoto, Stmt3GotoLabel):
                target_idx = label_to_idx[stmt.label]
                stmts_info[target_idx] = Metadata(True)
                is_next_leader = True

        # 2. make blocks
        graph = FlowGraph(method_name, exit_label)
        idx_to_block = {}
        prev_bid = graph.ENTRY_BID
        curr_bid = 0
        curr_block = Block(method_name, curr_bid, exit_label)
        i = 0
        while i < len(stmts):

            # do-while, iterate until the next block, or the end
            while True:
                curr_block.add_stmt(stmts[i])
                idx_to_block[i] = curr_bid
                i += 1
                if i >= len(stmts) or stmts_info[i].is_leader:
                    break

            graph.add_block(curr_bid, curr_block)
            graph.connect_blocks(prev_bid, curr_bid)

            if i >= len(stmts):
                # connect current block to the EXIT block
                graph.connect_blocks(curr_bid, graph.EXIT_BID)
                break
            else:
                # reset the current block
                prev_bid = curr_bid
                curr_bid += 1
                curr_block = Block(method_name, curr_bid, exit_label)

        # 3. connect blocks and update jump labels
        for i, stmt in enumerate(stmts):
            if type(stmt) in (Stmt3IfGoto, Stmt3GotoLabel):
                # retrieve the block number of the jump
                jump_idx = label_to_idx[stmt.label]
                target_bid = idx_to_block[jump_idx]
                # replace jumps to isntructions/labels by jumps to basic blocks
                label_stmt: Stmt3LabelSemicolon = stmts[jump_idx]
                graph.connect_blocks(idx_to_block[i], target_bid)

                # update labels
                new_label = format_label(target_bid)
                label_stmt.label_name = new_label
                if type(stmt) == Stmt3IfGoto:
                    stmt: Stmt3IfGoto
                    stmt.goto_label = new_label
                elif type(stmt) == Stmt3GotoLabel:
                    stmt: Stmt3GotoLabel
                    stmt.label = new_label

        return graph

    @staticmethod
    def construct_asm_from_graph(g: 'FlowGraph'):
        # generate liveness information for each block
        # TODO try this out once we get the main algorithm working
        # g.add_liveness_info()

        # simple code generation with getReg
        code = g.generate_simple_code()
        return code

    def fill_symbol_table(self):
        global symbol_table
        # add classes
        for cdata3 in self.ir.cdata3_list:
            symbol_table.add_class(cdata3)

        # add methods
        for cmtd3 in self.ir.cmtd3_list:
            symbol_table.add_method(cmtd3)


class FlowGraph:
    ENTRY_BID = -1
    EXIT_BID = 999999

    def __init__(self, method_name: str, exit_label: str):
        self.method_name = method_name
        self.exit_label = exit_label
        self.adj_list: Dict[int, List[int]] = {
            FlowGraph.ENTRY_BID: [],
            FlowGraph.EXIT_BID: []
        }
        self.bid_to_block: Dict[int, Block] = {
            FlowGraph.ENTRY_BID: Block(method_name, FlowGraph.ENTRY_BID, exit_label),
            FlowGraph.EXIT_BID: Block(method_name, FlowGraph.EXIT_BID, exit_label)
        }

    def add_block(self, bid: int, block: 'Block'):
        self.adj_list[bid] = []
        self.bid_to_block[bid] = block

    def get_block(self, bid: int):
        return self.bid_to_block[bid]

    def connect_blocks(self, a: int, b: int):
        self.adj_list[a].append(b)

    def connect_entry_to(self, bid: int):
        self.connect_blocks(FlowGraph.ENTRY_BID, bid)

    def connect_to_exit(self, bid: int):
        self.connect_blocks(bid, FlowGraph.EXIT_BID)

    def add_liveness_info(self):
        for bid in self.get_bids_ascending():
            self.bid_to_block[bid].add_liveness_info()

    def generate_simple_code(self):
        # generate code in order
        code = []
        for bid in self.get_bids_ascending():
            block_code = self.get_block(bid).generate_code()
            code.extend(block_code)
        return code

    def get_bids_ascending(self):
        # don't do anything to entry and exit blocks
        return sorted(filter(lambda x: x not in (self.ENTRY_BID, self.EXIT_BID), self.bid_to_block.keys()))

    def __str__(self):
        strs = []
        block_strs = []
        for block_id in self.get_bids_ascending():
            neighbours = ",".join(map(str, self.adj_list[block_id]))
            strs.append(f"{block_id}: {neighbours}")
            block_strs.append(f"--- Block {block_id}: ---\n{str(self.bid_to_block[block_id])}")
        combined = ["---------------"] + strs + block_strs + ["---------------"]
        return "\n".join(combined)
"""
Represents a flow graph block.
"""
NextUseLiveness = namedtuple("NextUseLiveness", ["next_use", "is_live"])
class Block:
    def __init__(self, method_name: str, bid: int, exit_label: str):
        self.method_name = method_name
        self.bid = bid
        self.exit_label = exit_label
        self.stmts = []
        # index to liveness info NextUseLiveness
        self.liveness_info: Dict[int, Dict[str, NextUseLiveness]] = defaultdict(dict)

    def add_stmt(self, stmt: IR3Node):
        self.stmts.append(stmt)

    # generates liveness info (next-use info) for a single block
    def add_liveness_info(self):
        d = defaultdict(lambda: NextUseLiveness(None, False))
        for i, stmt in enumerate(reversed(self.stmts)):
            lhs, rhs = IR3Node.extract_vars(stmt)

            # assign to statement i: x = y + z the info current found in symbol table about next use
            # and liveness of x, y and z
            for name in lhs:
                info_tuple = d[name]
                self.liveness_info[i][name] = info_tuple
            for name in rhs:
                info_tuple = d[name]
                self.liveness_info[i][name] = info_tuple

            # in the symbol table, set x to "not live" and "no next use"
            for name in lhs:
                d[name].is_live = False
                d[name].next_use = None

            # in the symbol table, set y, z to "live" and next use of y, z to i
            for name in rhs:
                d[name].is_live = True
                d[name].next_use = i

    def generate_code(self):
        global symbol_table

        def gen_load_idc3(reg: str, node: Idc3):
            if node.is_var():
                return gen_load_from_mem(reg, node.var_name)
            elif node.is_int():
                return gen_load_const_int(reg, node.var_value)
            elif node.is_string():
                return gen_load_const_str(reg, node.var_value)
            elif node.is_bool():
                return gen_load_const_bool(reg, node.var_value)
            else:
                raise NotImplementedError()

        def gen_load_from_mem(reg: str, var: str):
            return f"ldr {reg},{gen_fp_offset(var)}"

        def gen_load_const_bool(reg: str, b: bool):
            return f"mov {reg},#{1 if b else 0}"

        def gen_load_const_str(reg: str, s: str):
            return f"ldr {reg},={symbol_table.get_string_label(s)}"

        def gen_load_const_int(reg: str, i: int):
            if 0 <= i <= 255:
                return f"mov {reg},#{i}"
            # https://developer.arm.com/documentation/den0042/a/Unified-Assembly-Language-Instructions/Instruction-set-basics/Constant-and-immediate-values
            # https://stackoverflow.com/questions/10261300/invalid-constant-after-fixup
            # arm pseudo instruction to handle values greater than 12 bits
            return f"ldr {reg},=#{i}"

        def gen_fp_offset(var: str):
            return f"[fp,#{symbol_table.get_fp_offset(self.method_name, var)}]"

        def exec_stmt(s: IR3Node):
            typ = type(s)
            ret = []
            if typ == Stmt3LabelSemicolon:
                s: Stmt3LabelSemicolon # PEP 526
                ret.append("") # leave a space
                ret.append(f"{s.label_name}:")
            elif typ == Stmt3IfGoto:
                """if t1 goto label
                ldr a1,[fp,#offset_t1]
                cmp a1,#1 ; if left-right = 0, set Z set to 1, else 0 
                beq label ; if Z set, branch to label
                """
                s: Stmt3IfGoto
                ret.append(gen_load_from_mem("a1", s.temporary))
                ret.append(f"cmp a1,#1")
                ret.append(f"beq {s.label}")
            elif typ == Stmt3GotoLabel:
                """goto label
                b label
                """
                s: Stmt3GotoLabel
                ret.append(f"b {s.label}")
            elif typ == Stmt3Readln:
                """readln(x) - where x is restricted to be an integer
                ldr a1,=INT_FORMAT_STRING_LABEL ; load format string for int
                add a2,fp,#offset_x ; store results directly into stack memory
                bl scanf(PLT)
                """
                s: Stmt3Readln
                if type(symbol_table.get_type(self.method_name, s.id3_str)) != JInt:
                    raise NotImplementedError("readln only supports integers")
                ret.append(f"ldr a1,={SymbolTable.INT_FORMAT_LABEL_NAME}")
                ret.append(f"add a2,fp,#{symbol_table.get_fp_offset(self.method_name, s.id3_str)}")
                ret.append(f"bl scanf(PLT)")
            elif typ == Stmt3Println:
                """println(x) - where x is integer or string
                if JInt:
                    ldr a1,=label 
                    mov a2,#number
                    bl printf(PLT) 
                if JString:
                    ldr a1,=label 
                    bl printf(PLT)
                if temporary:
                    ldr a1,[fp, #offset]
                    bl printf(PLT)
                """
                s: Stmt3Println
                if s.idc3_node.is_int():
                    ret.append(f"ldr a1,={SymbolTable.INT_FORMAT_LABEL_NAME}")
                    ret.append(gen_load_const_int("a2", s.idc3_node.var_value))
                elif s.idc3_node.is_string():
                    ret.append(gen_load_const_str("a1", s.idc3_node.var_value))
                elif s.idc3_node.is_var():
                    typ = symbol_table.get_type(self.method_name, s.idc3_node.var_name)
                    if type(typ) in (JInt, JBool):
                        ret.append(f"ldr a1,={SymbolTable.INT_FORMAT_LABEL_NAME}")
                        ret.append(gen_load_from_mem("a2", s.idc3_node.var_name))
                    elif type(typ) == JString:
                        ret.append(gen_load_from_mem("a1", s.idc3_node.var_name))
                    else:
                        raise NotImplementedError()
                else:
                    raise NotImplementedError()
                ret.append("bl printf(PLT)")
            elif typ == Stmt3Assignment:
                """a = exp3
                ... do stuff for exp3
                str reg,[fp,#offset_a]
                """
                s: Stmt3Assignment
                reg, exp_code = exec_exp(s.exp3)
                ret.extend(exp_code)
                ret.append(f"str {reg},[fp,#{symbol_table.get_fp_offset(self.method_name, s.id3)}]")
            elif typ == Stmt3FieldAccessAssignment:
                """a.b = c
                ldr a1,[fp,#offset_c] ; load in c
                ldr a2,[fp,#offset_a] ; load in mem address of a
                str a1,[a2,#offset_b] ; store c in mem address(a + offset) 
                """
                s: Stmt3FieldAccessAssignment
                a = s.id3_left
                b = s.id3_right
                ret.append(gen_load_idc3("a1", s.idc3))
                ret.append(f"ldr a2,[fp,#{symbol_table.get_fp_offset(self.method_name, a)}]")
                ret.append(f"str a1,[a2,#{symbol_table.get_field_offset(self.method_name, a, b)}]")
            elif typ == Stmt3MethodCall:
                """id(1, "hi", c)
                
                """
                s: Stmt3MethodCall
                _, exp_code = exec_exp(s.exp3)
                ret.extend(exp_code)
            elif typ == Stmt3Return:
                """return [x] - where x may not exist
                ldr a1,[fp,#offset]
                b exit_label
                """
                s: Stmt3Return
                if s.ret_id:
                    ret.append(gen_load_from_mem("a1", s.ret_id))
                ret.append(f"b {self.exit_label}")
            else:
                raise NotImplementedError()
            return ret

        def exec_exp(node: IR3Node):
            global symbol_table
            typ = type(node)
            ret = []
            if typ == Exp3Relop:
                """a relop b
                ldr a1,[fp,#offset_a]
                ldr a2,[fp,#offset_b]
                cmp a1,a2
                mov{cond} a1,#1
                mov{cond} a1,#0
                """
                node: Exp3Relop
                ret.append(gen_load_idc3("a1", node.left_idc3))
                ret.append(gen_load_idc3("a2", node.right_idc3))
                ret.append(f"cmp a1,a2")
                if node.relop3.is_lt():
                    ret.append("movlt a1,#1")
                    ret.append("movge a1,#0")
                elif node.relop3.is_gt():
                    ret.append("movgt a1,#1")
                    ret.append("movle a1,#0")
                elif node.relop3.is_le():
                    ret.append("movle a1,#1")
                    ret.append("movgt a1,#0")
                elif node.relop3.is_ge():
                    ret.append("movge a1,#1")
                    ret.append("movlt a1,#0")
                elif node.relop3.is_eq():
                    ret.append("moveq a1,#1")
                    ret.append("movne a1,#0")
                elif node.relop3.is_ne():
                    ret.append("movne a1,#1")
                    ret.append("moveq a1,#0")
                return "a1", ret
            elif typ == Exp3Bop:
                """a bop b
                ldr a2,[fp,#offset_a]
                ldr a3,[fp,#offset_b]
                bop a1,a2,a3
                """
                node: Exp3Bop
                a = "a2"
                b = "a3"
                ret.append(gen_load_idc3(a, node.l_idc3))
                ret.append(gen_load_idc3(b, node.r_idc3))
                if node.bop3.is_and():
                    ret.append(f"and a1,{a},{b}")
                elif node.bop3.is_or():
                    ret.append(f"orr a1,{a},{b}")
                elif node.bop3.is_mult():
                    ret.append(f"mul a1,{a},{b}")
                elif node.bop3.is_div():
                    raise NotImplementedError("division is not supported")
                elif node.bop3.is_plus():
                    ret.append(f"add a1,{a},{b}")
                elif node.bop3.is_minus():
                    ret.append(f"sub a1,{a},{b}")
                return "a1", ret
            elif typ == Exp3Uop:
                """uop a
                ldr a1,[fp,#offset_a]
                
                """
                node: Exp3Uop
                ret.append(gen_load_idc3("a2", node.idc3))
                if node.uop3.is_unegative():
                    ret.append(gen_load_const_int("a3", -1))
                    ret.append(f"mul a1,a2,a3")
                elif node.uop3.is_complement():
                    ret.append(f"eor a1,a2,#1")
                return "a1", ret
            elif typ == Exp3FieldAccess:
                """a.b
                ldr a1,[fp,#offset_a] ; get heap address
                ldr a1,[a1,#field_b_offset] ; get value from heap
                """
                node: Exp3FieldAccess
                a = node.l_id3
                b = node.r_id3
                ret.append(gen_load_from_mem("a1", a))
                ret.append(f"ldr a1,[a1,#{symbol_table.get_field_offset(self.method_name, a, b)}]")
                return "a1", ret
            elif typ == Exp3MethodCall:
                """f(a,b,c...)
                ldr a1,[fp,#offset_a]
                ldr a2,[fp,#offset_b]
                ...
                
                """
                # here we assume <= 11 function args, one for each register
                node: Exp3MethodCall
                regs_it = iter(FUNCTION_REGS)
                if len(node.vlist3.idc3_list) > len(FUNCTION_REGS):
                    raise NotImplementedError(f"too many function args: {len(node.vlist3.idc3_list)}, max 11 allowed")

                for idc3 in node.vlist3.idc3_list:
                    ret.append(gen_load_idc3(next(regs_it), idc3))

                ret.append(f"bl {node.id3}")
                # function call result is always in a1, by convention
                return "a1", ret
            elif typ == Exp3ClassInstanceCreation:
                """a = new Cname()
                mov a1,#<object size>
                bl malloc(PLT)
                """
                node: Exp3ClassInstanceCreation
                ret.append(f"mov a1,#{symbol_table.get_class_info(node.cname3).size_bytes}")
                ret.append(f"bl malloc(PLT)")
                # malloc returns address of allocated memory
                return "a1", ret
            elif typ == Idc3:
                """a = b
                
                """
                node: Idc3
                ret.append(gen_load_idc3("a1", node))
                return "a1", ret

        # leave a line before beginning
        # code = ["", f"{self.method_name}_{self.bid}:"]
        code = []

        # go through each statement and convert IR3 to assembly code
        for i, stmt in enumerate(self.stmts):
            if i in self.liveness_info:
                # TODO get correctness right first, then use a greedy approach
                raise NotImplementedError()
            else:
                # naive code generation
                code.extend(exec_stmt(stmt))

        return code

    def __str__(self):
        strs = []
        strs.extend([str(s) for s in self.stmts])
        return "\n".join(strs)

