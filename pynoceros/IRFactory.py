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

from ScriptOrFnNode import ScriptOrFnNode
from Token import Token
from Node import Node, Jump
from FunctionNode import FunctionNode
from ScriptRuntime import ScriptRuntime
from Context import Context

class IRFactory(object):
    """ generated source for IRFactory
    /**
     * This class allows the creation of nodes, and follows the Factory pattern.
     *
     * @see Node
     * @author Mike McCabe
     * @author Norris Boyd
     */
    """

    def __init__(self, parser):
        self.parser = parser

    def createScript(self):
        return ScriptOrFnNode(Token.SCRIPT)

    def initScript(self, scriptNode, body):
        children = body.getFirstChild()
        if children is not None:
            scriptNode.addChildrenToBack(children)

    #@overloaded
    def createLeaf(self, nodeType):
        return Node(nodeType)

    """@createLeaf.register(object, int, int)
    def createLeaf_0(self, nodeType, nodeOp):
        return Node(nodeType, nodeOp)
    """

    def createSwitch(self, expr, lineno):
        switchNode = Jump(Token.SWITCH, expr, lineno)
        block = Node(Token.BLOCK, switchNode)
        return block

    def addSwitchCase(self, switchBlock, caseExpression, statements):
        if (switchBlock.getType() != Token.BLOCK):
            raise Kit.codeBug()
        switchNode = switchBlock.getFirstChild()
        if (switchNode.getType() != Token.SWITCH):
            raise Kit.codeBug()
        gotoTarget = Node.newTarget()
        if caseExpression is not None:
            caseNode = Jump(Token.CASE, caseExpression)
            caseNode.target = gotoTarget
            switchNode.addChildToBack(caseNode)
        else:
            switchNode.setDefault(gotoTarget)
        switchBlock.addChildToBack(gotoTarget)
        switchBlock.addChildToBack(statements)

    def closeSwitch(self, switchBlock):
        if (switchBlock.getType() != Token.BLOCK):
            raise Kit.codeBug()
        switchNode = switchBlock.getFirstChild()
        if (switchNode.getType() != Token.SWITCH):
            raise Kit.codeBug()
        switchBreakTarget = Node.newTarget()
        switchNode.target = switchBreakTarget
        defaultTarget = switchNode.getDefault()
        if defaultTarget is None:
            defaultTarget = switchBreakTarget
        switchBlock.addChildAfter(self.makeJump(Token.GOTO, defaultTarget), switchNode)
        switchBlock.addChildToBack(switchBreakTarget)

    def createVariables(self, token, lineno):
        return Node(token, lineno)

    def createExprStatement(self, expr, lineno):
        type = 0
        if self.parser.insideFunction():
            type = Token.EXPR_VOID
        else:
            type = Token.EXPR_RESULT
        return Node(type, expr, lineno)

    def createExprStatementNoReturn(self, expr, lineno):
        return Node(Token.EXPR_VOID, expr, lineno)

    def createDefaultNamespace(self, expr, lineno):
        self.setRequiresActivation()
        n = self.createUnary(Token.DEFAULTNAMESPACE, expr)
        result = self.createExprStatement(n, lineno)
        return result

    def createName(self, name):
        self.checkActivationName(name, Token.NAME)
        return Node.newString(Token.NAME, name)

    def createString(self, string):
        return Node.newString(string)

    def createNumber(self, number):
        return Node.newNumber(number)

    def createCatch(self, varName, catchCond, stmts, lineno):
        if catchCond is None:
            catchCond = Node(Token.EMPTY)
        return Node(Token.CATCH, self.createName(varName), catchCond, stmts, lineno)

    def createThrow(self, expr, lineno):
        return Node(Token.THROW, expr, lineno)

    def createReturn(self, expr, lineno):
        return Node(Token.RETURN, lineno) if expr is None else Node(Token.RETURN, expr, lineno)

    def createLabel(self, lineno):
        return Jump(Token.LABEL, lineno)

    def getLabelLoop(self, label):
        return label.getLoop()

    def createLabeledStatement(self, labelArg, statement):
        label = labelArg
        breakTarget = Node.newTarget()
        block = Node(Token.BLOCK, label, statement, breakTarget)
        label.target = breakTarget
        return block

    def createBreak(self, breakStatement, lineno):
        n = Jump(Token.BREAK, lineno)
        jumpStatement = None#Jump()
        t = breakStatement.getType()
        if (t == Token.LOOP) or (t == Token.LABEL):
            jumpStatement = breakStatement
        else:
            if (t == Token.BLOCK) and (breakStatement.getFirstChild().getType() == Token.SWITCH):
                jumpStatement = breakStatement.getFirstChild()
            else:
                raise Kit.codeBug()
        n.setJumpStatement(jumpStatement)
        return n

    def createContinue(self, loop, lineno):
        if (loop.getType() != Token.LOOP):
            Kit.codeBug()
        n = Jump(Token.CONTINUE, lineno)
        n.setJumpStatement(loop)
        return n

    def createBlock(self, lineno):
        return Node(Token.BLOCK, lineno)

    def createFunction(self, name):
        return FunctionNode(name)

    def initFunction(self, fnNode, functionIndex, statements, functionType):
        fnNode.itsFunctionType = functionType
        fnNode.addChildToBack(statements)
        functionCount = fnNode.getFunctionCount()
        if (functionCount != 0):
            fnNode.itsNeedsActivation = True
            ## for-while
            i = 0
            while (i != functionCount):
                fn = fnNode.getFunctionNode(i)
                if (fn.getFunctionType() == FunctionNode.FUNCTION_EXPRESSION_STATEMENT):
                    name = fn.getFunctionName()
                    if name is not None and len((name) != 0):
                        fnNode.removeParamOrVar(name)
                i += 1
        if (functionType == FunctionNode.FUNCTION_EXPRESSION):
            name = fnNode.getFunctionName()
            if (name is not None) and \
                            len(name) != 0 \
                            and (not fnNode.hasParamOrVar(name)):

                if (fnNode.addVar(name) == ScriptOrFnNode.DUPLICATE_CONST):
                    self.parser.addError("msg.const.redecl", name)
                setFn = Node(Token.EXPR_VOID, Node(Token.SETNAME, Node.newString(Token.BINDNAME, name), Node(Token.THISFN)))
                statements.addChildrenToFront(setFn)
        lastStmt = statements.getLastChild()
        if lastStmt is None or (lastStmt.getType() != Token.RETURN):
            statements.addChildToBack(Node(Token.RETURN))
        result = Node.newString(Token.FUNCTION, fnNode.getFunctionName())
        result.putIntProp(Node.FUNCTION_PROP, functionIndex)
        return result

    def addChildToBack(self, parent, child):
        parent.addChildToBack(child)

    def createLoopNode(self, loopLabel, lineno):
        result = Jump(Token.LOOP, lineno)
        if loopLabel is not None:
            loopLabel.setLoop(result)
        return result

    def createWhile(self, loop, cond, body):
        return self.createLoop(loop, self.LOOP_WHILE, body, cond, None, None)

    def createDoWhile(self, loop, body, cond):
        return self.createLoop(loop, self.LOOP_DO_WHILE, body, cond, None, None)

    def createFor(self, loop,
                        init,
                        test,
                        incr,
                        body):
        return self.createLoop(loop, self.LOOP_FOR, body, test, init, incr)

    def createLoop(self, loop,
                         loopType,
                         body,
                         cond,
                         init,
                         incr):
        bodyTarget = Node.newTarget()
        condTarget = Node.newTarget()
        if (loopType == self.LOOP_FOR) and (cond.getType() == Token.EMPTY):
            cond = Node(Token.TRUE)
        IFEQ = Jump(Token.IFEQ, cond)
        IFEQ.target = bodyTarget
        breakTarget = Node.newTarget()
        loop.addChildToBack(bodyTarget)
        loop.addChildrenToBack(body)
        if (loopType == self.LOOP_WHILE) or (loopType == self.LOOP_FOR):
            loop.addChildrenToBack(Node(Token.EMPTY, loop.getLineno()))
        loop.addChildToBack(condTarget)
        loop.addChildToBack(IFEQ)
        loop.addChildToBack(breakTarget)
        loop.target = breakTarget
        continueTarget = condTarget
        if (loopType == self.LOOP_WHILE) or (loopType == self.LOOP_FOR):
            loop.addChildToFront(self.makeJump(Token.GOTO, condTarget))
            if (loopType == self.LOOP_FOR):
                if (init.getType() != Token.EMPTY):
                    if (init.getType() != Token.VAR):
                        init = Node(Token.EXPR_VOID, init)
                    loop.addChildToFront(init)
                incrTarget = Node.newTarget()
                loop.addChildAfter(incrTarget, body)
                if (incr.getType() != Token.EMPTY):
                    incr = Node(Token.EXPR_VOID, incr)
                    loop.addChildAfter(incr, incrTarget)
                continueTarget = incrTarget
        loop.setContinue(continueTarget)
        return loop

    def createForIn(self, loop,
                          lhs,
                          obj,
                          body,
                          isForEach):
        type = lhs.getType()
        lvalue = None#Node()
        if (type == Token.VAR):
            lastChild = lhs.getLastChild()
            if (lhs.getFirstChild() != lastChild):
                self.parser.reportError("msg.mult.index")
            lvalue = Node.newString(Token.NAME, lastChild.getString())
        else:
            lvalue = self.makeReference(lhs)
            if lvalue is None:
                self.parser.reportError("msg.bad.for.in.lhs")
                return obj
        localBlock = Node(Token.LOCAL_BLOCK)
        initType = Token.ENUM_INIT_VALUES if isForEach else Token.ENUM_INIT_KEYS
        init = Node(initType, obj)
        init.putProp(Node.LOCAL_BLOCK_PROP, localBlock)
        cond = Node(Token.ENUM_NEXT)
        cond.putProp(Node.LOCAL_BLOCK_PROP, localBlock)
        id = Node(Token.ENUM_ID)
        id.putProp(Node.LOCAL_BLOCK_PROP, localBlock)
        newBody = Node(Token.BLOCK)
        assign = self.simpleAssignment(lvalue, id)
        newBody.addChildToBack(Node(Token.EXPR_VOID, assign))
        newBody.addChildToBack(body)
        loop = self.createWhile(loop, cond, newBody)
        loop.addChildToFront(init)
        if (type == Token.VAR):
            loop.addChildToFront(lhs)
        localBlock.addChildToBack(loop)
        return localBlock

    def createTryCatchFinally(self, tryBlock, catchBlocks, finallyBlock, lineno):
        hasFinally = finallyBlock is not None and ( (finallyBlock.getType() != Token.BLOCK) or finallyBlock.hasChildren())
        if (tryBlock.getType() == Token.BLOCK) and not tryBlock.hasChildren() and not hasFinally:
            return tryBlock
        hasCatch = catchBlocks.hasChildren()
        if not hasFinally and not hasCatch:
            return tryBlock
        handlerBlock = Node(Token.LOCAL_BLOCK)
        pn = Jump(Token.TRY, tryBlock, lineno)
        pn.putProp(Node.LOCAL_BLOCK_PROP, handlerBlock)
        if hasCatch:
            endCatch = Node.newTarget()
            pn.addChildToBack(self.makeJump(Token.GOTO, endCatch))
            catchTarget = Node.newTarget()
            pn.target = catchTarget
            pn.addChildToBack(catchTarget)
            catchScopeBlock = Node(Token.LOCAL_BLOCK)
            cb = catchBlocks.getFirstChild()
            hasDefault = False
            scopeIndex = 0
            while cb is not None:
                catchLineNo = cb.getLineno()
                name = cb.getFirstChild()
                cond = name.getNext()
                catchStatement = cond.getNext()
                cb.removeChild(name)
                cb.removeChild(cond)
                cb.removeChild(catchStatement)
                catchStatement.addChildToBack(Node(Token.LEAVEWITH))
                catchStatement.addChildToBack(self.makeJump(Token.GOTO, endCatch))
                condStmt = None#Node()
                if (cond.getType() == Token.EMPTY):
                    condStmt = catchStatement
                    hasDefault = True
                else:
                    condStmt = self.createIf(cond, catchStatement, None, catchLineNo)
                catchScope = Node(Token.CATCH_SCOPE, name, self.createUseLocal(handlerBlock))
                catchScope.putProp(Node.LOCAL_BLOCK_PROP, catchScopeBlock)
                catchScope.putIntProp(Node.CATCH_SCOPE_PROP, scopeIndex)
                catchScopeBlock.addChildToBack(catchScope)
                catchScopeBlock.addChildToBack(self.createWith(self.createUseLocal(catchScopeBlock), condStmt, catchLineNo))
                cb = cb.getNext()
                scopeIndex += 1
            pn.addChildToBack(catchScopeBlock)
            if not hasDefault:
                rethrow = Node(Token.RETHROW)
                rethrow.putProp(Node.LOCAL_BLOCK_PROP, handlerBlock)
                pn.addChildToBack(rethrow)
            pn.addChildToBack(endCatch)
        if hasFinally:
            finallyTarget = Node.newTarget()
            pn.setFinally(finallyTarget)
            pn.addChildToBack(self.makeJump(Token.JSR, finallyTarget))
            finallyEnd = Node.newTarget()
            pn.addChildToBack(self.makeJump(Token.GOTO, finallyEnd))
            pn.addChildToBack(finallyTarget)
            fBlock = Node(Token.FINALLY, finallyBlock)
            fBlock.putProp(Node.LOCAL_BLOCK_PROP, handlerBlock)
            pn.addChildToBack(fBlock)
            pn.addChildToBack(finallyEnd)
        handlerBlock.addChildToBack(pn)
        return handlerBlock

    def createWith(self, obj, body, lineno):
        self.setRequiresActivation()
        result = Node(Token.BLOCK, lineno)
        result.addChildToBack(Node(Token.ENTERWITH, obj))
        bodyNode = Node(Token.WITH, body, lineno)
        result.addChildrenToBack(bodyNode)
        result.addChildToBack(Node(Token.LEAVEWITH))
        return result

    def createDotQuery(self, obj, body, lineno):
        self.setRequiresActivation()
        result = Node(Token.DOTQUERY, obj, body, lineno)
        return result

    def createArrayLiteral(self, elems, skipCount):
        length = len(elems)
        skipIndexes = None
        if (skipCount != 0):
            skipIndexes = [int() for __idx0 in range(skipCount)]
        array = Node(Token.ARRAYLIT)
        ## for-while
        i = 0
        j = 0
        while (i != length):
            elem = elems[i]
            if elem is not None:
                array.addChildToBack(elem)
            else:
                skipIndexes[j] = i
                j += 1
            i += 1
        if (skipCount != 0):
            array.putProp(Node.SKIP_INDEXES_PROP, skipIndexes)
        return array

    def createObjectLiteral(self, elems):
        size = len(elems) / 2
        ob = Node(Token.OBJECTLIT)
        if (size == 0):
            properties = ScriptRuntime.emptyArgs
        else:
            properties = [object() for __idx0 in range(size)]
            ## for-while
            i = 0
            while (i != size):
                properties[i] = elems[2 * i]
                value = elems[2 * i + 1]
                ob.addChildToBack(value)
                i += 1
        ob.putProp(Node.OBJECT_IDS_PROP, properties)
        return ob

    def createRegExp(self, regexpIndex):
        n = Node(Token.REGEXP)
        n.putIntProp(Node.REGEXP_PROP, regexpIndex)
        return n

    def createIf(self, cond, ifTrue, ifFalse, lineno):
        condStatus = self.isAlwaysDefinedBoolean(cond)
        if (condStatus == self.ALWAYS_TRUE_BOOLEAN):
            return ifTrue
        else:
            if (condStatus == self.ALWAYS_FALSE_BOOLEAN):
                if ifFalse is not None:
                    return ifFalse
                return Node(Token.BLOCK, lineno)
        result = Node(Token.BLOCK, lineno)
        ifNotTarget = Node.newTarget()
        IFNE = Jump(Token.IFNE, cond)
        IFNE.target = ifNotTarget
        result.addChildToBack(IFNE)
        result.addChildrenToBack(ifTrue)
        if ifFalse is not None:
            endTarget = Node.newTarget()
            result.addChildToBack(self.makeJump(Token.GOTO, endTarget))
            result.addChildToBack(ifNotTarget)
            result.addChildrenToBack(ifFalse)
            result.addChildToBack(endTarget)
        else:
            result.addChildToBack(ifNotTarget)
        return result

    def createCondExpr(self, cond, ifTrue, ifFalse):
        condStatus = self.isAlwaysDefinedBoolean(cond)
        if (condStatus == self.ALWAYS_TRUE_BOOLEAN):
            return ifTrue
        else:
            if (condStatus == self.ALWAYS_FALSE_BOOLEAN):
                return ifFalse
        return Node(Token.HOOK, cond, ifTrue, ifFalse)

    def createUnary(self, nodeType, child):
        childType = child.getType()
        if nodeType == Token.DELPROP:
            n = None#Node()
            if (childType == Token.NAME):
                child.setType(Token.BINDNAME)
                left = child
                right = Node.newString(child.getString())
                n = Node(nodeType, left, right)
            else:
                if (childType == Token.GETPROP) or (childType == Token.GETELEM):
                    left = child.getFirstChild()
                    right = child.getLastChild()
                    child.removeChild(left)
                    child.removeChild(right)
                    n = Node(nodeType, left, right)
                else:
                    if (childType == Token.GET_REF):
                        ref = child.getFirstChild()
                        child.removeChild(ref)
                        n = Node(Token.DEL_REF, ref)
                    else:
                        n = Node(Token.TRUE)
            return n
        elif nodeType == Token.TYPEOF:
            if (childType == Token.NAME):
                child.setType(Token.TYPEOFNAME)
                return child
        elif nodeType == Token.BITNOT:
            if (childType == Token.NUMBER):
                value = ScriptRuntime.toInt32(child.getDouble())
                child.setDouble(~value)
                return child
        elif nodeType == Token.NEG:
            if (childType == Token.NUMBER):
                child.setDouble(-child.getDouble())
                return child
        elif nodeType == Token.NOT:
            status = self.isAlwaysDefinedBoolean(child)
            if (status != 0):
                type = 0
                if (status == self.ALWAYS_TRUE_BOOLEAN):
                    type = Token.FALSE
                else:
                    type = Token.TRUE
                if (childType == Token.TRUE) or (childType == Token.FALSE):
                    child.setType(type)
                    return child
                return Node(type)
        return Node(nodeType, child)

    def createCallOrNew(self, nodeType, child):
        type = Node.NON_SPECIALCALL
        if (child.getType() == Token.NAME):
            name = child.getString()
            if name == "eval":
                type = Node.SPECIALCALL_EVAL
            else:
                if name == "With":
                    type = Node.SPECIALCALL_WITH
        else:
            if (child.getType() == Token.GETPROP):
                name = child.getLastChild().getString()
                if name == "eval":
                    type = Node.SPECIALCALL_EVAL
        node = Node(nodeType, child)
        if (type != Node.NON_SPECIALCALL):
            self.setRequiresActivation()
            node.putIntProp(Node.SPECIALCALL_PROP, type)
        return node

    def createIncDec(self, nodeType, post, child):
        child = self.makeReference(child)
        if child is None:
            msg = ""
            if (nodeType == Token.DEC):
                msg = "msg.bad.decr"
            else:
                msg = "msg.bad.incr"
            self.parser.reportError(msg)
            return
        childType = child.getType()
        if childType in  (Token.NAME,
                          Token.GETPROP,
                          Token.GETELEM,
                          Token.GET_REF):
            n = Node(nodeType, child)
            incrDecrMask = 0
            if (nodeType == Token.DEC):
                incrDecrMask |= Node.DECR_FLAG
            if post:
                incrDecrMask |= Node.POST_FLAG
            n.putIntProp(Node.INCRDECR_PROP, incrDecrMask)
            return n
        raise Kit.codeBug()

    def createPropertyGet(self, target, namespace, name, memberTypeFlags):
        if namespace is None and (memberTypeFlags == 0):
            if target is None:
                return self.createName(name)
            self.checkActivationName(name, Token.GETPROP)
            if ScriptRuntime.isSpecialProperty(name):
                ref = Node(Token.REF_SPECIAL, target)
                ref.putProp(Node.NAME_PROP, name)
                return Node(Token.GET_REF, ref)
            return Node(Token.GETPROP, target, self.createString(name))
        elem = self.createString(name)
        memberTypeFlags |= Node.PROPERTY_FLAG
        return self.createMemberRefGet(target, namespace, elem, memberTypeFlags)

    def createElementGet(self, target, namespace, elem, memberTypeFlags):
        if namespace is None and (memberTypeFlags == 0):
            if target is None:
                raise Kit.codeBug()
            return Node(Token.GETELEM, target, elem)
        return self.createMemberRefGet(target, namespace, elem, memberTypeFlags)

    def createMemberRefGet(self, target, namespace, elem, memberTypeFlags):
        nsNode = None
        if namespace is not None:
            if namespace == "*":
                nsNode = Node(Token.NULL)
            else:
                nsNode = self.createName(namespace)
        ref = None#Node()
        if target is None:
            if namespace is None:
                ref = Node(Token.REF_NAME, elem)
            else:
                ref = Node(Token.REF_NS_NAME, nsNode, elem)
        else:
            if namespace is None:
                ref = Node(Token.REF_MEMBER, target, elem)
            else:
                ref = Node(Token.REF_NS_MEMBER, target, nsNode, elem)
        if (memberTypeFlags != 0):
            ref.putIntProp(Node.MEMBER_TYPE_PROP, memberTypeFlags)
        return Node(Token.GET_REF, ref)

    def createBinary(self, nodeType, left, right):
        if nodeType == Token.ADD:
            if (left.type == Token.STRING):
                s2 = ""
                if (right.type == Token.STRING):
                    s2 = right.getString()
                else:
                    if (right.type == Token.NUMBER):
                        s2 = ScriptRuntime.numberToString(right.getDouble(), 10)
                    else:
                        pass
                s1 = left.getString()
                left.setString(s1+s2)
                return left
            else:
                if (left.type == Token.NUMBER):
                    if (right.type == Token.NUMBER):
                        left.setDouble(left.getDouble() + right.getDouble())
                        return left
                    else:
                        if (right.type == Token.STRING):
                            s1 = ""
                            s2 = ""
                            s1 = ScriptRuntime.numberToString(left.getDouble(), 10)
                            s2 = right.getString()
                            right.setString(s1.concat(s2))
                            return right
        elif nodeType == Token.SUB:
            if (left.type == Token.NUMBER):
                ld = left.getDouble()
                if (right.type == Token.NUMBER):
                    left.setDouble(ld - right.getDouble())
                    return left
                else:
                    if (ld == 0.0):
                        return Node(Token.NEG, right)
            else:
                if (right.type == Token.NUMBER):
                    if (right.getDouble() == 0.0):
                        return Node(Token.POS, left)
        elif nodeType == Token.MUL:
            if (left.type == Token.NUMBER):
                ld = left.getDouble()
                if (right.type == Token.NUMBER):
                    left.setDouble(ld * right.getDouble())
                    return left
                else:
                    if (ld == 1.0):
                        return Node(Token.POS, right)
            else:
                if (right.type == Token.NUMBER):
                    if (right.getDouble() == 1.0):
                        return Node(Token.POS, left)
        elif nodeType == Token.DIV:
            if (right.type == Token.NUMBER):
                rd = right.getDouble()
                if (left.type == Token.NUMBER):
                    left.setDouble(left.getDouble() / rd)
                    return left
                else:
                    if (rd == 1.0):
                        return Node(Token.POS, left)
        elif nodeType == Token.AND:
            leftStatus = self.isAlwaysDefinedBoolean(left)
            if (leftStatus == self.ALWAYS_FALSE_BOOLEAN):
                return left
            else:
                if (leftStatus == self.ALWAYS_TRUE_BOOLEAN):
                    return right
        elif nodeType == Token.OR:
            leftStatus = self.isAlwaysDefinedBoolean(left)
            if (leftStatus == self.ALWAYS_TRUE_BOOLEAN):
                return left
            else:
                if (leftStatus == self.ALWAYS_FALSE_BOOLEAN):
                    return right
        return Node(nodeType, left, right)

    def simpleAssignment(self, left, right):
        nodeType = left.getType()
        if nodeType == Token.NAME:
            left.setType(Token.BINDNAME)
            return Node(Token.SETNAME, left, right)
        elif nodeType in (Token.GETPROP, 
                          Token.GETELEM):
            obj = left.getFirstChild()
            id = left.getLastChild()
            type = 0
            if (nodeType == Token.GETPROP):
                type = Token.SETPROP
            else:
                type = Token.SETELEM
            return Node(type, obj, id, right)
        elif nodeType == Token.GET_REF:
            ref = left.getFirstChild()
            self.checkMutableReference(ref)
            return Node(Token.SET_REF, ref, right)
        raise Kit.codeBug()

    def checkMutableReference(self, n):
        memberTypeFlags = n.getIntProp(Node.MEMBER_TYPE_PROP, 0)
        if (memberTypeFlags & Node.DESCENDANTS_FLAG != 0):
            self.parser.reportError("msg.bad.assign.left")

    def createAssignment(self, assignType, left, right):
        left = self.makeReference(left)
        if left is None:
            self.parser.reportError("msg.bad.assign.left")
            return right
        assignOp = 0
        if assignType == Token.ASSIGN:
            return self.simpleAssignment(left, right)
        elif assignType == Token.ASSIGN_BITOR:
            assignOp = Token.BITOR
        elif assignType == Token.ASSIGN_BITXOR:
            assignOp = Token.BITXOR
        elif assignType == Token.ASSIGN_BITAND:
            assignOp = Token.BITAND
        elif assignType == Token.ASSIGN_LSH:
            assignOp = Token.LSH
        elif assignType == Token.ASSIGN_RSH:
            assignOp = Token.RSH
        elif assignType == Token.ASSIGN_URSH:
            assignOp = Token.URSH
        elif assignType == Token.ASSIGN_ADD:
            assignOp = Token.ADD
        elif assignType == Token.ASSIGN_SUB:
            assignOp = Token.SUB
        elif assignType == Token.ASSIGN_MUL:
            assignOp = Token.MUL
        elif assignType == Token.ASSIGN_DIV:
            assignOp = Token.DIV
        elif assignType == Token.ASSIGN_MOD:
            assignOp = Token.MOD
        else:
            raise Kit.codeBug()
        nodeType = left.getType()
        if nodeType == Token.NAME:
            s = left.getString()
            opLeft = Node.newString(Token.NAME, s)
            op = Node(assignOp, opLeft, right)
            lvalueLeft = Node.newString(Token.BINDNAME, s)
            return Node(Token.SETNAME, lvalueLeft, op)
        elif nodeType in (Token.GETPROP,
                          Token.GETELEM):
            obj = left.getFirstChild()
            id = left.getLastChild()
            type = Token.SETPROP_OP if (nodeType == Token.GETPROP) else Token.SETELEM_OP
            opLeft = Node(Token.USE_STACK)
            op = Node(assignOp, opLeft, right)
            return Node(type, obj, id, op)
        elif nodeType == Token.GET_REF:
            ref = left.getFirstChild()
            self.checkMutableReference(ref)
            opLeft = Node(Token.USE_STACK)
            op = Node(assignOp, opLeft, right)
            return Node(Token.SET_REF_OP, ref, op)
        raise Kit.codeBug()

    def createUseLocal(self, localBlock):
        if (Token.LOCAL_BLOCK != localBlock.getType()):
            raise Kit.codeBug()
        result = Node(Token.LOCAL_LOAD)
        result.putProp(Node.LOCAL_BLOCK_PROP, localBlock)
        return result

    def makeJump(self, type, target):
        n = Jump(type)
        n.target = target
        return n

    def makeReference(self, node):
        type = node.getType()
        if type in (Token.NAME, 
                    Token.GETPROP, 
                    Token.GETELEM, 
                    Token.GET_REF):
                    
            return node
        elif type == Token.CALL:
            node.setType(Token.REF_CALL)
            return Node(Token.GET_REF, node)
        return

    @classmethod
    def isAlwaysDefinedBoolean(cls, node):
        if node.getType() in (Token.FALSE, Token.NULL):
            return cls.ALWAYS_FALSE_BOOLEAN
        elif node.getType() == Token.TRUE:
            return cls.ALWAYS_TRUE_BOOLEAN
        elif node.getType() == Token.NUMBER:
            num = node.getDouble()
            if (num == num) and (num != 0.0):
                return cls.ALWAYS_TRUE_BOOLEAN
            else:
                return cls.ALWAYS_FALSE_BOOLEAN
        return 0

    def checkActivationName(self, name, token):
        if self.parser.insideFunction():
            activation = False
            if "arguments" == name or \
                (self.parser.compilerEnv.activationNames is not None) and \
                (self.parser.compilerEnv.activationNames.get(name) is not None):
                activation = True
            else:
                if "length" == name:
                    if (token == Token.GETPROP) and (self.parser.compilerEnv.getLanguageVersion() == Context.VERSION_1_2):
                        activation = True
            if activation:
                self.setRequiresActivation()

    def setRequiresActivation(self):
        if self.parser.insideFunction():
            self.parser.currentScriptOrFn.itsNeedsActivation = True

    LOOP_DO_WHILE = 0
    LOOP_WHILE = 1
    LOOP_FOR = 2
    ALWAYS_TRUE_BOOLEAN = 1
    ALWAYS_FALSE_BOOLEAN = -1

