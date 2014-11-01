import operator

t_PLUS = r'\+'
t_MINUS = r'-'

def t_AND(token):
    r'and'
    return token


def t_WORD(t):
    r'[a-z]+'
    return t


def t_NUMBER(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_WHITESPACES(token):
    r'" "'
    pass

def t_error(t):
    print 'Illegal character'
    t.lexer.skip(1)

t_ignore = ' \t\v\r'  # shortcut for whitespaces

tokens = ['WORD', 'NUMBER','PLUS', 'MINUS', 'WHITESPACES' ,'AND']

class Node(object):
    """docstring for Node"""

    def __init__(self):
        self.childrens = []

    def add(self, child):
        self.childrens.append(child)

    def dooperation(self):
        """do operation on childrens, eval"""
        pass

    def __str__(self):
        print "<" + self.__class__.__name__ + ">"
        if len(self.childrens) == 0:
            return "Nema vise dece ova grana"
        for child in self.childrens:
            print child.__str__()
        return "to"


class LeafNode(Node):
    def __init__(self, token):
        super(LeafNode, self).__init__()
        self.token = token

    def dooperation(self):
        return self.token.value


class BaseExprNode(Node):
    def dooperation(self):
        #print "BaseExpr"
        return self.childrens[0].dooperation()


class AndMathOpNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class MathOpNode(Node):
    def dooperation(self):
        if len(self.childrens) == 3:
            op_func = self.childrens[1].dooperation()
            arg_1 = self.childrens[0].dooperation()
            arg_2 = self.childrens[2].dooperation()
            return op_func(arg_1,arg_2)
        else:
            return self.childrens[0].dooperation()


class OperatorNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class NumberNode(LeafNode):
    def dooperation(self):
        return self.token.value


class PlusNode(LeafNode):
    def dooperation(self):
        return operator.add


class MinusNode(LeafNode):
    def dooperation(self):
        return operator.sub

grammar =  {"baseexpr" : [["andmathop"]],
			"andmathop" : [["mathop", "and","andmathop"],["mathop"]],
    		"mathop": [["number","operator","mathop"],["number"]],
			"operator":[["plus"],["minus"]]}


nodes = {"baseexpr": BaseExprNode,
         "andmathop" : AndMathOpNode,
         "mathop" : MathOpNode,
         "operator" : OperatorNode,
         "number" : NumberNode,
         "plus": PlusNode,
         "minus": MinusNode}


def bajt (arg1):
    def fun(arg2):
        print arg1 + arg2

    return fun

BYTECODE ={}

def bytecode(code):
    def cl(func):
        BYTECODE[code] = func
        return func

    return cl

# @bytecode(code = "pet")
def proba(arg1):
    print arg1

# proba("argument")
# print BYTECODE

bytecode("neki kod")("string")
print BYTECODE
proba = bytecode("stoti")
proba("pet")