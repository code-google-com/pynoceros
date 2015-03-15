# Sample Usage
# pynocerous #

## Sample Usage ##

# Standard Imports

>>> from pynoceros.Parser import Parser
>>> from pynoceros.CompilerEnvirons import CompilerEnvirons
>>> from pynoceros.ErrorReporter import ErrorReporter

# Create our parser object and parse a simple script

>>> p = Parser(CompilerEnvirons(), ErrorReporter())
>>> tree = p.parse("alert('hello world');", sourceURI="", lineno=0)

# Now we can traverse the parse tree. The token type can be compared to values
# on the Token class,

>>> from pynoceros.Token import Token
>>> tree.getType() == Token.SCRIPT
TRUE

# or displayed as a string using Token.name

>>> print Token.name(tree.getType())
'SCRIPT'

# Use getFirstChild(), getLastChild() and getNext() to navigate the nodes.

>>> tree.getFirstChild().getFirstChild()
<pynoceros.Node.Node object at 0x7ff61a375a90>
>>> tree.getFirstChild().getFirstChild().getFirstChild()
<pynoceros.Node.StringNode object at 0x7ff61a375a50>
>>> tree.getFirstChild().getFirstChild().getFirstChild().getString()
'alert'