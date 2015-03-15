# Overview #

Pynocerous contains a port the tokenizer etc. for the Rhino JavaScript interpreter (http://www.mozilla.org/rhino/). It does not currently contain any way to execute the provided token stream.

## Why... ##

This project started with the following goals:
  1. As part of a python port of the yui-compressor (which is almost complete and coming soon)
  1. For a personal challenge

## Sample ##

```
from pynoceros.Parser import Parser
from pynoceros.CompilerEnvirons import CompilerEnvirons
from pynoceros.ErrorReporter import ErrorReporter
p = Parser(CompilerEnvirons(), ErrorReporter())
tree = p.parse("alert('hello world');", sourceURI="", lineno=0)
```

## You may be interested... ##
An other pure python javascript parser you may be interested in is pynarcissus (http://code.google.com/p/pynarcissus/).

If you are looking for a robust javascript interpreter accessable from python you may be interested in pyv8 (http://code.google.com/p/pyv8/).


## About the code ##

Large parts of the code were origionally converted from Java using java2python (http://code.google.com/p/java2python/). As such, the code currently isn't very pythonic, or optimised for python.

Patches are very welcome.