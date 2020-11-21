import sys

# Jihye Woo

# AST Nodes

class Node():
    def __init__(self):
        self.parent = None

    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count

class Assignment(Node):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.lvalue.parent = self
        self.rvalue.parent = self

    def eval(self):
        pass

class Negation(Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
        self.child.parent = self

    def eval(self):
        # try:
        return not self.child.eval()
        # except:
        #     semantic_error_handle()

class Conjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        # try:
        return self.left.eval() and self.right.eval()
        # except:
        #     semantic_error_handle()


class Disjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        # try:
        result = self.left.eval() or self.right.eval()
        return result
        # except:
        #     semantic_error_handle()


class BoolOperation(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.right = right
        self.op = op
        # self.left.parent = self
        # self.right.parent = self

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if self.op == 'in' and isinstance(right, (list, tuple, str)):
            return left in right

        if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or \
                (isinstance(left, (str)) and isinstance(right, (str))):
            if self.op == '<>':
                return left != right
            elif self.op == '<=':
                return left <= right
            elif self.op == '<':
                return left < right
            elif self.op == '==':
                return left == right
            elif self.op =='>=':
                return left == right
            elif self.op == '>':
                return left > right

        # semantic_error_handle()

class AST_True(Node):
    def __init__(self):
        super().__init__()
        self.value = True

    def eval(self):
        return self.value


class AST_False(Node):
    def __init__(self):
        super().__init__()
        self.value = False

    def eval(self):
        return self.value

class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def eval(self):
        # if self.name in names:
        return names[self.name]


class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self):
        names[self.name] = self.value.eval()

class AssignList(Node):
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

    def eval(self):
        targetList = names[self.name]
        targetList[self.index.eval()] = self.value.eval()
        # except:
        #     semantic_error_handle()

class GetByListIndex(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self):
        # try:
        targetList = names[self.name]
        return targetList[self.index.eval()]
        # except:
        #     semantic_error_handle()

class Number(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self):
        return self.value

class Operation(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if self.op == '**':
                return left ** right
            elif self.op == '+':
                return left + right
            elif self.op == '-':
                return left - right
            elif self.op == '*':
                return left * right
            elif self.op == '/':
                return left / right
            elif self.op == 'div':
                return left // right
            elif self.op == 'mod':
                return left % right
        elif isinstance(left, (str)) and isinstance(right, (str)):
            if self.op == '+':
                return left + right
        elif isinstance(left, (list)) and isinstance(right, (list)):
            if self.op == '+':
                return left + right
        elif isinstance(left, (int)) and isinstance(right, (list)):
            if self.op == '::':
                return [left] + right
        # semantic_error_handle()


class StringNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value[1:-1]

    def eval(self):
        return self.value

class List(Node):
    def __init__(self, values):
        super().__init__()
        self.value = values

    def eval(self):
        result = []
        for element in self.value:
            result.append(element.eval())
        return result

class ListIndex(Node):
    def __init__(self, list, index):
        super().__init__()
        self.list = list
        self.index = index
    def eval(self):
        list = self.list.eval()
        index = self.index.eval()
        # try:
        if(isinstance(index, (int))):
            return list[index]
        # except:
        #     semantic_error_handle()

class Tuple(Node):
    def __init__(self, values):
        super().__init__()
        self.value = values

    def eval(self):
        result = []
        for element in self.value:
            result.append(element.eval())
        return tuple(result)

class TupleIndex(Node):
    def __init__(self, index, tuple):
        super().__init__()
        self.index = index
        self.tuple = tuple

    def eval(self):
        # try:
        tuple = self.tuple.eval()
        index = self.index
        if (isinstance(index, (int))):
            return tuple[index]
        # except:
        #     semantic_error_handle()

class Print(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        target = self.value.eval()
        print(target)

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self):
        # try:
        for statement in self.statements:
            statement.eval()
        # except:
        #     semantic_error_handle()


class While(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def eval(self):
        while self.condition.eval():
            self.block.eval()

class If(Node):
    def __init__(self, condition, ifblock):
        self.condition = condition
        self.ifblock = ifblock


    def eval(self):
        if self.condition.eval():
            return self.ifblock.eval()
        else:
            pass

class IfElse(Node):
    def __init__(self, condition, ifblock, elseblock):
        self.condition = condition
        self.ifblock = ifblock
        self.elseblock = elseblock

    def eval(self):
        if self.condition.eval():
            return self.ifblock.eval()
        else:
            return self.elseblock.eval()

class Execute(Node):
    def __init__(self, blocks):
        self.blocks = blocks
    def eval(self):
        for block in self.blocks:
            block.eval()

class FunDef(Node):
    def __init__(self, var, parameters, block, expr):
        self.var = var
        self.parameters = parameters
        self.block = block
        self.expr = expr

    def eval(self):
        names[self.var] = {"parameters" : self.parameters,
                           "block" : self.block,
                           "returnVal" : self.expr}

class FunCall(Node):
    def __init__(self, var, arguments):
        self.var = var
        self.arguments = arguments

    def eval(self):
        definedFun = names[self.var]
        paras = definedFun['parameters']

        # local variable setting
        arguments = self.arguments.eval()
        for index in range(len(paras)):
            names[paras[index]] = arguments[index]

        # execute function
        definedFun['block'].eval()
        return_value = definedFun['returnVal'].eval()
        # reset local variable
        map(names.pop, paras)

        return return_value

# Tokens

tokens = ('EQUALS',
          'NEGATION','CONJUNCTION', 'DISJUNCTION',
          'LPAREN' ,'RPAREN', 'LLIST', 'RLIST',
          'TRUE', 'FALSE',
          'VARIABLE', 'NUMBER','STRING', 'TUPLEINDEXING',
          'COMPARISON',
          'PLUS' ,'MINUS' ,'TIMES' ,'DIVIDE',
          'EXPONENT', 'INTDIV', 'MODULUS',
          'MEMBER', 'CONS', 'COMMA',
          'PRINT', 'SEMI',
          'LCURLY', 'RCURLY',
          'WHILE', 'IF', 'ELSE', 'FUN'
          )

t_EQUALS                = r'='
t_NEGATION              = r'not'
t_CONJUNCTION           = r'andalso'
t_DISJUNCTION           = r'orelse'
t_LPAREN                = r'\('
t_RPAREN                = r'\)'
t_TRUE                  = r'True'
t_FALSE                 = r'False'
t_COMPARISON            = r'(<> | <= | < | == | >= | >)'
t_PLUS                  = r'\+'
t_MINUS                 = r'-'
t_TIMES                 = r'\*'
t_DIVIDE                = r'/'
t_EXPONENT              = r'\*\*'
t_INTDIV                = r'div'
t_MODULUS               = r'mod'
t_STRING                = r'(\"[^\"\r\n]*\")|(\'[^\'\r\n]*\')'
t_MEMBER                = r'in'
t_CONS                  = r'::'
t_LLIST                 = r'\['
t_RLIST                 = r'\]'
t_COMMA                 = r','
t_TUPLEINDEXING         = r'\#'
t_PRINT                 = r'print'
t_SEMI                  = r';'
t_LCURLY                = r'{'
t_RCURLY                = r'}'
t_WHILE                 = r'while'
t_IF                    = r'if'
t_ELSE                  = r'else'
t_ignore                = " \t\n"
t_FUN                   = "fun"

def t_VARIABLE(t):
    r'(?!\b(div|mod|True|False|orelse|andalso|in|not|print|while|if|else|fun)\b)[a-zA-Z][a-zA-Z0-9_]*'
    return t


def t_NUMBER(t):
    r'(\d*(\d\.|\.\d)\d*((e|E)-?\d+)?|\d+)'
    # try:
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t
    # except:
    #     semantic_error_handle()

# Count newlines
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += t.value.count("\n")

# Report lexing errors
def t_error(t):
    # print("Illegal Character '%s', at %d, %d" %
    #       (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)

# Build lexer
import ply.lex as lex
lexer = lex.lex(debug = True)

def tokenize(inp):
    lexer.input(inp)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Parsing rules

names = {}
precedence = (
              # ('left','EQUALS'),
              ('left', 'DISJUNCTION', 'CONJUNCTION'),
              ('left', 'NEGATION'),
              ('left', 'COMPARISON'),
              ('left', 'CONS'),
              ('left', 'MEMBER'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE', 'INTDIV', 'MODULUS'),
              ('right','EXPONENT'),
              ('left', 'LLIST', 'RLIST'),
              ('left', 'LPAREN' ,'RPAREN')
              )



def p_program_body(p):
    '''program : blocks'''
    p[0] = Execute(p[1])

def p_program_body2(p):
    '''blocks : blocks block'''
    p[0] = p[1] + [p[2]]

def p_functionDef_fundef(p):
    '''functionDef : FUN VARIABLE parameters EQUALS block expr SEMI'''
    p[0] = FunDef(p[2], p[3], p[5], p[6])

def p_functionCall_funcall(p):
    '''functionCall : VARIABLE tuple '''
    p[0] = FunCall(p[1], p[2])

def p_parameter_para(p):
    '''parameters : LPAREN para_list RPAREN'''
    p[0] = p[2]

def p_parameter_para2(p):
    '''parameters : LPAREN RPAREN'''
    p[0] = []

def p_para_list_para(p):
    '''para_list : VARIABLE COMMA para_list'''
    p[0] = [p[1]] + p[3]

def p_para_list_para2(p):
    '''para_list : VARIABLE'''
    p[0] = [p[1]]

def p_expr_funcall(p):
    '''expr : functionCall'''
    p[0] = p[1]

def p_program_body3(p):
    '''blocks : block
            | functionDef '''
    p[0] = [p[1]]

def p_block_block(p):
    '''block : LCURLY statements RCURLY'''
    p[0] = Block(p[2])

def p_block_nullBlock(p):
    '''block : LCURLY RCURLY'''
    p[0] = Block([])

def p_statements_statements(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_statements2(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_while(p):
    '''statement : WHILE paren block'''
    p[0] = While(p[2], p[3])

def p_condition_ifCondition(p):
    '''condition : IF paren block'''
    p[0] = If(p[2], p[3])

def p_condition_ifElseCondition(p):
    '''condition : IF paren block ELSE block'''
    p[0] = IfElse(p[2], p[3], p[5])

def p_statement_expr(p):
    '''statement : expr SEMI
                | condition'''
    p[0] = p[1]

def p_expr_assign(p):
    '''expr : VARIABLE EQUALS expr'''
    p[0] = Assign(p[1], p[3])

def p_expr_assign2(p):
    'expr : VARIABLE LLIST expr RLIST EQUALS expr'
    p[0] = AssignList(p[1], p[3], p[6])

def p_expr_assign3(p):
    'expr : VARIABLE LLIST expr RLIST'
    p[0] = GetByListIndex(p[1],p[3])

def p_expr_print(p):
    'expr : PRINT paren'
    p[0] = Print(p[2])

def p_expr_negation(p):
    'expr : NEGATION expr'
    p[0] = Negation(p[2])

def p_expr_conjunction(p):
    'expr : expr CONJUNCTION expr'
    p[0] = Conjunction(p[1], p[3])

def p_expr_disjunction(p):
    'expr : expr DISJUNCTION expr'
    p[0] = Disjunction(p[1], p[3])

def p_expr_true(p):
    'expr : TRUE'
    p[0] = AST_True()

def p_expr_false(p):
    'expr : FALSE'
    p[0] = AST_False()

def p_expr_comparison(p):
    'expr : expr COMPARISON expr'
    p[0] = BoolOperation(p[1], p[2], p[3])

def p_expr_memeber(p):
    'expr : expr MEMBER expr'
    p[0] = BoolOperation(p[1], p[2], p[3])
    print(p[0])

def p_expr_operation(p):
    '''expr : expr EXPONENT expr
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr INTDIV expr
            | expr MODULUS expr
            '''
    p[0] = Operation(p[1], p[2], p[3])

def p_paren_parentheses(p):
    'paren : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_variable(p):
    'expr : VARIABLE'
    p[0] = Variable(p[1])

def p_expr_number(p):
    'expr : NUMBER'
    p[0] = Number(p[1])

def p_expr_string(p):
    'expr : STRING'
    p[0] = StringNode(p[1])

def p_expr_init(p):
    '''expr : list
            | tuple
            | paren
            '''
    p[0] = p[1]


def p_tuple_tuple(p):
    '''tuple : LPAREN listing RPAREN'''
    p[0] = Tuple(p[2])

def p_expr_tupleindex(p):
    '''expr : TUPLEINDEXING NUMBER expr'''
    p[0] = TupleIndex(p[2],p[3])

def p_list_list(p):
    '''list : LLIST listing RLIST
            | LLIST RLIST'''
    if p[2] == ']':    p[0] = List([])
    else:              p[0] = List(p[2])

def p_listing_listing(p):
    '''listing : expr COMMA listing'''
    # try:
    p[0] = [p[1]]+p[3]
    # except:
    #     semantic_error_handle()

def p_listing_listingTail(p):
    '''listing : expr
                | expr COMMA'''
    # try:
    p[0] = [p[1]]
    # except:
    #     semantic_error_handle()


def p_expr_listindex(p):
    ''' expr : expr LLIST expr RLIST'''
    p[0] = ListIndex(p[1], p[3])

def p_list_conslist(p):
    '''expr : expr CONS expr'''
    p[0] = Operation(p[1], p[2], p[3])

def p_error(p):
    print("SYNTAX ERROR")
    sys.exit()

def semantic_error_handle():
    print("SEMANTIC ERROR")
    raise SystemExit

import ply.yacc as yacc
parser = yacc.yacc(debug = False)

def parse(inp):
    result = parser.parse(inp, debug = 1)
    return result

def main():
    with open(sys.argv[1], 'r') as inputFile:
        inputText = inputFile.read().replace('\n', '')
        tokenize(inputText)
        result = parse(inputText)
        try:
            result.eval()
        except:
            semantic_error_handle()
    # while True:
    #     inp = input("Enter a expression: ").replace('\n', '')
    #     tokenize(inp)
    #     result = parse(inp)
    #     print(result)
    #     if result is not None:
    #         try:
    #             result.eval()
    #         except:
    #             semantic_error_handle()

if __name__ == "__main__":
    main()
