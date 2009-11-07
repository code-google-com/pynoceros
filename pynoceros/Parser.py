#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Pynoceros code (ported from Rhino)
#
# The Initial Developer of the Original Code is
# Tim Wintle.
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#       Tim Wintle
#       Team Rubber (http://www.teamrubber.com/blog/)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

from Decompiler import Decompiler
from IRFactory import IRFactory
from CompilerEnvirons import CompilerEnvirons
from ErrorReporter import ErrorReporter
from TokenStream import TokenStream
from Hashtable import Hashtable
from Token import Token
from ScriptRuntime import ScriptRuntime
from FunctionNode import FunctionNode
from ScriptOrFnNode import ScriptOrFnNode
from Node import Node
from Context import Context

class ParserException(RuntimeError):
    """ generated source for ParserException
    """
    serialVersionUID = 5882582646773765630L
    

class Parser(object):
    """ generated source for Parser

    """
    CLEAR_TI_MASK = 0xFFFF
    TI_AFTER_EOL = 1 << 16
    TI_CHECK_LABEL = 1 << 17
    compilerEnv = CompilerEnvirons()
    errorReporter = ErrorReporter()
    sourceURI = ""
    calledByCompileFunction = bool()
    #ts = TokenStream()
    currentFlaggedToken = 0
    syntaxErrorCount = 0
    #nf = IRFactory()
    nestingOfFunction = 0
    decompiler = Decompiler()
    encodedSource = ""
    currentScriptOrFn = None #ScriptOrFnNode()
    nestingOfWith = 0
    labelSet = Hashtable()
    loopSet = []#ObjArray()
    loopAndSwitchSet = []#ObjArray()
    hasReturnValue = bool()
    functionEndFlags = 0

    def __init__(self, compilerEnv, errorReporter):
        self.compilerEnv = compilerEnv
        self.errorReporter = errorReporter

    def createDecompiler(self, compilerEnv):
        return Decompiler()

    def addStrictWarning(self, messageId, messageArg):
        if self.compilerEnv.isStrictMode():
            self.addWarning(messageId, messageArg)

    def addWarning(self, messageId, messageArg):
        message = ScriptRuntime.getMessage1(messageId, messageArg)
        if self.compilerEnv.reportWarningAsError():
            self.syntaxErrorCount += 1
            self.errorReporter.error(message, self.sourceURI, self.ts.getLineno(), self.ts.getLine(), self.ts.getOffset())
        else:
            self.errorReporter.warning(message, self.sourceURI, self.ts.getLineno(), self.ts.getLine(), self.ts.getOffset())

    def addError(self, messageId, messageArg = None):
        if messageArg is not None:
            return self.addError_0(messageId, messageArg)
        self.syntaxErrorCount += 1
        print "ERROR (error not done) -> ", self.sourceURI, self.ts.getLineno(), \
                        self.ts.getLine(), self.ts.getOffset()
        
        message = ScriptRuntime.getMessage0(messageId)
        self.errorReporter.error(message, self.sourceURI, self.ts.getLineno(), self.ts.getLine(), self.ts.getOffset())
        

    def addError_0(self, messageId, messageArg):
        self.syntaxErrorCount += 1
        message = ScriptRuntime.getMessage1(messageId, messageArg)
        self.errorReporter.error(message, self.sourceURI, self.ts.getLineno(), self.ts.getLine(), self.ts.getOffset())

    def reportError(self, messageId):
        self.addError(messageId)
        raise ParserException()

    def peekToken(self):
        tt = self.currentFlaggedToken
        if (tt == Token.EOF):
            tt = self.ts.getToken()
            while (tt == Token.CONDCOMMENT) or (tt == Token.KEEPCOMMENT):
                if (tt == Token.CONDCOMMENT):
                    self.decompiler.addJScriptConditionalComment(self.ts.getString())
                else:
                    self.decompiler.addPreservedComment(self.ts.getString())
                tt = self.ts.getToken()
            if (tt == Token.EOL):
                while (tt == Token.EOL) or (tt == Token.CONDCOMMENT) or (tt == Token.KEEPCOMMENT):
                    tt = self.ts.getToken()
                    if (tt == Token.CONDCOMMENT):
                        self.decompiler.addJScriptConditionalComment(self.ts.getString())
                    else:
                        if (tt == Token.KEEPCOMMENT):
                            self.decompiler.addPreservedComment(self.ts.getString())
                tt |= self.TI_AFTER_EOL
            self.currentFlaggedToken = tt
        return tt & self.CLEAR_TI_MASK

    def peekFlaggedToken(self):
        self.peekToken()
        return self.currentFlaggedToken

    def consumeToken(self):
        self.currentFlaggedToken = Token.EOF

    def nextToken(self):
        tt = self.peekToken()
        self.consumeToken()
        return tt

    def nextFlaggedToken(self):
        self.peekToken()
        ttFlagged = self.currentFlaggedToken
        self.consumeToken()
        return ttFlagged

    def matchToken(self, toMatch):
        tt = self.peekToken()
        if (tt != toMatch):
            return False
        self.consumeToken()
        return True

    def peekTokenOrEOL(self):
        tt = self.peekToken()
        if (self.currentFlaggedToken & self.TI_AFTER_EOL != 0):
            tt = Token.EOL
        return tt

    def setCheckForLabel(self):
        if (self.currentFlaggedToken & self.CLEAR_TI_MASK != Token.NAME):
            raise Kit.codeBug()
        self.currentFlaggedToken |= self.TI_CHECK_LABEL

    def mustMatchToken(self, toMatch, messageId):
        if not self.matchToken(toMatch):
            self.reportError(messageId)

    def mustHaveXML(self):
        if not self.compilerEnv.isXmlAvailable():
            self.reportError("msg.XML.not.available")

    def getEncodedSource(self):
        return self.encodedSource

    def eof(self):
        return self.ts.eof()

    def insideFunction(self):
        return (self.nestingOfFunction != 0)

    def enterLoop(self, loopLabel):
        loop = self.nf.createLoopNode(loopLabel, self.ts.getLineno())
        if self.loopSet is None:
            self.loopSet = []#ObjArray()
            if self.loopAndSwitchSet is None:
                self.loopAndSwitchSet = []#ObjArray()
        self.loopSet.append(loop)
        self.loopAndSwitchSet.append(loop)
        return loop

    def exitLoop(self):
        self.loopSet.pop()
        self.loopAndSwitchSet.pop()

    def enterSwitch(self, switchSelector, lineno):
        switchNode = self.nf.createSwitch(switchSelector, lineno)
        if self.loopAndSwitchSet is None:
            self.loopAndSwitchSet = []#ObjArray()
        self.loopAndSwitchSet.append(switchNode)
        return switchNode

    def exitSwitch(self):
        self.loopAndSwitchSet.pop()

    #@overloaded
    def parse(self, sourceString, sourceURI, lineno):
        self.sourceURI = sourceURI
        self.ts = TokenStream(self, None, sourceString, lineno)
        try:
            return self.parse_main()
        #TODO:
        #except (IOException, ), ex:
        except TypeError, e: 
            print e
            raise
            raise IllegalStateException()
            
    def parse_main(self):
        """This was overloaded in Java"""
        self.decompiler = self.createDecompiler(self.compilerEnv)
        self.nf = IRFactory(self)
        self.currentScriptOrFn = self.nf.createScript()
        sourceStartOffset = self.decompiler.getCurrentOffset();
        self.encodedSource = None;
        self.decompiler.addToken(Token.SCRIPT);
        
        self.currentFlaggedToken = Token.EOF;
        self.syntaxErrorCount = 0;

        baseLineno = self.ts.getLineno();  #// line number where source starts

        #/* so we have something to add nodes to until
        # * we've collected all the source */
        pn = self.nf.createLeaf(Token.BLOCK);
        try:
            while(True):
                tt = self.peekToken()
                if (tt <= Token.EOF):
                    break
                n = None
                
                if tt == Token.FUNCTION:
                    self.consumeToken()
                    try: 
                        n = self.function( \
                            (FunctionNode.FUNCTION_EXPRESSION,\
                            FunctionNode.FUNCTION_STATEMENT)[self.calledByCompileFunction])
                    except ParserException:
                        raise NotImplementedError()#  should this have to raise?
                        break;
                    #raise NotImplementedError <- I think this is now implemented - TW
                
                else:
                    n = self.statement()
                    
                self.nf.addChildToBack(pn, n)
                    
           
        except RuntimeError:
            # Was StackOverflowError
            raise
            # TODO: exception handling
        
        if (self.syntaxErrorCount != 0) :
            msg = str(self.syntaxErrorCount)
            #msg = ScriptRuntime.getMessage1("msg.got.syntax.errors", msg);
            #throw errorReporter.runtimeError(msg, sourceURI, baseLineno,
            #                                 null, 0);

        self.currentScriptOrFn.setSourceName(self.sourceURI);
        self.currentScriptOrFn.setBaseLineno(baseLineno);
        self.currentScriptOrFn.setEndLineno(self.ts.getLineno());

        sourceEndOffset = self.decompiler.getCurrentOffset();
        self.currentScriptOrFn.setEncodedSourceBounds(sourceStartOffset,
                                                 sourceEndOffset);

        self.nf.initScript(self.currentScriptOrFn, pn);

        if (self.compilerEnv.isGeneratingSource()):
            self.encodedSource = self.decompiler.getEncodedSource();
            
        del self.decompiler# comment was //"It helps GC" 
                                  # - can't do any harm on CPython either

        return self.currentScriptOrFn;
    """
        private ScriptOrFnNode parse()
        throws IOException
    {
        this.decompiler = createDecompiler(compilerEnv);
        this.nf = new IRFactory(this);
        currentScriptOrFn = nf.createScript();
        int sourceStartOffset = decompiler.getCurrentOffset();
        this.encodedSource = null;
        decompiler.addToken(Token.SCRIPT);

        this.currentFlaggedToken = Token.EOF;
        this.syntaxErrorCount = 0;

        int baseLineno = ts.getLineno();  // line number where source starts

        /* so we have something to add nodes to until
         * we've collected all the source */
        Node pn = nf.createLeaf(Token.BLOCK);

        try {
            while (true) {
                int tt = peekToken();

                if (tt <= Token.EOF) {
                    break;
                }

                Node n;
                if (tt == Token.FUNCTION) {
                    consumeToken();
                    try {
                        n = function(calledByCompileFunction
                                     ? FunctionNode.FUNCTION_EXPRESSION
                                     : FunctionNode.FUNCTION_STATEMENT);
                    } catch (ParserException e) {
                        break;
                    }
                } else {
                    n = statement();
                }
                nf.addChildToBack(pn, n);
            }
        } catch (StackOverflowError ex) {
            String msg = ScriptRuntime.getMessage0(
                "msg.too.deep.parser.recursion");
            throw Context.reportRuntimeError(msg, sourceURI,
                                             ts.getLineno(), null, 0);
        }

        if (this.syntaxErrorCount != 0) {
            String msg = String.valueOf(this.syntaxErrorCount);
            msg = ScriptRuntime.getMessage1("msg.got.syntax.errors", msg);
            throw errorReporter.runtimeError(msg, sourceURI, baseLineno,
                                             null, 0);
        }
    }"""
    
    #/*
    # * The C version of this function takes an argument list,
    # * which doesn't seem to be needed for tree generation...
    # * it'd only be useful for checking argument hiding, which
    # * I'm not doing anyway...
    # */
    def parseFunctionBody(self):
        self.nestingOfFunction += 1 ;
        pn = self.nf.createBlock(self.ts.getLineno());
        try:
            #bodyLoop: while (true) {
            while True:
                n = None
                tt = self.peekToken();
                if tt in (Token.ERROR, 
                          Token.EOF, 
                          Token.RC):
                    break
                elif tt == Token.FUNCTION:
                    self.consumeToken()
                    n = self.function(FunctionNode.FUNCTION_STATEMENT)
                else:
                    n = self.statement()

                self.nf.addChildToBack(pn,n)

        except AttributeError, e:
            # Think this is for empty functions, where n = None?
            # doesn't seem to be happending any more though
            # TimW
            raise
            # pass
        finally:
            self.nestingOfFunction -= 1
        return pn;

    def function(self, functionType):
        syntheticType = functionType
        baseLineno = self.ts.getLineno()
        functionSourceStart = self.decompiler.markFunctionStart(functionType)
        name = ""
        memberExprNode = None
        if self.matchToken(Token.NAME):
            name = self.ts.getString()
            self.decompiler.addName(name)
            if not self.matchToken(Token.LP):
                if self.compilerEnv.isAllowMemberExprAsFunctionName():
                    memberExprHead = self.nf.createName(name)
                    name = ""
                    memberExprNode = memberExprTail(False, memberExprHead)
                self.mustMatchToken(Token.LP, "msg.no.paren.parms")
        else:
            if self.matchToken(Token.LP):
                name = ""
            else:
                name = ""
                if self.compilerEnv.isAllowMemberExprAsFunctionName():
                    memberExprNode = self.memberExpr(False)
                self.mustMatchToken(Token.LP, "msg.no.paren.parms")
        if memberExprNode is not None:
            syntheticType = FunctionNode.FUNCTION_EXPRESSION
        nested = self.insideFunction()
        fnNode = self.nf.createFunction(name)
        if nested or self.nestingOfWith > 0:
            fnNode.itsIgnoreDynamicScope = True
        functionIndex = self.currentScriptOrFn.addFunction(fnNode)
        functionSourceEnd = 0
        savedScriptOrFn = self.currentScriptOrFn
        self.currentScriptOrFn = fnNode
        savedNestingOfWith = self.nestingOfWith
        self.nestingOfWith = 0
        savedLabelSet = self.labelSet
        self.labelSet = None
        savedLoopSet = self.loopSet
        self.loopSet = None
        savedLoopAndSwitchSet = self.loopAndSwitchSet
        self.loopAndSwitchSet = None
        savedHasReturnValue = self.hasReturnValue
        savedFunctionEndFlags = self.functionEndFlags
        body = None#Node()
        try:
            self.decompiler.addToken(Token.LP)
            if not self.matchToken(Token.RP):
                first = True
                while first or self.matchToken(Token.COMMA):
                    if not first:
                        self.decompiler.addToken(Token.COMMA)
                    first = False
                    self.mustMatchToken(Token.NAME, "msg.no.parm")
                    s = self.ts.getString()
                    if fnNode.hasParamOrVar(s):
                        self.addWarning("msg.dup.parms", s)
                    fnNode.addParam(s)
                    self.decompiler.addName(s)
                self.mustMatchToken(Token.RP, "msg.no.paren.after.parms")
            self.decompiler.addToken(Token.RP)
            self.mustMatchToken(Token.LC, "msg.no.brace.body")
            self.decompiler.addEOL(Token.LC)
            body = self.parseFunctionBody()
            self.mustMatchToken(Token.RC, "msg.no.brace.after.body")
            if self.compilerEnv.isStrictMode() and not body.hasConsistentReturnUsage():
                msg = ""
                if len(name) > 0:
                    msg = "msg.no.return.value"
                else:
                    msg ="msg.anon.no.return.value"
                
                self.addStrictWarning(msg, name)
            self.decompiler.addToken(Token.RC)
            functionSourceEnd = self.decompiler.markFunctionEnd(functionSourceStart)
            if (functionType != FunctionNode.FUNCTION_EXPRESSION):
                self.decompiler.addToken(Token.EOL)
        except:
            raise
            # pass
            pass
        finally:
            self.hasReturnValue = savedHasReturnValue
            self.functionEndFlags = savedFunctionEndFlags
            self.loopAndSwitchSet = savedLoopAndSwitchSet
            self.loopSet = savedLoopSet
            self.labelSet = savedLabelSet
            self.nestingOfWith = savedNestingOfWith
            self.currentScriptOrFn = savedScriptOrFn
        fnNode.setEncodedSourceBounds(functionSourceStart, functionSourceEnd)
        fnNode.setSourceName(self.sourceURI)
        fnNode.setBaseLineno(baseLineno)
        fnNode.setEndLineno(self.ts.getLineno())
        if name is not None:
            index = self.currentScriptOrFn.getParamOrVarIndex(name)
            if 0 <= index < self.currentScriptOrFn.getParamCount():
                self.addStrictWarning("msg.var.hides.arg", name)
        pn = self.nf.initFunction(fnNode, functionIndex, body, syntheticType)
        if memberExprNode is not None:
            pn = self.nf.createAssignment(Token.ASSIGN, memberExprNode, pn)
            if (functionType != FunctionNode.FUNCTION_EXPRESSION):
                pn = self.nf.createExprStatementNoReturn(pn, baseLineno)
        return pn
        
    def statement(self):
        try:
            pn = self.statementHelper(None)
            if (pn is not None):
                if (self.compilerEnv.isStrictMode() and \
                    not pn.hasSideEffects()):
                    addStrictWarning("msg.no.side.effects","")
                return pn
        except ParserException, e:
            print "Caught a Parser Exception in Parser.py", e
        except Exception:
            raise #catch (ParserException e) { }
            
        
        #skip to the end of statement
        lineno = self.ts.getLineno()
        while (True):
            tt = self.peekTokenOrEOL()
            self.consumeToken()
            if tt in (Token.ERROR, 
                      Token.EOF, 
                      Token.EOL, 
                      Token.SEMI):
                break
        return self.nf.createExprStatement(self.nf.createName("error"), lineno)
        
    def statementHelper(self, statementLabel):
        pn = None
        tt = 0
        tt = self.peekToken()
        if tt == Token.IF:
            self.consumeToken()
            self.decompiler.addToken(Token.IF)
            lineno = self.ts.getLineno()
            cond = self.condition()
            self.decompiler.addEOL(Token.LC)
            ifTrue = self.statement()
            ifFalse = None
            if self.matchToken(Token.ELSE):
                self.decompiler.addToken(Token.RC)
                self.decompiler.addToken(Token.ELSE)
                self.decompiler.addEOL(Token.LC)
                ifFalse = self.statement()
            self.decompiler.addEOL(Token.RC)
            pn = self.nf.createIf(cond, ifTrue, ifFalse, lineno)
            return pn
        elif tt == Token.SWITCH:
            self.consumeToken()
            self.decompiler.addToken(Token.SWITCH)
            lineno = self.ts.getLineno()
            self.mustMatchToken(Token.LP, "msg.no.paren.switch")
            self.decompiler.addToken(Token.LP)
            pn = self.enterSwitch(self.expr(False), lineno)
            try:
                self.mustMatchToken(Token.RP, "msg.no.paren.after.switch")
                self.decompiler.addToken(Token.RP)
                self.mustMatchToken(Token.LC, "msg.no.brace.switch")
                self.decompiler.addEOL(Token.LC)
                hasDefault = False
                
                # switchLoop:
                while True:
                    tt = self.nextToken()
                    caseExpression = None
                    if tt == Token.RC:
                        break
                    elif tt == Token.CASE:
                        self.decompiler.addToken(Token.CASE)
                        caseExpression = self.expr(False)
                        self.mustMatchToken(Token.COLON, "msg.no.colon.case")
                        self.decompiler.addEOL(Token.COLON);
                    elif tt == Token.DEFAULT:
                        if hasDefault:
                            self.reportError("msg.double.switch.default")
                        self.decompiler.addToken(Token.DEFAULT)
                        hasDefault = True
                        caseExpression = None
                        self.mustMatchToken(Token.COLON, "msg.no.colon.case")
                        self.decompiler.addEOL(Token.COLON)
                    else:
                        self.reportError("msg.bad.switch")
                        break
                    
                    block = self.nf.createLeaf(Token.BLOCK)
                    
                    tt = self.peekToken()
                    while tt not in (Token.RC, 
                                     Token.CASE, 
                                     Token.DEFAULT, 
                                     Token.EOF):
                        self.nf.addChildToBack(block, self.statement())
                        tt = self.peekToken()
                    
                    self.nf.addSwitchCase(pn, caseExpression, block);
                """
                switchLoop: while (true) {
                    tt = nextToken();
                    Node caseExpression;
                    switch (tt) {
                      case Token.RC:
                        break switchLoop;

                      case Token.CASE:
                        decompiler.addToken(Token.CASE);
                        caseExpression = expr(false);
                        mustMatchToken(Token.COLON, "msg.no.colon.case");
                        decompiler.addEOL(Token.COLON);
                        break;

                      case Token.DEFAULT:
                        if (hasDefault) {
                            reportError("msg.double.switch.default");
                        }
                        decompiler.addToken(Token.DEFAULT);
                        hasDefault = true;
                        caseExpression = null;
                        mustMatchToken(Token.COLON, "msg.no.colon.case");
                        decompiler.addEOL(Token.COLON);
                        break;

                      default:
                        reportError("msg.bad.switch");
                        break switchLoop;
                    }
                    

                    Node block = nf.createLeaf(Token.BLOCK);
                    while ((tt = peekToken()) != Token.RC
                           && tt != Token.CASE
                           && tt != Token.DEFAULT
                           && tt != Token.EOF)
                    {
                        nf.addChildToBack(block, statement());
                    }

                    // caseExpression == null => add default lable
                    nf.addSwitchCase(pn, caseExpression, block);
                }
                """
                self.decompiler.addEOL(Token.RC)
                self.nf.closeSwitch(pn)
            except:
                raise
                #pass
            finally:
                self.exitSwitch()
            return pn
        elif tt == Token.WHILE:
            self.consumeToken()
            self.decompiler.addToken(Token.WHILE)
            loop = self.enterLoop(statementLabel)
            try:
                cond = self.condition()
                self.decompiler.addEOL(Token.LC)
                body = self.statement()
                self.decompiler.addEOL(Token.RC)
                pn = self.nf.createWhile(loop, cond, body)
            except:
                pass
            finally:
                self.exitLoop()
            return pn
        elif tt == Token.DO:
            self.consumeToken()
            self.decompiler.addToken(Token.DO)
            self.decompiler.addEOL(Token.LC)
            loop = self.enterLoop(statementLabel)
            try:
                body = self.statement()
                self.decompiler.addToken(Token.RC)
                self.mustMatchToken(Token.WHILE, "msg.no.while.do")
                self.decompiler.addToken(Token.WHILE)
                cond = self.condition()
                pn = self.nf.createDoWhile(loop, body, cond)
            except:
                pass
            finally:
                self.exitLoop()
            self.matchToken(Token.SEMI)
            self.decompiler.addEOL(Token.SEMI)
            return pn
        elif tt == Token.FOR:
            self.consumeToken()
            isForEach = False
            self.decompiler.addToken(Token.FOR)
            loop = self.enterLoop(statementLabel)
            try:
                init = None#Node()
                cond = None#Node()
                incr = None
                body = None#Node()
                if self.matchToken(Token.NAME):
                    self.decompiler.addName(self.ts.getString())
                    if self.ts.getString() == "each":
                        isForEach = True
                    else:
                        self.reportError("msg.no.paren.for")
                self.mustMatchToken(Token.LP, "msg.no.paren.for")
                self.decompiler.addToken(Token.LP)
                tt = self.peekToken()
                if (tt == Token.SEMI):
                    init = self.nf.createLeaf(Token.EMPTY)
                else:
                    if (tt == Token.VAR):
                        # set init to a var list or initial
                        self.consumeToken() # consume the 'var' token
                        init = self.variables(Token.FOR)
                    else:
                        init = self.expr(True)
                        
                if self.matchToken(Token.IN):
                    self.decompiler.addToken(Token.IN)
                    #'cond' is the object over which we're iterating
                    cond = self.expr(False)
                else: #ordinary for loop
                    self.mustMatchToken(Token.SEMI, "msg.no.semi.for")
                    self.decompiler.addToken(Token.SEMI)
                    if (self.peekToken() == Token.SEMI):
                        # no loop condition
                        cond = self.nf.createLeaf(Token.EMPTY)
                    else:
                        cond = self.expr(False)
                    self.mustMatchToken(Token.SEMI, "msg.no.semi.for.cond")
                    self.decompiler.addToken(Token.SEMI)
                    if (self.peekToken() == Token.RP):
                        incr = self.nf.createLeaf(Token.EMPTY)
                    else:
                        incr = self.expr(False)
                self.mustMatchToken(Token.RP, "msg.no.paren.for.ctrl")
                self.decompiler.addToken(Token.RP)
                self.decompiler.addEOL(Token.LC)
                body = self.statement()
                self.decompiler.addEOL(Token.RC)
                if incr is None:
                    pn = self.nf.createForIn(loop, init, cond, body, isForEach)
                else:
                    pn = self.nf.createFor(loop, init, cond, incr, body)
            except:
                raise
                pass
            finally:
                self.exitLoop()
            return pn
        elif tt == Token.TRY:
            self.consumeToken()
            lineno = self.ts.getLineno()
            tryblock = None#Node()
            catchblocks = None
            finallyblock = None
            self.decompiler.addToken(Token.TRY)
            self.decompiler.addEOL(Token.LC)
            tryblock = self.statement()
            self.decompiler.addEOL(Token.RC)
            catchblocks = self.nf.createLeaf(Token.BLOCK)
            sawDefaultCatch = False
            peek = self.peekToken()
            if (peek == Token.CATCH):
                while self.matchToken(Token.CATCH):
                    if sawDefaultCatch:
                        reportError("msg.catch.unreachable")
                    self.decompiler.addToken(Token.CATCH)
                    self.mustMatchToken(Token.LP, "msg.no.paren.catch")
                    self.decompiler.addToken(Token.LP)
                    self.mustMatchToken(Token.NAME, "msg.bad.catchcond")
                    varName = self.ts.getString()
                    self.decompiler.addName(varName)
                    catchCond = None
                    if self.matchToken(Token.IF):
                        self.decompiler.addToken(Token.IF)
                        catchCond = self.expr(False)
                    else:
                        sawDefaultCatch = True
                    self.mustMatchToken(Token.RP, "msg.bad.catchcond")
                    self.decompiler.addToken(Token.RP)
                    self.mustMatchToken(Token.LC, "msg.no.brace.catchblock")
                    self.decompiler.addEOL(Token.LC)
                    self.nf.addChildToBack(catchblocks, self.nf.createCatch(varName, 
                                catchCond, self.statements(), self.ts.getLineno()))
                    self.mustMatchToken(Token.RC, "msg.no.brace.after.body")
                    self.decompiler.addEOL(Token.RC)
            else:
                if (peek != Token.FINALLY):
                    self.mustMatchToken(Token.FINALLY, "msg.try.no.catchfinally")
            if self.matchToken(Token.FINALLY):
                self.decompiler.addToken(Token.FINALLY)
                self.decompiler.addEOL(Token.LC)
                finallyblock = self.statement()
                self.decompiler.addEOL(Token.RC)
            pn = self.nf.createTryCatchFinally(tryblock, catchblocks, finallyblock, lineno)
            return pn
        elif tt == Token.THROW:
            self.consumeToken()
            if (self.peekTokenOrEOL() == Token.EOL):
                reportError("msg.bad.throw.eol")
            lineno = self.ts.getLineno()
            self.decompiler.addToken(Token.THROW)
            pn = self.nf.createThrow(self.expr(False), lineno)
        elif tt == Token.BREAK:
            self.consumeToken()
            lineno = self.ts.getLineno()
            self.decompiler.addToken(Token.BREAK)
            breakStatement = self.matchJumpLabelName()
            if breakStatement is None:
                if self.loopAndSwitchSet is None or (len(self.loopAndSwitchSet) == 0):
                    self.reportError("msg.bad.break")
                    return
                breakStatement = self.loopAndSwitchSet[-1]
            pn = self.nf.createBreak(breakStatement, lineno)
        elif tt == Token.CONTINUE:
            self.consumeToken()
            lineno = self.ts.getLineno()
            self.decompiler.addToken(Token.CONTINUE)
            loop = None#Node()
            label = self.matchJumpLabelName()
            if label is None:
                if self.loopSet is None or (len(self.loopSet) == 0):
                    reportError("msg.continue.outside")
                    return
                loop = self.loopSet[-1]
            else:
                loop = self.getLabelLoop(label)
                if loop is None:
                    reportError("msg.continue.nonloop")
                    return
            pn = self.nf.createContinue(loop, lineno)
        elif tt == Token.WITH:
            self.consumeToken()
            self.decompiler.addToken(Token.WITH)
            lineno = self.ts.getLineno()
            self.mustMatchToken(Token.LP, "msg.no.paren.with")
            self.decompiler.addToken(Token.LP)
            obj = self.expr(False)
            self.mustMatchToken(Token.RP, "msg.no.paren.after.with")
            self.decompiler.addToken(Token.RP)
            self.decompiler.addEOL(Token.LC)
            self.nestingOfWith += 1
            body = None#Node()
            try:
                body = self.statement()
            except:
                pass
            finally:
                self.nestingOfWith -= 1
            self.decompiler.addEOL(Token.RC)
            pn = self.nf.createWith(obj, body, lineno)
            return pn
        elif tt in (Token.CONST,
                   Token.VAR):
            self.consumeToken()
            pn = self.variables(tt)
        elif tt == Token.RETURN:
            if not self.insideFunction():
                self.reportError("msg.bad.return")
            self.consumeToken()
            self.decompiler.addToken(Token.RETURN)
            lineno = self.ts.getLineno()
            retExpr = None#Node()
            tt = self.peekTokenOrEOL()
            if tt in (Token.SEMI,
                      Token.RC,
                      Token.EOF,
                      Token.EOL, 
                      Token.ERROR):
                retExpr = None
            else:
                retExpr = self.expr(False)
                hasReturnValue = True
            pn = self.nf.createReturn(retExpr, lineno)
            if retExpr is None:
                if (self.functionEndFlags == Node.END_RETURNS_VALUE):
                    self.addStrictWarning("msg.return.inconsistent", "")
                self.functionEndFlags |= Node.END_RETURNS
            else:
                if (self.functionEndFlags == Node.END_RETURNS):
                    self.addStrictWarning("msg.return.inconsistent", "")
                self.functionEndFlags |= Node.END_RETURNS_VALUE
        elif tt == Token.LC:
            self.consumeToken()
            if statementLabel is not None:
                self.decompiler.addToken(Token.LC)
            pn = self.statements()
            self.mustMatchToken(Token.RC, "msg.no.brace.block")
            if statementLabel is not None:
                self.decompiler.addEOL(Token.RC)
            return pn
        elif tt == Token.SEMI:
            self.consumeToken()
            pn = self.nf.createLeaf(Token.EMPTY)
            return pn
        elif tt == Token.FUNCTION:
            self.consumeToken()
            pn = self.function(FunctionNode.FUNCTION_EXPRESSION_STATEMENT)
            return pn
        elif tt == Token.DEFAULT:
            self.consumeToken()
            self.mustHaveXML()
            self.decompiler.addToken(Token.DEFAULT)
            nsLine = self.ts.getLineno()
            if not matchToken(Token.NAME) and self.ts.getString() == "xml":
                self.reportError("msg.bad.namespace")
            self.decompiler.addName(" xml")
            if not matchToken(Token.NAME) and self.ts.getString() == "namespace":
                self.reportError("msg.bad.namespace")
            self.decompiler.addName(" namespace")
            if not matchToken(Token.ASSIGN):
                reportError("msg.bad.namespace")
            decompiler.addToken(Token.ASSIGN)
            expr = self.expr(False)
            pn = nf.createDefaultNamespace(expr, nsLine)
        elif tt == Token.NAME:
            lineno = self.ts.getLineno()
            name = self.ts.getString()
            self.setCheckForLabel()
            pn = self.expr(False)
            if (pn.getType() != Token.LABEL):
                pn = self.nf.createExprStatement(pn, lineno)
            else:
                if (self.peekToken() != Token.COLON):
                    Kit.codeBug()
                self.consumeToken()
                self.decompiler.addName(name)
                self.decompiler.addEOL(Token.COLON)
                if self.labelSet is None:
                    self.labelSet = Hashtable()
                else:
                    if self.labelSet.get(name) is not None:
                        reportError("msg.dup.label")
                firstLabel = bool()
                if statementLabel is None:
                    firstLabel = True
                    statementLabel = pn
                else:
                    firstLabel = False
                self.labelSet[name]=statementLabel
                try:
                    pn = self.statementHelper(statementLabel)
                except:
                    pass
                finally:
                    del self.labelSet[name]
                if firstLabel:
                    pn = self.nf.createLabeledStatement(statementLabel, pn)
                return pn
        else:
            lineno = self.ts.getLineno()
            pn = self.expr(False)
            pn = self.nf.createExprStatement(pn, lineno)
        ttFlagged = self.peekFlaggedToken()
        if (ttFlagged & self.CLEAR_TI_MASK) == Token.SEMI:
            self.consumeToken()
        elif (ttFlagged & self.CLEAR_TI_MASK) in (Token.RC, 
                                                  Token.EOF, 
                                                  Token.ERROR):
            pass
        else:
            if ((ttFlagged & self.TI_AFTER_EOL) == 0):
                self.reportError("msg.no.semi.stmt")
        self.decompiler.addEOL(Token.SEMI)
        return pn

    def statements(self):
        pn = self.nf.createBlock(self.ts.getLineno())
        tt = 0
        tt = self.peekToken()
        while tt > Token.EOF and (tt != Token.RC):
            self.nf.addChildToBack(pn, self.statement())
            tt = self.peekToken()
        return pn

    def condition(self):
        self.mustMatchToken(Token.LP, "msg.no.paren.cond")
        self.decompiler.addToken(Token.LP)
        pn = self.expr(False)
        self.mustMatchToken(Token.RP, "msg.no.paren.after.cond")
        self.decompiler.addToken(Token.RP)
        if pn.getProp(Node.PARENTHESIZED_PROP) is None and \
                    (pn.getType() == Token.SETNAME) or \
                    (pn.getType() == Token.SETPROP) or \
                    (pn.getType() == Token.SETELEM):
            self.addStrictWarning("msg.equal.as.assign", "")
        return pn

    def matchJumpLabelName(self):
        label = None
        tt = self.peekTokenOrEOL()
        if (tt == Token.NAME):
            self.consumeToken()
            name = self.ts.getString()
            self.decompiler.addName(name)
            if self.labelSet is not None:
                label = self.labelSet[name]
            if label is None:
                self.reportError("msg.undef.label")
        return label

    def variables(self, context):
        """
         /**
         * Parse a 'var' or 'const' statement, or a 'var' init list in a for
         * statement.
         * @param context A token value: either VAR, CONST or FOR depending on
         * context.
         * @return The parsed statement
         * @throws IOException
         * @throws ParserException
         */
        """
        pn = None #Node()
        first = True
        if (context == Token.CONST):
            pn = self.nf.createVariables(Token.CONST, self.ts.getLineno())
            self.decompiler.addToken(Token.CONST)
        else:
            pn = self.nf.createVariables(Token.VAR, self.ts.getLineno())
            self.decompiler.addToken(Token.VAR)
        while True:
            name = None#Node()
            init = None#Node()
            self.mustMatchToken(Token.NAME, "msg.bad.var")
            s = self.ts.getString()
            if not first:
                self.decompiler.addToken(Token.COMMA)
            first = False
            self.decompiler.addName(s)
            if (context == Token.CONST):
                if not self.currentScriptOrFn.addConst(s):
                    if (self.currentScriptOrFn.addVar(s) != ScriptOrFnNode.DUPLICATE_CONST):
                        self.addError("msg.var.redecl", s)
                    else:
                        self.addError("msg.const.redecl", s)
            else:
                dupState = self.currentScriptOrFn.addVar(s)
                if (dupState == ScriptOrFnNode.DUPLICATE_CONST):
                    self.addError("msg.const.redecl", s)
                else:
                    if (dupState == ScriptOrFnNode.DUPLICATE_PARAMETER):
                        self.addStrictWarning("msg.var.hides.arg", s)
                    else:
                        if (dupState == ScriptOrFnNode.DUPLICATE_VAR):
                            self.addStrictWarning("msg.var.redecl", s)
            name = self.nf.createName(s)
            if self.matchToken(Token.ASSIGN):
                self.decompiler.addToken(Token.ASSIGN)
                init = self.assignExpr((context == Token.FOR))
                self.nf.addChildToBack(name, init)
            self.nf.addChildToBack(pn, name)
            if not self.matchToken(Token.COMMA):
                break
        return pn
        
    def assignExpr(self, inForInit):
        pn = self.condExpr(inForInit)

        tt = self.peekToken();
        if (Token.FIRST_ASSIGN <= tt <= Token.LAST_ASSIGN):
            self.consumeToken();
            self.decompiler.addToken(tt);
            pn = self.nf.createAssignment(tt, pn, self.assignExpr(inForInit));
        return pn;

    def expr(self, inForInit):
        pn = self.assignExpr(inForInit)
        while self.matchToken(Token.COMMA):
            self.decompiler.addToken(Token.COMMA)
            if self.compilerEnv.isStrictMode() and not pn.hasSideEffects():
                self.addStrictWarning("msg.no.side.effects", "")
            pn = self.nf.createBinary(Token.COMMA, pn, self.assignExpr(inForInit))
        return pn
        

    def condExpr(self, inForInit):
        pn = self.orExpr(inForInit)
        if self.matchToken(Token.HOOK):
            self.decompiler.addToken(Token.HOOK)
            ifTrue = self.assignExpr(False)
            self.mustMatchToken(Token.COLON, "msg.no.colon.cond")
            self.decompiler.addToken(Token.COLON)
            ifFalse = self.assignExpr(inForInit)
            return self.nf.createCondExpr(pn, ifTrue, ifFalse)
        return pn

    def orExpr(self, inForInit):
        pn = self.andExpr(inForInit)
        if self.matchToken(Token.OR):
            self.decompiler.addToken(Token.OR)
            pn = self.nf.createBinary(Token.OR, pn, self.orExpr(inForInit))
        return pn

    def andExpr(self, inForInit):
        pn = self.bitOrExpr(inForInit)
        if self.matchToken(Token.AND):
            self.decompiler.addToken(Token.AND)
            pn = self.nf.createBinary(Token.AND, pn, self.andExpr(inForInit))
        return pn

    def bitOrExpr(self, inForInit):
        pn = self.bitXorExpr(inForInit)
        while self.matchToken(Token.BITOR):
            self.decompiler.addToken(Token.BITOR)
            pn = self.nf.createBinary(Token.BITOR, pn, self.bitXorExpr(inForInit))
        return pn

    def bitXorExpr(self, inForInit):
        pn = self.bitAndExpr(inForInit)
        while self.matchToken(Token.BITXOR):
            self.decompiler.addToken(Token.BITXOR)
            pn = self.nf.createBinary(Token.BITXOR, pn, self.bitAndExpr(inForInit))
        return pn

    def bitAndExpr(self, inForInit):
        pn = self.eqExpr(inForInit)
        while self.matchToken(Token.BITAND):
            self.decompiler.addToken(Token.BITAND)
            pn = self.nf.createBinary(Token.BITAND, pn, self.eqExpr(inForInit))
        return pn

    def eqExpr(self, inForInit):
        pn = self.relExpr(inForInit)
        while True:
            tt = self.peekToken()
            if tt in (Token.SHNE, 
                      Token.SHEQ, 
                      Token.NE, 
                      Token.EQ):
                self.consumeToken()
                decompilerToken = tt
                parseToken = tt
                if (self.compilerEnv.getLanguageVersion() == Context.VERSION_1_2):
                    """
                    // JavaScript 1.2 uses shallow equality for == and != .
                    // In addition, convert === and !== for decompiler into
                    // == and != since the decompiler is supposed to show
                    // canonical source and in 1.2 ===, !== are allowed
                    // only as an alias to ==, !=.
                    """
                    if tt == Token.EQ:
                        parseToken = Token.SHEQ
                    elif tt == Token.NE:
                        parseToken = Token.SHNE
                    elif tt == Token.SHEQ:
                        decompilerToken = Token.EQ
                    elif tt == Token.SHNE:
                        decompilerToken = Token.NE
                self.decompiler.addToken(decompilerToken)
                pn = self.nf.createBinary(parseToken, pn, self.relExpr(inForInit))
                continue
            break
        return pn

    def relExpr(self, inForInit):
        pn = self.shiftExpr()
        while True:
            tt = self.peekToken()
            if tt == Token.IN and inForInit:
                pass
            elif tt in (Token.INSTANCEOF, 
                         Token.LE, 
                         Token.LT, \
                         Token.GE, 
                         Token.GT,
                         Token.IN):
                self.consumeToken()
                self.decompiler.addToken(tt)
                pn = self.nf.createBinary(tt, pn, self.shiftExpr())
                continue
            break
        return pn

    def shiftExpr(self):
        pn = self.addExpr()
        while True:
            tt = self.peekToken()
            if tt in (Token.LSH, 
                      Token.URSH, 
                      Token.RSH):
                self.consumeToken()
                self.decompiler.addToken(tt)
                pn = self.nf.createBinary(tt, pn, self.addExpr())
                continue
            break
        return pn

    def addExpr(self):
        pn = self.mulExpr()
        while True:
            tt = self.peekToken()
            if (tt == Token.ADD) or (tt == Token.SUB):
                self.consumeToken()
                self.decompiler.addToken(tt)
                pn = self.nf.createBinary(tt, pn, self.mulExpr())
                continue
            break
        return pn

    def mulExpr(self):
        pn = self.unaryExpr()
        while True:
            tt = self.peekToken()
            if tt in (Token.MUL, 
                      Token.DIV, 
                      Token.MOD):
                self.consumeToken()
                self.decompiler.addToken(tt)
                pn = self.nf.createBinary(tt, pn, self.unaryExpr())
                continue
            break
        return pn

    def unaryExpr(self):
        tt = 0
        tt = self.peekToken()
        if tt in (Token.VOID, 
                  Token.NOT, 
                  Token.BITNOT,
                  Token.TYPEOF):
            self.consumeToken()
            self.decompiler.addToken(tt)
            return self.nf.createUnary(tt, self.unaryExpr())
        elif tt == Token.ADD:
            self.consumeToken()
            self.decompiler.addToken(Token.POS)
            return self.nf.createUnary(Token.POS, self.unaryExpr())
        elif tt == Token.SUB:
            self.consumeToken()
            self.decompiler.addToken(Token.NEG)
            return self.nf.createUnary(Token.NEG, self.unaryExpr())
        elif tt == Token.DEC or tt == Token.INC:
            self.consumeToken()
            self.decompiler.addToken(tt)
            return self.nf.createIncDec(tt, False, self.memberExpr(True))
        elif tt == Token.DELPROP:
            self.consumeToken()
            self.decompiler.addToken(Token.DELPROP)
            return self.nf.createUnary(Token.DELPROP, self.unaryExpr())
        elif tt == Token.ERROR:
            self.consumeToken()
            
        #// XML stream encountered in expression.
        elif tt == Token.LT and self.compilerEnv.isXmlAvailable():
            self.consumeToken()
            pn = self.xmlInitializer()
            return memberExprTail(True, pn)
            #else Fall thru to the default handling of RELOP
        else:
            pn = self.memberExpr(True)
            tt = self.peekTokenOrEOL()
            if (tt == Token.INC) or (tt == Token.DEC):
                self.consumeToken()
                self.decompiler.addToken(tt)
                return self.nf.createIncDec(tt, True, pn)
            return pn
        return self.nf.createName("err")

    def xmlInitializer(self):
        tt = self.ts.getFirstXMLToken()
        if (tt != Token.XML) and (tt != Token.XMLEND):
            self.reportError("msg.syntax")
            return
        pnXML = self.nf.createLeaf(Token.NEW)
        xml = self.ts.getString()
        fAnonymous = xml.trim().startsWith("<>")
        pn = self.nf.createName("XMLList" if fAnonymous else "XML")
        self.nf.addChildToBack(pnXML, pn)
        pn = None
        self.expr = None#Node()
        while True:
            if tt == Token.XML:
                xml = self.ts.getString()
                self.decompiler.addName(xml)
                self.mustMatchToken(Token.LC, "msg.syntax")
                self.decompiler.addToken(Token.LC)
                self.expr = self.nf.createString("") if (self.peekToken() == Token.RC) else self.expr(False)
                self.mustMatchToken(Token.RC, "msg.syntax")
                self.decompiler.addToken(Token.RC)
                if pn is None:
                    pn = self.nf.createString(xml)
                else:
                    pn = self.nf.createBinary(Token.ADD, pn, self.nf.createString(xml))
                if self.ts.isXMLAttribute():
                    self.expr = self.nf.createUnary(Token.ESCXMLATTR, self.expr)
                    prepend = self.nf.createBinary(Token.ADD, self.nf.createString("\""), self.expr)
                    self.expr = self.nf.createBinary(Token.ADD, prepend, self.nf.createString("\""))
                else:
                    self.expr = self.nf.createUnary(Token.ESCXMLTEXT, self.expr)
                pn = self.nf.createBinary(Token.ADD, pn, self.expr)

            elif tt == Token.XMLEND:
                xml = self.ts.getString()
                self.decompiler.addName(xml)
                if pn is None:
                    pn = self.nf.createString(xml)
                else:
                    pn = self.nf.createBinary(Token.ADD, pn, self.nf.createString(xml))
                self.nf.addChildToBack(pnXML, pn)
                return pnXML
            else:
                self.reportError("msg.syntax")
                return
            tt = self.ts.getNextXMLToken()

    def argumentList(self, listNode):
        matched = bool()
        matched = self.matchToken(Token.RP)
        if not matched:
            first = True
            while first or self.matchToken(Token.COMMA):
                if not first:
                    self.decompiler.addToken(Token.COMMA)
                first = False
                self.nf.addChildToBack(listNode, self.assignExpr(False))
            self.mustMatchToken(Token.RP, "msg.no.paren.arg")
        self.decompiler.addToken(Token.RP)

    def memberExpr(self, allowCallSyntax):
        tt = 0
        pn = None#Node()
        tt = self.peekToken()
        if (tt == Token.NEW):
            self.consumeToken()
            self.decompiler.addToken(Token.NEW)
            pn = self.nf.createCallOrNew(Token.NEW, self.memberExpr(False))
            if self.matchToken(Token.LP):
                self.decompiler.addToken(Token.LP)
                self.argumentList(pn)
            tt = self.peekToken()
            if (tt == Token.LC):
                self.nf.addChildToBack(pn, self.primaryExpr())
        else:
            pn = self.primaryExpr()
        return self.memberExprTail(allowCallSyntax, pn)
      
    def memberExprTail(self, allowCallSyntax, pn):
        while True:
            tt = self.peekToken()
            if tt in (Token.DOT, 
                      Token.DOTDOT):
                memberTypeFlags = 0
                s = ""
                self.consumeToken()
                self.decompiler.addToken(tt)
                if tt == Token.DOTDOT:
                    self.mustHaveXML()
                    memberTypeFlags = Node.DESCENDANTS_FLAG
                    
                if not self.compilerEnv.isXmlAvailable():
                    self.mustMatchToken(Token.NAME, "msg.no.name.after.dot")
                    s = self.ts.getString()
                    self.decompiler.addName(s)
                    pn = self.nf.createPropertyGet(pb, None, s, memberTypeFlags)
                else:
                    tt = self.nextToken()
                    if tt == Token.NAME:
                        # handles: name, ns::name, ns::*, ns::[expr]
                        s = self.ts.getString()
                        self.decompiler.addName(s)
                        pn = self.propertyName(pn, s, memberTypeFlags)
                    elif tt == Token.MUL:
                        # handles: *, *::name, *::*, *::[expr]
                        self.decompiler.addName("*")
                        pn = self.propertyName(pn, s, memberTypeFlags)
                    elif tt == Token.XMLATTR:
                        # handles: '@attr', '@ns::attr', '@ns::*', '@ns::*',
                        #          '@::attr', '@::*', '@*', '@*::attr', '@*::*'
                        self.decompiler.addToken(Token.XMLATTR)
                        pn = self.attributeAccess(pn, memberTypeFlags)
                    else:
                        reportError("msg.no.name.after.dot")
                
            elif tt == Token.DOTQUERY:
                self.consumeToken();
                self.mustHaveXML();
                self.decompiler.addToken(Token.DOTQUERY);
                pn = self.nf.createDotQuery(pn, self.expr(False), 
                                            self.ts.getLineno());
                self.mustMatchToken(Token.RP, "msg.no.paren");
                self.decompiler.addToken(Token.RP);

            elif tt == Token.LB:
                self.consumeToken();
                self.decompiler.addToken(Token.LB);
                pn = self.nf.createElementGet(pn, None, self.expr(False), 0);
                self.mustMatchToken(Token.RB, "msg.no.bracket.index");
                self.decompiler.addToken(Token.RB);
            elif tt == Token.LP:
                if not allowCallSyntax:
                    break
                self.consumeToken();
                self.decompiler.addToken(Token.LP);
                pn = self.nf.createCallOrNew(Token.CALL, pn);
                #/* Add the arguments to pn, if any are supplied. */
                self.argumentList(pn);
            else:
                break
        return pn
            
        """
    private Node memberExprTail(boolean allowCallSyntax, Node pn)
        throws IOException, ParserException
    {
      tailLoop:
        while (true) {
            int tt = peekToken();
            switch (tt) {

              case Token.DOT:
              case Token.DOTDOT:
                {
                    int memberTypeFlags;
                    String s;

                    consumeToken();
                    decompiler.addToken(tt);
                    memberTypeFlags = 0;
                    if (tt == Token.DOTDOT) {
                        mustHaveXML();
                        memberTypeFlags = Node.DESCENDANTS_FLAG;
                    }
                    if (!compilerEnv.isXmlAvailable()) {
                        mustMatchToken(Token.NAME, "msg.no.name.after.dot");
                        s = ts.getString();
                        decompiler.addName(s);
                        pn = nf.createPropertyGet(pn, null, s, memberTypeFlags);
                        break;
                    }

                    tt = nextToken();
                    switch (tt) {
                      // handles: name, ns::name, ns::*, ns::[expr]
                      case Token.NAME:
                        s = ts.getString();
                        decompiler.addName(s);
                        pn = propertyName(pn, s, memberTypeFlags);
                        break;

                      // handles: *, *::name, *::*, *::[expr]
                      case Token.MUL:
                        decompiler.addName("*");
                        pn = propertyName(pn, "*", memberTypeFlags);
                        break;

                      // handles: '@attr', '@ns::attr', '@ns::*', '@ns::*',
                      //          '@::attr', '@::*', '@*', '@*::attr', '@*::*'
                      case Token.XMLATTR:
                        decompiler.addToken(Token.XMLATTR);
                        pn = attributeAccess(pn, memberTypeFlags);
                        break;

                      default:
                        reportError("msg.no.name.after.dot");
                    }
                }
                break;

              case Token.DOTQUERY:
                consumeToken();
                mustHaveXML();
                decompiler.addToken(Token.DOTQUERY);
                pn = nf.createDotQuery(pn, expr(false), ts.getLineno());
                mustMatchToken(Token.RP, "msg.no.paren");
                decompiler.addToken(Token.RP);
                break;

              case Token.LB:
                consumeToken();
                decompiler.addToken(Token.LB);
                pn = nf.createElementGet(pn, null, expr(false), 0);
                mustMatchToken(Token.RB, "msg.no.bracket.index");
                decompiler.addToken(Token.RB);
                break;

              case Token.LP:
                if (!allowCallSyntax) {
                    break tailLoop;
                }
                consumeToken();
                decompiler.addToken(Token.LP);
                pn = nf.createCallOrNew(Token.CALL, pn);
                /* Add the arguments to pn, if any are supplied. */
                argumentList(pn);
                break;

              default:
                break tailLoop;
            }
        }
        return pn;
    }"""

    def attributeAccess(self, pn, memberTypeFlags):
        memberTypeFlags |= Node.ATTRIBUTE_FLAG
        tt = self.nextToken()
        if tt == Token.NAME:
            s = self.ts.getString()
            self.decompiler.addName(s)
            pn = self.propertyName(pn, s, memberTypeFlags)
        elif tt == Token.MUL:
            self.decompiler.addName("*")
            pn = self.propertyName(pn, "*", memberTypeFlags)
        elif tt == Token.LB:
            self.decompiler.addToken(Token.LB)
            pn = self.nf.createElementGet(pn, None, self.expr(False), memberTypeFlags)
            self.mustMatchToken(Token.RB, "msg.no.bracket.index")
            self.decompiler.addToken(Token.RB)
        else:
            self.reportError("msg.no.name.after.xmlAttr")
            pn = self.nf.createPropertyGet(pn, None, "?", memberTypeFlags)
        return pn

    def propertyName(self, pn, name, memberTypeFlags):
        namespace = None
        if self.matchToken(Token.COLONCOLON):
            self.decompiler.addToken(Token.COLONCOLON)
            namespace = name
            tt = self.nextToken()
            if tt == Token.NAME:
                name = self.ts.getString()
                self.decompiler.addName(name)
            elif tt == Token.MUL:
                self.decompiler.addName("*")
                name = "*"
            elif tt == Token.LB:
                self.decompiler.addToken(Token.LB)
                pn = self.nf.createElementGet(pn, namespace, self.expr(False), memberTypeFlags)
                self.mustMatchToken(Token.RB, "msg.no.bracket.index")
                self.decompiler.addToken(Token.RB)
                return pn
            else:
                self.reportError("msg.no.name.after.coloncolon")
                name = "?"
        pn = self.nf.createPropertyGet(pn, namespace, name, memberTypeFlags)
        return pn

    def plainProperty(self, elems, prop):
        self.mustMatchToken(Token.COLON, "msg.no.colon.prop")
        self.decompiler.addToken(Token.OBJECTLIT)
        elems.append(prop)
        elems.append(self.assignExpr(False))

    def getterSetterProperty(self, elems, property, isGetter):
        f = self.function(FunctionNode.FUNCTION_EXPRESSION)
        if (f.getType() != Token.FUNCTION):
            self.reportError("msg.bad.prop")
            return False
        fnIndex = f.getExistingIntProp(Node.FUNCTION_PROP)
        fn = self.currentScriptOrFn.getFunctionNode(fnIndex)
        if len((fn.getFunctionName()) != 0):
            self.reportError("msg.bad.prop")
            return False
        elems.add(property)
        if isGetter:
            elems.add(self.nf.createUnary(Token.GET, f))
        else:
            elems.add(self.nf.createUnary(Token.SET, f))
        return True
        
        
    def primaryExpr(self):
        ttFlagged = self.nextFlaggedToken()
        tt = ttFlagged & self.CLEAR_TI_MASK
        
        """Is it worth creating a jump dict for this?"""
        if tt == Token.FUNCTION:
            return self.function(FunctionNode.FUNCTION_EXPRESSION)
        elif tt == Token.LB:
            elems = []
            skipCount = 0
            self.decompiler.addToken(Token.LB)
            after_lb_or_comma = True
            while True:
                tt = self.peekToken()
                if tt == Token.COMMA:
                    self.consumeToken()
                    self.decompiler.addToken(Token.COMMA)
                    if (not after_lb_or_comma):
                        after_lb_or_comma = True
                    else:
                        elems.append(None)
                        skipCount += 1
                elif tt == Token.RB:
                    self.consumeToken()
                    self.decompiler.addToken(Token.RB)
                    break
                else:
                    if (not after_lb_or_comma):
                        self.reportError("msg.no.bracket.arg")
                    elems.append(self.assignExpr(False))
                    after_lb_or_comma = False
            return self.nf.createArrayLiteral(elems, skipCount)
            
        elif tt == Token.LC:
            elems = [];
            self.decompiler.addToken(Token.LC);
            if (not self.matchToken(Token.RC)):
                first = True;
                while True:
                    prop = None

                    if (not first):
                        self.decompiler.addToken(Token.COMMA);
                    else:
                        first = False

                    tt = self.peekToken();
                    if tt in (Token.NAME, 
                              Token.STRING):
                        self.consumeToken();
                        #// map NAMEs to STRINGs in object literal context
                        #// but tell the decompiler the proper type
                        s = self.ts.getString();
                        if (tt == Token.NAME):
                            if (s == "get" and \
                                self.peekToken() == Token.NAME):
                                self.decompiler.addToken(Token.GET);
                                self.consumeToken();
                                s = self.ts.getString();
                                self.decompiler.addName(s);
                                prop = ScriptRuntime.getIndexObject(s);
                                if ( not self.getterSetterProperty(elems, \
                                            prop, True)):
                                    break
                            elif (s == "set" and \
                                       self.peekToken() == Token.NAME):
                                self.decompiler.addToken(Token.SET);
                                self.consumeToken();
                                self.s = self.ts.getString();
                                self.decompiler.addName(s);
                                prop = ScriptRuntime.getIndexObject(s);
                                if (not self.getterSetterProperty(elems, \
                                            prop, False)):
                                    break
                            else:
                                self.decompiler.addName(s);
                                prop = ScriptRuntime.getIndexObject(s)
                                self.plainProperty(elems, prop)
                        else:
                            self.decompiler.addString(s)
                            prop = ScriptRuntime.getIndexObject(s)
                            self.plainProperty(elems, prop)

                    elif tt == Token.NUMBER:
                        self.consumeToken();
                        n = self.ts.getNumber()
                        self.decompiler.addNumber(n)
                        prop = ScriptRuntime.getIndexObject(n)
                        self.plainProperty(elems, prop)

                    elif tt ==  Token.RC:
                        # trailing comma is OK.
                        break
                    else:
                        self.reportError("msg.bad.prop");
                        break
                        
                    if not self.matchToken(Token.COMMA):
                        # tail condition for Java do loop
                        break

                self.mustMatchToken(Token.RC, "msg.no.brace.prop");
                
            self.decompiler.addToken(Token.RC);
            return self.nf.createObjectLiteral(elems);
            
        elif tt == Token.LP:
            """
             /* Brendan's IR-jsparse.c makes a new node tagged with
             * TOK_LP here... I'm not sure I understand why.  Isn't
             * the grouping already implicit in the structure of the
             * parse tree?  also TOK_LP is already overloaded (I
             * think) in the C IR as 'function call.'  */
            """
            self.decompiler.addToken(Token.LP);
            pn = self.expr(False);
            #pn.putProp(Node.PARENTHESIZED_PROP, Boolean.TRUE);
            pn.putProp(Node.PARENTHESIZED_PROP, True);
            self.decompiler.addToken(Token.RP);
            self.mustMatchToken(Token.RP, "msg.no.paren");
            return pn;
            
        elif tt == Token.XMLATTR:
            raise NotImplementedError() # XMLAttr
        elif tt == Token.NAME:
            name = self.ts.getString()
            if (ttFlagged & self.TI_CHECK_LABEL) != 0:
                if self.peekToken() == Token.COLON:
                    # Don't consume colon, it is used as unwind indicator
                    # to recurt to statementHelper.
                    # XXX Better way?
                    return self.nf.createLabel(self.ts.getLineno());
            self.decompiler.addName(name)
            pn = None
            if (self.compilerEnv.isXmlAvailable()):
                pn = self.propertyName(None, name, 0)
            else:
                pn = self.nf.createName(name)
            return pn
            
        elif tt == Token.NUMBER:
            self.consumeToken()
            n = self.ts.getNumber()
            self.decompiler.addNumber(n)
            return self.nf.createNumber(n);
            #prop = ScriptRuntime.getIndexObject(n)
            #self.plainProperty(elems, prop)

        elif tt == Token.STRING:
            s = self.ts.getString();
            self.decompiler.addString(s);
            return self.nf.createString(s);
            
        elif tt in (Token.ASSIGN_DIV, Token.DIV):
            #// Got / or /= which should be treated as regexp in fact
            self.ts.readRegExp(tt);
            flags = self.ts.regExpFlags;
            self.ts.regExpFlags = None
            re = self.ts.getString();
            self.decompiler.addRegexp(re, flags);
            index = self.currentScriptOrFn.addRegexp(re, flags);
            return self.nf.createRegExp(index);
            
        elif tt in (Token.NULL, 
                    Token.THIS, 
                    Token.FALSE, 
                    Token.TRUE):
            self.decompiler.addToken(tt);
            return self.nf.createLeaf(tt);
            
        raise NotImplementedError() # should never reach here
        """
    private Node primaryExpr()
        throws IOException, ParserException
    {
        Node pn;

        int ttFlagged = nextFlaggedToken();
        int tt = ttFlagged & CLEAR_TI_MASK;

        switch(tt) {

          case Token.FUNCTION:
            return function(FunctionNode.FUNCTION_EXPRESSION);

          case Token.LB: {
            ObjArray elems = new ObjArray();
            int skipCount = 0;
            decompiler.addToken(Token.LB);
            boolean after_lb_or_comma = true;
            while (true) {
                tt = peekToken();

                if (tt == Token.COMMA) {
                    consumeToken();
                    decompiler.addToken(Token.COMMA);
                    if (!after_lb_or_comma) {
                        after_lb_or_comma = true;
                    } else {
                        elems.add(null);
                        ++skipCount;
                    }
                } else if (tt == Token.RB) {
                    consumeToken();
                    decompiler.addToken(Token.RB);
                    break;
                } else {
                    if (!after_lb_or_comma) {
                        reportError("msg.no.bracket.arg");
                    }
                    elems.add(assignExpr(false));
                    after_lb_or_comma = false;
                }
            }
            return nf.createArrayLiteral(elems, skipCount);
          }

          case Token.LC: {
            ObjArray elems = new ObjArray();
            decompiler.addToken(Token.LC);
            if (!matchToken(Token.RC)) {

                boolean first = true;
            commaloop:
                do {
                    Object property;

                    if (!first)
                        decompiler.addToken(Token.COMMA);
                    else
                        first = false;

                    tt = peekToken();
                    switch(tt) {
                      case Token.NAME:
                      case Token.STRING:
                        consumeToken();
                        // map NAMEs to STRINGs in object literal context
                        // but tell the decompiler the proper type
                        String s = ts.getString();
                        if (tt == Token.NAME) {
                            if (s.equals("get") &&
                                peekToken() == Token.NAME) {
                                decompiler.addToken(Token.GET);
                                consumeToken();
                                s = ts.getString();
                                decompiler.addName(s);
                                property = ScriptRuntime.getIndexObject(s);
                                if (!getterSetterProperty(elems, property,
                                                          true))
                                    break commaloop;
                                break;
                            } else if (s.equals("set") &&
                                       peekToken() == Token.NAME) {
                                decompiler.addToken(Token.SET);
                                consumeToken();
                                s = ts.getString();
                                decompiler.addName(s);
                                property = ScriptRuntime.getIndexObject(s);
                                if (!getterSetterProperty(elems, property,
                                                          false))
                                    break commaloop;
                                break;
                            }
                            decompiler.addName(s);
                        } else {
                            decompiler.addString(s);
                        }
                        property = ScriptRuntime.getIndexObject(s);
                        plainProperty(elems, property);
                        break;

                      case Token.NUMBER:
                        consumeToken();
                        double n = ts.getNumber();
                        decompiler.addNumber(n);
                        property = ScriptRuntime.getIndexObject(n);
                        plainProperty(elems, property);
                        break;

                      case Token.RC:
                        // trailing comma is OK.
                        break commaloop;
                    default:
                        reportError("msg.bad.prop");
                        break commaloop;
                    }
                } while (matchToken(Token.COMMA));

                mustMatchToken(Token.RC, "msg.no.brace.prop");
            }
            decompiler.addToken(Token.RC);
            return nf.createObjectLiteral(elems);
          }

          case Token.LP:

            /* Brendan's IR-jsparse.c makes a new node tagged with
             * TOK_LP here... I'm not sure I understand why.  Isn't
             * the grouping already implicit in the structure of the
             * parse tree?  also TOK_LP is already overloaded (I
             * think) in the C IR as 'function call.'  */
            decompiler.addToken(Token.LP);
            pn = expr(false);
            pn.putProp(Node.PARENTHESIZED_PROP, Boolean.TRUE);
            decompiler.addToken(Token.RP);
            mustMatchToken(Token.RP, "msg.no.paren");
            return pn;

          case Token.XMLATTR:
            mustHaveXML();
            decompiler.addToken(Token.XMLATTR);
            pn = attributeAccess(null, 0);
            return pn;

          case Token.NAME: {
            String name = ts.getString();
            if ((ttFlagged & TI_CHECK_LABEL) != 0) {
                if (peekToken() == Token.COLON) {
                    // Do not consume colon, it is used as unwind indicator
                    // to return to statementHelper.
                    // XXX Better way?
                    return nf.createLabel(ts.getLineno());
                }
            }

            decompiler.addName(name);
            if (compilerEnv.isXmlAvailable()) {
                pn = propertyName(null, name, 0);
            } else {
                pn = nf.createName(name);
            }
            return pn;
          }

          case Token.NUMBER: {
            double n = ts.getNumber();
            decompiler.addNumber(n);
            return nf.createNumber(n);
          }

          case Token.STRING: {
            String s = ts.getString();
            decompiler.addString(s);
            return nf.createString(s);
          }

          case Token.DIV:
          case Token.ASSIGN_DIV: {
            // Got / or /= which should be treated as regexp in fact
            ts.readRegExp(tt);
            String flags = ts.regExpFlags;
            ts.regExpFlags = null;
            String re = ts.getString();
            decompiler.addRegexp(re, flags);
            int index = currentScriptOrFn.addRegexp(re, flags);
            return nf.createRegExp(index);
          }

          case Token.NULL:
          case Token.THIS:
          case Token.FALSE:
          case Token.TRUE:
            decompiler.addToken(tt);
            return nf.createLeaf(tt);

          case Token.RESERVED:
            reportError("msg.reserved.id");
            break;

          case Token.ERROR:
            /* the scanner or one of its subroutines reported the error. */
            break;

          case Token.EOF:
            reportError("msg.unexpected.eof");
            break;

          default:
            reportError("msg.syntax");
            break;
        }
        return null;    // should never reach here
    }"""


