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
```
parser.parse(token_list)
```

During parsing process parser is making trace which idicates how to build
something that very much resembles to AST.

## AST

To build AST(SDT) create AST obj provide token list, start node
(object corresponding to start symbol), grammar and nodes
