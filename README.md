# CS4212 JLite Compiler Report

JLite to ARM assembly (v5T) compiler written as an assignment for CS4212 Compiler Design at
the National University of Singapore.

JLite is a toy programming language based off Java. See [JLite Specification](#jlite-specification)
for more details on JLite's syntax.

This report's structure is based off [this report](https://github.com/pyokagan/CS4212-Compiler/blob/master/README.adoc#entry-point)
, but its contents are solely my work.

# Table of Contents
1. [Usage](#usage)
2. [Example Programs](#example-programs)
3. [Project File Structure](#project-file-structure)
4. [JLite Specification](#jlite-specification)
   1. [Entry Point](#entry-point)
   2. [Data Types, Literals and Classes](#data-types-literals-and-classes)
   3. [Operators](#operators)
   4. [Control Flow Statements](#control-flow-statements)
   5. [Reserved keywords](#reserved-keywords)
   6. [Extended BNF Notation](#extended-bnf-notation)
5. [Compiler Internals](#compiler-internals)
   1. [Lexer](#lexer)
   2. [Parser](#parser)
   3. [Static Checking](#static-checking)
   4. [Intermediate Code Generation](#intermediate-code-generation)
   5. [Assembly Code Generation](#assembly-code-generator)
   6. [Code Optimization](#code-optimization)
7. [References](#references)

# Usage

You must have **Python 3.8.10**, the **ARM GCC cross-compiler toolchain** and a 
**Qemu emulator** installed.

Download Python from the [official python website](https://www.python.org/downloads/release/python-3810/).

Download the cross-compiler by run these commands on Ubuntu Linux or Windows Subsystem for Linux (Ubuntu 20.04):
```
sudo apt update
sudo apt upgrade
sudo apt install gcc-10-arm-linux-gnueabi

// to compile a program
arm-linux-gnueabi-gcc-10 hello.c -o hello --static
```

Download the Qemu ARM emulator by running:
```
sudo apt install qemu-user

// to run an ARM binary
qemu-arm <path-to>/hello
```

Clone the repo:
```
git clone https://github.com/KendrickAng/compilers
```

Run the compiler, passing it a file with valid JLite syntax:
```
python3 compile.py program.j
```
A corresponding `program.s` file will be written to disk in the directory the
script is invoked from, containing the generated ARM binary code. 

***There are no optimizations, and hence no option to toggle optimizations!***

Compile and run the resulting ARM binary:
```
// compile
arm-linux-gnueabi-gcc-10 program.s -o program --static

// run
qemu-arm program 
```

# Example Programs

Hello World
```java
class Main {
    Void main() {
        println("Hello World!");
    }
}
```

Hello World - output assembly
```
    .data
L1:
    .asciz "Hello World"

    .text
    .global main
    .type main, %function
main:
    stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
    add fp,sp,#24
    sub sp,fp,#32
    ldr a1,=L1
    bl printf(PLT)

.L1exit:
    mov a4,#0
    mov a1,r3
    sub sp,fp,#24
    ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
```

# Project File Structure
The project root is `project/`. Directories `exercise1/` and `tut1` are irrelevant
and should be ignored.

- project/ - the project root file.
  - images/ - images used in this README. 
  - old/ - legacy documents or files.
  - test/ - directory containing sample inpu/output for all compiler phases.
    - arm/ - sample input and output files for code generation.
    - parsing/ - sample input and output files for AST generation.
    - semantics/ - sample input and output files for IR3 code generation.
  - ast.py - AST and IR3 generation code.
  - backend.py - ARM assembly generation code.
  - compile.py - runner file for ARM assembly code generation.
  - gen.py - runner file for IR3 code generation.
  - ir3.py - cointains data structures for IR3 code representation.
  - lex.py - lexer for the compiler.
  - parse.py - parser for the compiler where AST and IR3 generation logic is.
  - README.md - this file.
  - visualize.py - simple script to visualize an AST with Graphviz.

# JLite Specification
JLite is a toy programming language with basic data types, basic arithmetic
and logical operators, classes and functions.

## Entry Point

The first class in the file must be the "Main" class, which can be called anything
but must contain a single method with signature `Void main()`. It cannot have any fields,
and serves as the main entry point into the program.

## Data Types, Literals and Classes


## Operators

## Control Flow Statements

## Reserved Keywords

## Extended BNF Notation
![JLite Syntax](./images/ebnf.png)

# Compiler Internals
A compiler generally consists of three parts - a front-end, middle-end and
back-end.
- front-end: handles lexing and parsing of tokens into an Abstract Syntax Tree
- middle-end: performs static checking and generates an intermediate code
representation to be used by the back-end
- back-end: converts intermediate code into assembly code

The python `typing` module is extensively used for static code-hinting and a more enjoyable dev experience.

## Lexer
A lexer performs **lexical analysis**, or the conversion of a sequence of characters
representing a program into a sequence of tokens.

### Overview
The lexer reads the entire file as a string, and goes through it like a stream of tokens by maintaining an index
to the current token being lexed.

It is essentially a big while loop that greedily delegates token lexing to other functions for more complex lex
operations.

```python
# converts the input text into a list of Tokens
def lex(self) -> Tuple[List[Token], Optional[Error]]:
    tokens = []

    while self.curr_token is not None:
        token = self.curr_token

        if token == "+": # binop arithmetic
            tokens.append(Token(TT_PLUS, lexed_pos=self.pos.copy()))
            self.advance()
# and so on...
```
### Informative Error Messages
The `LexerPosition` class keeps track of where a token is lexed, increasing the verbosity of error messages during
lexing and parsing.

```python
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
```

Custom `Error` classes are also used with `LexerPosition` to customise error messages.
```python
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
```

### Golang-style Code Structure
The Golang standard library explicitly returns errors instead of using `try-catch` to encourage programmers
to handle them and actively consider errors their program may have, at the cost of verbosity.

For example:
```python
token, err = self.lex_identifier_or_keyword()
if err is not None:
    return tokens, err
tokens.append(token)
```
I adopted this style of coding in `lex.py` and `parse.py`, but dropped this convention later on due to
increased verbosity.

## Parser
A parser performs **syntax analysis**, analyzing tokens from the lexer and constructing a parse tree
representing the program. 

Usually, the parser also outputs an Abstract Syntax Tree (AST), a standard tree format enabling easier static checking
and intermediate code generation.

### Overview
**Recursive Descent with Backtracking** is used to parse tokens, since the grammar is not in the class of
LL(k) grammars.
- Data structures for the AST Nodes are in `ast.py`.
- The Recursive Descent logic is in `parse.py`. 

It should be noted that the program outputs both a Concrete Syntax Tree (CST) and Abstract Syntax Tree (AST).
The CST represents the program parsed as-in according to the [modified grammar](#modified-jlite-grammar),
whereas the AST re-arranges information is a way suitable for bottom-up recursion when further parsing the tree.

An example of Recursive Descent with Backtracking:
```python
def eat_program1(self) -> Tuple[CstNode, Optional[Error], Optional[ClassDecls], Any]:
    # try one path
    cursor = self.save_cursor()
    node, err, astt, _ = self.eat_program11()
    if err is None: return node, err, astt, _
    self.backtrack(cursor)
    
    # if that causes an error, try another path
    cursor = self.save_cursor()
    node, err, astt, _ = self.eat_program12()
    if err is None: return node, err, astt, _
    self.backtrack(cursor)
    
    # backtracking didn't work, return error
    return CstNode.empty(), self.generic_syntax_err(), None, None
```

### Modified JLite Grammar
**Left Factoring** and **Left Recursion Removal** was also done on the original [JLite Syntax](#extended-bnf-notation)
to enable the use of Recursive Descent.

The final modified JLite grammar:
```
Program -> MainClass Program1
Program1 -> ClassDecl Program1  | ''
MainClass -> class cname { void main ( FmlList ) MdBody }
ClassDecl -> class cname { ClassDecl1 ClassDecl2 }
ClassDecl1 -> VarDecl ClassDecl1 | ''
ClassDecl2 -> MdDecl ClassDecl2 | ''
VarDecl -> Type id ;
MdDecl -> Type id ( FmlList ) MdBody
FmlList -> Type id FmlList1 | ''
FmlList1 -> FmlRest FmlList1 | ''
FmlRest -> , Type id
Type -> Int | Bool | String | Void | cname
MdBody -> { MdBody1 Stmt MdBody2 }
MdBody1 -> VarDecl MdBody1 | ''
MdBody2 -> Stmt MdBody2 | ''
Stmt -> if ( Exp ) { Stmt Stmt1 } else { Stmt Stmt1 }
        | while ( Exp ) { Stmt1 }
        | readln ( id ) ;
        | println ( Exp ) ;
        | id = Exp ;
        | Atom = Exp ; 
        | Atom ; 
        | return Exp ; 
        | return ;
Stmt1 -> Stmt Stmt1 | ''
Exp -> BExp | AExp | SExp
BExp -> Conj BExp1
BExp1 -> || Conj BExp1 | ''
Conj -> RExp Conj1
Conj1 -> && RExp Conj1 | ''
RExp -> AExp BOp AExp | BGrd
BOp -> < | > | <= | >= | == | !=
BGrd -> ! BGrd | true | false | Atom
AExp -> Term AExp1
AExp1 -> + Term AExp1 | - Term AExp1 | ''
Term -> Ftr Term1
Term1 -> * Ftr Term1 | / Ftr Term1 | ''
Ftr -> integer_literal | - Ftr | Atom
SExp -> string_literal SExp1 | Atom SExp1
SExp1 -> + SExp SExp1 | ''
Atom -> this Atom1 | id Atom1 | new cname ( ) Atom1 | ( Exp ) Atom1 | null Atom1
Atom1 -> . id Atom1 | ( ExpList ) Atom1 | ( ) Atom1 | ''
ExpList -> Exp ExpList1
ExpList1 -> ExpRest ExpList1 | ''
ExpRest -> , Exp

```

### Informative Error Messages
The AST nodes generated also contain location information from the Lexing phase, allowing the location
of the error to be displayed to the user.

```python
class AstNode:
    def __init__(self, name: str, value: lex.Token=None, children=None): # <-- lex.Token here
        if children is None:
            children = []
        self.name = name
        self.value = value
        self.children = children
```

### Tie-breaking on multiple correct paths
Recursive Descent is a "greedy" algorithm - it looks at the JLite grammar and tries to eat some tokens
corresponding to a prefix of the actual tokens parsed if we continue down that route.

What happens if there are multiple correct paths at a particular point in time (due to the epsilon, the empty string
being a possible token to parse)? I chose to tie-break by picking
the path that went the farthest, or by an arbitarily decided order for the same travel distance. 

```python
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
```

## Static Checking
**Static Checking** is a form of **semantic analysis** performed on the AST output by the parser to ensure
it follows the rules of JLite.
- Type Checking and Distinct-Name Checking are forms of static checking.

1. **Distinct Name Checking** ensures that:
    1. No two classes declared have the same class name.
    2. No two fields in a class have the same name.
    3. No two methods in a class have the same name (method overloading is not implemented).
    4. No two parameters in a method declaration have the same name.

2. **Type Checking** ensures that:
    1. Uses of program constructs conforms to the [Typing Rules](#typing-rules) shown below.

### Overview

The code for type checking consists of three main parts:
1. The classes for the type checking, `TypeEnvironment`, `ClassDescriptor` and `Environment`.
2. The code for initializing the type environment, `TypeEnvironment.initialize(...)`.
3. The code that traverses the AST and type-checks the tree in a bottom-up manner, `AstNode.static_check(...)`.

Sample static code checking for boolean OR `a || b`:
```python
def static_check(self, type_env: 'TypeEnvironment' = None, metadata=None) -> 'JBool':
    left_type = self.left.static_check(type_env, metadata)
    if type(left_type) != JBool:
        raise TypeCheckError(f"expected type Bool in '||' LHS, got {left_type}")

    right_type = self.right.static_check(type_env, metadata)
    if type(right_type) != JBool:
        raise TypeCheckError(f"expected type Bool in '||' RHS, got {right_type}")

    return left_type
```

### Type Environment, Class Descriptor and Environment
These classes are found in `ast.py`, near the end of the file (~line 2433)

They attempt to following the description of the Class Descriptor, Type Environment and Local Environment respectively.

A `TypeEnvironment` consists of a `ClassDescriptor`, containing information about a class, such as its name, field declarations
with their types, and method signatures with their types. 
It also has a local environment `Environment`, which maps variables declared locally to their types.

Of note is `TypeEnvironment.child_env()`, which creates another instance of `TypeEnvironment` with a new `Environment`
pointing to the parent `Environment`, but using the same `ClassDescriptor`. This is to simulate static block scoping.

```Python3
def child_env(self) -> 'TypeEnvironment':
    return TypeEnvironment(self.cd, self.env.child_env())
```

### Handling `null`
Of note: `ast.py` line ~2356 contains classes representing the types `Int`, `String`, `Bool`, `Void`, `Cname`.

I handled `null` by treating it as the null-object or empty-string - `null` has a type of all classes and `String`.
The use of classes allows elegant ways to handle this checking. 
By overriding `__eq__`, we can just use Python `==` to see if two types are equal or not.
```python
JNull() == JClass("Object") # true
JNull() == JString() # true
JNull() == JInt() # false
```

### Typing Rules
The typing rules of JLite are shown below.

![Typing Rules 1](./images/typerules1.png)
![Typing Rules 2](./images/typerules2.png)
![Typing Rules 3](./images/typerules3.png)
![Typing Rules 4](./images/typerules4.png)

## Intermediate Code Generation
After semantic analysis, the annotated AST is converted into a linear representation,
and may be language independent or language specific.
- three-address code (IR3) is language-independent. 

### Overview

The code for IR3 generation consists of two main parts:
1. The `ir3.py` file, which contains data structures correspnoding to the Syntactic Specification of IR3 (in the Appendix)
2. The `ir3()` function of the `AstNode` class, which generates IR3 three-address code bottom-up with the AST.

- All ir3 data structures inherit from the class `IR3Node`. This enables type-checking in Python when used together
  with the `typing` module for a smoother dev experience.
- ir3 data structures have a one-to-one mapping with the IR3 Syntactic Specification from the assignment Appendix.
- `ir3.py` exposes a `run(tree)` method, which takes in an AST augmented with type information and returns the top-level
  ir3 data structure `Program3`.
- `Program3` contains `CData3`, which holds information of a single class, e.g class name, class variable declarations,
  and `CMtd3`, which holds information of a single method from a class.
```python
class Program3(IR3Node):
    def __init__(self, cdata3: List['CData3'], cmtd3: List['CMtd3']):
        self.cdata3 = cdata3
        self.cmtd3 = cmtd3
```
- The IR3 three-address statements are stored in `MdBody3`. Once `ir3()` is called, it will hold a list of data structures,
  each corresponding to a single line of three-address code. It receives this three-address code from its direct children,
  which in turn receives three-address code from its children, and so on until the leaves.
- `AstNode.ir3()` is the method all nodes that inherit from `AstNode` must override.
- The function mostly works in a recursive, bottom-up fashion, with children providing parents their three-address code,
  and the parent uses that three-address code to produce its own.
- The function throws an Exception when and error is met, including a brief description of what went wrong.

Sample code for IR3 generation for boolean OR `a || b`:
```python
def ir3(self, context: Dict[str, Any]) -> IR3Result:
    # generate ir3 for left and right children a and b, bottom-up
    a_code, a_temp = self.left.ir3(context)
    b_code, b_temp = self.right.ir3(context)

    code = []
    code.extend(a_code)
    code.extend(b_code)

    # generate ir3 representing a boolean OR between a and b
    temporary = IR3Node.new_temporary()
    exp3 = Exp3Bop(Idc3(a_temp), Bop3.or_op(), Idc3(b_temp))
    code.append(Stmt3Assignment(temporary, exp3, JBool()))

    return code, temporary
```

### Creating declarations for temporary variables
Three-address code generation may require the creation of temporary variables (e.g `t1`) to store intermediate
values. How will we know how much space a temporary needs?

One way would be to assume all temporaries have a fixed size (e.g 4 bytes). A cleaner way would be to generate
type information together with the IR3 objects used, and variable declarations for each temporary variable.

I used a mix of both, generating new variables for expressions in return statements, and assuming that all
variables have a size of 4 bytes (for strings, 4 bytes store the memory address to its point in .data)

Since JLite requires variable declarations at the start of a function, information needs to be passed
several levels up the AST. I let this information be passed multiple levels up the tree by
using a `context` python dictionary to share information throughout `ir3()` without using global variables.

```java
// original JLite code
Int func() { 
    return 1;
}

// string representation of generated IR3
Int %Functional_func(Functional this) {
    Int _t1;
    _t1 = 1;
    return _t1;
}
```

### Injecting `this` into functions
Converting functions to IR3 entails moving all of them into the global scope; IR3 functions
have no notion of `this`. To support function code involving `this`, a `this` variable
representing the current object has to be manually injected.
```java
Int func() { ... }

Int %Functional_func(Functional this) { ... }
``` 

I did this by passing the class name in the `context` python dict in `ir3()`. When converting
a method to `ir3()`, I inject a variable `this` to the function parameters.

### IR3 Syntax
![IR3 Specification](./images/ir3syntax.png)

## Assembly Code Generation
After IR3 code generation, the compiler backend takes the IR3 and converts it into a form readily executed
by a machine (e.g machine code). In this project, we output ARM assembly that can be cross-compiled to machine code.
- an important task at this stage is **register allocation**, the allocation of variables to processor registers.

### Overview
The backend code lies in the file `backend.py`, consisting of five main stages:

1. Symbol Table generation
2. Basic Block and Flow Graph generation
3. Register allocation for each block in a flow graph
4. Generation of ARM assembly
5. Machine-independent optimization

### Symbol Table generation
During code generation, there are times when we need the retrieve the size of a class (new instance creation), or
the type of a variable.
The symbol table is a data structure meant to answer these queries.

```python
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
        pass

    def add_method(self, cmtd3: CMtd3):
        pass

    def add_string(self, s: str) -> str:
        pass

    def get_string_label(self, s: str) -> str:
        pass

    def has_class(self, name: str):
        pass

    def get_method_info(self, name: str) -> MethodInfo:
        pass

    def get_stack_info(self, method_name: str) -> Dict[str, StackInfo]:
        pass

    def set_stack_info(self, method_name: str, var: str, info: StackInfo):
        pass

    def get_class_info(self, name: str) -> ClassInfo:
        pass

    def get_fp_offset(self, method_name: str, var_name: str) -> int:
        pass

    def get_fp_field_offset(self, method_name: str, var: str, field_name: str) -> int:
        pass

    def get_field_offset(self, method_name: str, var: str, field_name: str):
        pass

    def get_type(self, method_name: str, var_name: str) -> JLiteType:
        pass

```

### Block and Flow Graph Generation
IR3 code generation separates the methods of classes from the classes themselves.
A flow graph is then created from each method, which consists of *basic blocks* connected by edges; each block
represents a maximal sequence of consecutive three-address instructions such that:
1. Control flow can only enter the basic block through the first insturction in the block; there are no jumps to
the middle of the block
2. Control will leave the block without halting or branching, except possibly at the last insturction in the block.

This allows us to assume code runs isolated and linearly in each block, allowing some optimisations.

After generating and partitioning blocks, they are connected into a flow graph, which is then passed through
the code generation algorithm, which generations code block-by-block.

### Register Allocation
To first ensure correctness, a basic register allocation is used - given some instruction of form `a = b + c`,
assume variables are not in any registers, but in stack/heap memory. Generate loads for `b` and `c` from their
appropriate addresses into registers, calculate the end result and generate a store for `a` into its memory
location. Basically, a basic load-store model.

It is assumed that all operations can fit into the registers used by ARM.

Example code for handling `a = <expression>`:
```python
s: Stmt3Assignment
reg, exp_code = exec_exp(s.exp3)
code.extend(exp_code)
code.append(f"str {reg},[fp,#{symbol_table.get_fp_offset(self.method_name, s.id3)}]")
```

### Procedure calls and stack maintenance
Before a function call, registers are assigned from a1, a2, a3, a4, v1, v2, v3, v4, v5, in that order.

```python
FUNCTION_REGS = ["a1", "a2", "a3", "a4", "v1", "v2", "v3", "v4", "v5"]
...
regs_it = iter(FUNCTION_REGS)
if len(node.vlist3.idc3_list) > len(FUNCTION_REGS):
    raise NotImplementedError(f"too many function args: {len(node.vlist3.idc3_list)}, max 11 allowed")

for idc3 in node.vlist3.idc3_list:
    ret.append(gen_load_idc3(next(regs_it), idc3))
```

When setting up a call frame for function call, stack space is first allocated for every
parameter of the function. The values from the registers are then saved to the stack before
the function call executes.

```python
# if the method has any params, store them in from their corresponding register
param_info: NameType
for idx, param_info in enumerate(minfo.params):
    reg = FUNCTION_REGS[idx]
    name = param_info.name
    ret.append(f"str {reg},[fp,#{symbol_table.get_fp_offset(method_name, name)}]")
```

### Escaping strings placed in .data
Strings in the program must appear as-in in .data, meaning that special characters must be escaped
before being printed to file.

Python includes *raw strings*, which tell Python not to recognise special characters. By
default, `repr()` returns a raw string when used on strings. Since it wraps the strings in single quotes,
these have to be removed too.

```python
print(repr("\n")[1:-1]) # gives \n
```

### Handling large integers
How are statements like `a = 5000 + 5000` handled? 
While `mov a1,#constant` is an easy way to load a constant integer into registers, ARM v5t only accepts a range
of 0-255. 

To handle larger constant integers with more than 8 bits, I use a pseudo-instruction `ldr reg,=constant`.

```python
def gen_load_const_int(reg: str, i: int):
    if 0 <= i <= 255:
        return f"mov {reg},#{i}"
    # https://developer.arm.com/documentation/den0042/a/Unified-Assembly-Language-Instructions/Instruction-set-basics/Constant-and-immediate-values
    # https://stackoverflow.com/questions/10261300/invalid-constant-after-fixup
    # arm pseudo instruction to handle values greater than 8 bits
    return f"ldr {reg},=#{i}"
```

### Correct program flow
ARM Assembly code is executed from top to bottom. Once the main function executes finish,
the program should exit. As an implementation detail, I therefore added a branch to the function's 
exit label and ensured that `main`'s exit label was at the end of the assembly code.

```
.data
IntegerFormat:
.asciz "%i"
L1:
.asciz "Hello World!"

.text
.global main
.type main, %function

main:
stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
add fp,sp,#24
sub sp,fp,#32
str a1,[fp,#-28]
ldr a1,=L1
bl printf(PLT)
b mainexit <--- here

mainexit: <--- here
sub sp,fp,#24
ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
```

## Machine-Independent Optimization
At any point in time during code generation, machine-independent optimization algorithms can be run to improve
the runtime of the final program.

There are two kinds of optimizations:
1. Local optimizations, which happen within each basic block
2. Glboal optmization, which looks at how information flwos among the basic blocks of a program.

For example, if an unconditional branch is followed by another unconditional branch, the second statement
will definitely be unreachable and can be removed without affect program correctness.

Currently, no optimizations are performed.

# References
Almost all concepts applied here come from the "Dragon Book", Compilers: Principles, Techniques, and Tools, 2nd 
Edition.

CS4212 - Compiler Design was taught by Prof. Wong Weng Fai in AY2021/2022, Semester 1, who also designed this
project.

I do not know if this project was inspired by other sources.