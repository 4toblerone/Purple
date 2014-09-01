import ply.lex as lex
from collections import deque  

def breakDownStringToTokens(text, module):
        lexer = lex.lex(module)
        lexer.input(text)
        token_list = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            token_list.append(tok)
        return token_list

def resetfileds(fn):
    """Decorator for reseting object's fields"""
    def wrapper(self, *args):
        result = fn(self, *args)
        self.__init__()
        return result
    return wrapper


# TODO do proper exception on this
def tryit(func):
    """Decorator which encloses every other exception 
       and raises SyntaxException"""
    def wrapit(*args):
        try:
            func(*args)
        except Exception :
            raise SyntaxException("Code is not syntactically correct!")
    return wrapit


class SyntaxException(Exception):
    """"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParseText:

    def __init__(self, grammar, start_nonterminal):
        """
        Keywords arguments:
        grammar -- dictionary representing language grammar
        start_nonterminal -- grammar's start symbol/nonterminal 
        """
        self.grammar = grammar
        self.start_nonterminal = start_nonterminal
    
        
    def _initialize(self):
        #self.start_nonterminal = start_nonterminal
        # where_was_i[0] -> step in rule list
        # where_was_i[1] -> choosen rule
        # where_was_i[2] -> num of tokens, so we can know how
        # many tokens we need to go back if the current rule 
        # is not THE one
        self.daddy_stack = [self.start_nonterminal]
        self.helperstack = [[self.start_nonterminal, 0]]
        self.where_was_i = {self.start_nonterminal: [[0, 0, 0]]}
        self.x = 0 #all tokens matched
        self.removed = {}

    def addnewtohs(self, rule):
        self.helperstack.append([rule, 0])

    def uphelperstack(self):
        for upstair_rule in self.helperstack:
            upstair_rule[1] += 1

    def removefromhs(self):
        tocut = self.helperstack[-1][1]
        del self.helperstack[-1]
        for upstair_rule in self.helperstack:
            upstair_rule[1] -= tocut
        return tocut

    def downsizehs(self):
        tocut = self.helperstack[-1][1]
        for node in self.helperstack:
            node[1] -= self.helperstack[-1][1]
        return tocut

    def deletelasths(self):
        del self.helperstack[-1]

    def move_forward(self):
        self.where_was_i[self.daddy_stack[-1]][-1][1] += 1
        self.where_was_i[self.daddy_stack[-1]][-1][0] = 0
        self.where_was_i[self.daddy_stack[-1]][-1][2] = 0

    def parse(self, token_list):
        self._initialize()
        try:
            return self._validate(token_list)
        except Exception:
            #raise SyntaxException("Not valid!")
            return False

    # TODO get rid of the need for cushion node
    # what if token type defined doesn't exists in grammar dict?
    # add position 'x' of the token i token list so user can
    # have information where exception occured
    # What about context menager? Ain't gonna work
    #@resetfileds doesn't work cuz of recursion
    #@tryit , replaced by putting it in proper parse method
    def _validate(self, token_list):
        """Checks if given stream of tokens can be 
        generated from a given grammar. 

        Keywords arguments:
        token_list -- list of tokens
        """
        rule_list = self.grammar[self.daddy_stack[-1]][
            self.where_was_i[self.daddy_stack[-1]][-1][1]]
        # are we at and of the rule
        if len(rule_list[self.where_was_i[self.daddy_stack[-1]][-1][0]:]) == 0:
            if len(self.daddy_stack) > 1:
                self.daddy_stack.pop()
                return self._validate(token_list)
            elif len(token_list) > self.x:
                return False
        # did we check all tokens in the list
        if self.x == len(token_list):
            if len(self.daddy_stack) == 1:
                self.where_was_i = mergeall(self.removed, self.where_was_i)
                return True
            else:
                # check if there are more list of rules, and if there are
                # move to the next rule list and decrease self.x
                if self.where_was_i[self.daddy_stack[-1]][-1][1] < len(self.grammar[self.daddy_stack[-1]]):
                    self.where_was_i = mergeall(self.removed, self.where_was_i)
                    self.removed.clear()
                    while self.helperstack[-1][0] is not self.daddy_stack[-1]:
                        del self.where_was_i[self.helperstack[-1][0]][-1]
                        if self.helperstack[-1][0] in self.removed:
                            self.removed[self.helperstack[-1][0]][0] -= 1
                        self.x -= self.removefromhs()
                    self.move_forward()
                    return self._validate(token_list)

                if self.where_was_i[self.daddy_stack[-1]][-1][0] == len(
                        self.grammar[self.daddy_stack[-1]][self.where_was_i[self.daddy_stack[-1]][-1][1]]) - 1:
                    if len(self.daddy_stack) > 1:
                        # we can not get back all the way
                        if len(self.where_was_i[self.daddy_stack[-1]]) > 1:
                            last_one = self.where_was_i[
                                self.daddy_stack[-1]].pop()
                            self.removed[self.daddy_stack[-1]].append(
                                (self.removed[self.daddy_stack[-1]][0], last_one))
                            #del self.where_was_i[self.daddy_stack[-1]][-1]
                        self.daddy_stack.pop()
                        return self._validate(token_list)
                return False
        # if it is at the begging of the certain rule group(one rule can have
        # more then one group of rules)
        # and if length of that r.g. is biger than the num of 
        if self.where_was_i[self.daddy_stack[-1]][-1][0] == 0 and len(rule_list) > len(token_list) - self.x:
            # if we didnt check all rule groups
            if len(self.grammar[self.daddy_stack[-1]]) - 1 > self.where_was_i[self.daddy_stack[-1]][-1][1]:
                # get to the next rule list
                self.move_forward()
                # delete the last one on where_was_i and delete
                # kids of his parent
                self.x -= self.downsizehs()
                return self._validate(token_list)
            elif len(self.daddy_stack) > 1:
                # if we tried every grupe of rules, delete everything
                # from helperstack ()
                del self.daddy_stack[-1]
                while self.helperstack[-1][0] is not self.daddy_stack[-1]:
                    if len(self.removed[self.helperstack[-1][0]]) > 1 and self.removed[self.helperstack[-1][0]][-1][
                        0] == self.removed[self.helperstack[-1][0]][0]:
                        del self.removed[self.helperstack[-1][0]][-1]
                    else:
                        del self.where_was_i[self.helperstack[-1][0]][-1]
                    self.removed[self.helperstack[-1][0]][0] -= 1
                    self.x -= self.removefromhs()
                self.x -= self.downsizehs()
                self.move_forward()
                return self._validate(token_list)
            else:
                return False
        for index, pravilo in enumerate(rule_list[self.where_was_i[self.daddy_stack[-1]][-1][0]:]):
            # check if it leaf/terminal
            if pravilo not in self.grammar.keys():
                self.where_was_i[self.daddy_stack[-1]][-1][0] += 1
                # it means its leaf, next check if it is that type of tokens
                if self.x <= len(token_list) - 1 and pravilo == token_list[self.x].type.lower():
                    self.x += 1
                    self.where_was_i[self.daddy_stack[-1]][-1][2] += 1
                    self.uphelperstack()
                    # did we finish one list of rules, if we did and
                    # on daddy_stack has more then one 
                    if self.where_was_i[self.daddy_stack[-1]][-1][0] == len(rule_list):
                        if len(self.daddy_stack) > 1:  # reason for cushion!
                            if len(self.where_was_i[self.daddy_stack[-1]]) > 1:
                                poslednji = self.where_was_i[
                                    self.daddy_stack[-1]].pop()
                                self.removed[self.daddy_stack[-1]].append(
                                    (self.removed[self.daddy_stack[-1]][0], poslednji))
                            self.daddy_stack.pop()
                            # self.deletelasths()
                            return self._validate(token_list)
                        else:
                            return False
                elif self.x <= len(token_list) - 1 and pravilo != token_list[self.x].type.lower():
                    if len(self.grammar[self.daddy_stack[-1]]) - 1 > self.where_was_i[self.daddy_stack[-1]][-1][1]:
                        self.where_was_i[self.daddy_stack[-1]][-1][1] += 1
                        # reset where were we aka x == 0
                        self.where_was_i[self.daddy_stack[-1]][-1][0] = 0
                        while self.helperstack[-1][0] is not self.daddy_stack[-1]:
                            if len(self.removed[self.helperstack[-1][0]]) > 1 and \
                                self.removed[self.helperstack[-1][0]][-1][0] == \
                                self.removed[self.helperstack[-1][0]][0]:
                                del self.removed[self.helperstack[-1][0]][-1]
                            else:
                                del self.where_was_i[self.helperstack[-1][0]][-1]
                            self.removed[self.helperstack[-1][0]][0] -= 1
                            self.x -= self.removefromhs()
                        self.x -= self.downsizehs()
                        self.where_was_i[self.daddy_stack[-1]][-1][2] = 0
                        return self._validate(token_list)
                    elif len(self.daddy_stack) > 1:
                        while self.helperstack[-1][0] is not self.daddy_stack[-1]:
                            if len(self.removed[self.helperstack[-1][0]]) > 1 and \
                                self.removed[self.helperstack[-1][0]][-1][0] == \
                                self.removed[self.helperstack[-1][0]][0]:
                                del self.removed[self.helperstack[-1][0]][-1]
                            else:
                                del self.where_was_i[self.helperstack[-1][0]][-1]
                            self.removed[self.helperstack[-1][0]][0] -= 1
                            self.x -= self.removefromhs()
                        
                        self.x -= self.downsizehs()
                        self.where_was_i[self.daddy_stack[-1]][-1][2] = 0
                        
                        del self.where_was_i[self.daddy_stack[-1]][-1]
                        self.removed[self.daddy_stack[-1]][0] -= 1
                        del self.daddy_stack[-1]
                        # if there are more rule lists in the list
                        if len(self.grammar[self.daddy_stack[-1]]) - 1 > self.where_was_i[self.daddy_stack[-1]][-1][1]:
                            self.move_forward()
                            self.x -= self.downsizehs()
                            self.deletelasths()
                        else:
                            self.where_was_i[self.daddy_stack[-1]][-1][0] = len(
                                self.grammar[self.daddy_stack[-1]][self.where_was_i[self.daddy_stack[-1]][-1][1]])
                        return self._validate(token_list)
                else:
                    return False
            # if it is not leaf/terminal find list 
            # with that key in grammar dic and add it on daddy_stack
            else:
                self.where_was_i[self.daddy_stack[-1]][-1][0] += 1
                self.daddy_stack.append(pravilo)
                self.addnewtohs(pravilo)
                if pravilo not in self.where_was_i:
                    self.where_was_i[pravilo] = []
                self.where_was_i[pravilo].append([0, 0, 0])
                self.removed[pravilo] = self.removed.get(pravilo, [-1])
                self.removed[pravilo][0] = len(
                    self.where_was_i[pravilo]) + len(self.removed[pravilo]) - 2
                return self._validate(token_list)


def mergeall(removed, where_was_i):

    def merge(popeditems, key):

        lista = []
        i = 0
        where_was_i_part = deque(where_was_i[key])
        length = len(popeditems) + len(where_was_i_part)  # 3
        while i < length:
            if popeditems and i == popeditems[0][0]:
                lista.append(popeditems[0][1])
                del popeditems[0]
            elif len(where_was_i_part) > 0:
                lista.append(where_was_i_part[0])
                del where_was_i_part[0]
            else:
                lista.append(popeditems[0][1])
                del popeditems[0]
            i += 1
        return lista

    for key, value in removed.iteritems():
        if len(value) > 1:
            where_was_i[key] = merge(value[1:], key)
    return where_was_i


class AST(object):

    def __init__(self, token_list, start_node,grammar, nodes):
        """
        Keyword arguments:

        token_list -- List of tokens
        trace -- Dictionary which represents trace parser left while
                 moving 'through' the language grammar
        start_node -- Instace of class associated with start rule
        """
        #self.stack = [BaseExprNode()]
        self.start_node = start_node
        self.token_list = token_list
        self.stack = [self.start_node]
        self.stack2 = []
        self.dek = deque(self.token_list)
        self.grammar = grammar
        self.nodes = nodes

    def _initialize(self):
        self.stack = [self.start_node]
        self.stack2 = []
        self.dek = deque(self.token_list)

    # TODO initialize before tree creation starts
    # TODO think about generators
    def createnode(self,class_ref, *args):
        return class_ref(*args)

    def createleaf(self,class_ref, token_value):
        return self.createnode(class_ref, token_value)

    def createtree(self, key, trace):
        """
        Recursively creates SDT tree using language grammar
        and trace left by parse function

        Keyword arguments:
        key -- leftside nonterminal 
        grammar -- dictionary representing language grammar
        nodes -- dictionary connecting certain (non)terminals 
        and theirs corresponding classes
        """
        rulenum = trace[key][0][1]
        for index, rule in enumerate(self.grammar[key][rulenum]):
            if rule in self.nodes:
                if rule not in self.grammar:
                    self.stack[-1].add(self.createleaf(self.nodes[rule], self.dek.popleft()))
                    if index == len(self.grammar[key][rulenum]) - 1 and len(self.stack) > 1:
                        self.stack.pop()
                        del trace[key][0]
                else:
                    node = self.createnode(self.nodes[rule])
                    self.stack[-1].add(node)
                    if index == len(self.grammar[key][rulenum]) - 1:
                        if len(self.stack) == 1:
                            self.stack2.append(self.stack.pop())
                        else:
                            self.stack.pop()
                        del trace[key][0]
                    self.stack.append(node)
                    self.createtree(rule,trace)
            else:
                self.dek.popleft()
