Purple
===

Purple has two main parts: 
  - parser
  - tree maker
  
## Parser


Purple parser is dynamic as he can parse any non-left-recursive grammar.
Grammar is part defined by the user and part which is necessary 
to create ParseText obj. Grammar is represented in form of a dict, eg:
`
```python

grammar =  {"baseexpr" : [["mathop"]],
    		"mathop": [["number","operator","mathop"],["number"]],
			"operator":[["plus"],["minus"]]}
```
			
2nd argument which is required to create ParseText obj is grammar's start symbol.
In this case "baseexpr" would be the one.

After creating ParseText obj ( ```parser = ParserText(grammar, "baseexpr")``` ) to check if
some list of tokens (list of token type to be more precise) can be generated 
from specified grammar just call parse method (which returns True or False)
with token list as its argument
```python

parser.parse(token_list)
```

During parsing process, parser is making trace which indicates how to build
something that very much resembles to AST.

## AST

Every symbol in a grammar should be represented with a class of its own. 
Depending if symbol is a "leaf" or a "node" (it's a leaf if it doesn't have production rule
otherwise it's a node) coresponding class should inherit from LeafNode or Node class.

Some "leaf" symbols obviously don't have any semantic meaning like ```and``` so for them there is
no need to be represented with a class.

Semantic meaning of each symbol is defined by overriding Node's ```dooperation()``` method.
For 'leaf' symbols if not overriden dooperation will return value of token associated with that
particular symbol.
So in our example for symbols mathop, operator and plus we would have

```python
import operator

class MathOpNode(Node):
	def dooperation(self):
        if len(self.childrens) == 3:
            op_func = self.childrens[1].dooperation()
            arg_1 = self.childrens[0].dooperation()
            arg_2 = self.childrens[2].dooperation()
            return op_func(arg_1,arg_2)
        else:
            return self.childrens[0].dooperation()
            
class Operator(Node):
	def dooperation(self):
		return self.childrens[0].dooperation()
            
class PlusNode(LeafNode):
	dooperation():
		return operator.add
```

Final stage is to create dict with symbols as keys and theirs corresponding classes as values.

```python
nodes={
	"mathopnode" : MathOpNode,
	"plus" : PlusNode,
	.
	.
	.
}
```

To build AST(SDT) first create AST obj providen with token list, start node (object corresponding to start symbol), 
grammar and nodes ``` ast = AST(token_list, start_node, grammar, nodes)``` 
and then call create_tree method with start symbol and trace (from parser) as arguments ``` ast.create_tree(start_symbol, trace)```
After that tree is created and its root is ```tree_nodes```'s first element.

Assuming you have defined semantic meaning(with overriding ```dooperation()```) for every symbol, to execute your source code
you can just call ```dooperation()``` on the root node of the previously created tree. 




