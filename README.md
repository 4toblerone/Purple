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
grammar =  {"baseexpr" : [["andmathop"]],
			"andmathop" : [["mathop", "and","andmathop"],["mathop"]],
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
So in our example for symbols mathop and plus we would have
```python
class MathopNode(Node):
	pass
	
class PlusNode(LeafNode):
	pass
```
Some "leaf" symbols obviously don't have any semantic meaning like ```and``` so for them there is
no need to be represented with a class.

Semantic meaning of each symbol is defined by overriding Node's ```dooperation()``` method.
For 'leaf' symbols if not overriden dooperation will return value of token associated with that
particular symbol.



To build AST(SDT) create AST obj provide token list, start node
(object corresponding to start symbol), grammar and nodes
