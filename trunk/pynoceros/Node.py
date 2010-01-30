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

from Token import Token

class Node(object):
    """ generated source for Node

    """
    FUNCTION_PROP = 1
    LOCAL_PROP = 2
    LOCAL_BLOCK_PROP = 3
    REGEXP_PROP = 4
    CASEARRAY_PROP = 5
    TARGETBLOCK_PROP = 6
    VARIABLE_PROP = 7
    ISNUMBER_PROP = 8
    DIRECTCALL_PROP = 9
    SPECIALCALL_PROP = 10
    SKIP_INDEXES_PROP = 11
    OBJECT_IDS_PROP = 12
    INCRDECR_PROP = 13
    CATCH_SCOPE_PROP = 14
    LABEL_ID_PROP = 15
    MEMBER_TYPE_PROP = 16
    NAME_PROP = 17
    CONTROL_BLOCK_PROP = 18
    PARENTHESIZED_PROP = 19
    LAST_PROP = 19
    BOTH = 0
    LEFT = 1
    RIGHT = 2
    NON_SPECIALCALL = 0
    SPECIALCALL_EVAL = 1
    SPECIALCALL_WITH = 2
    DECR_FLAG = 0x1
    POST_FLAG = 0x2
    PROPERTY_FLAG = 0x1
    ATTRIBUTE_FLAG = 0x2
    DESCENDANTS_FLAG = 0x4

    #@overloaded
    def __init__(self, *args):
        def typefunction(arg):
            if isinstance(arg, Node):
                return Node
            else: 
                return type(arg)
                
        types = tuple([typefunction(a) for a in args])
        if types == (int, Node) or types == (int, type(None)):
            self.__init___0(*args)
        elif types == (int, Node, Node):
            self.__init___1(*args)
        elif types == (int, Node, Node, Node):
            self.__init___2(*args)
        elif types == (int, int):
            self.__init___3(*args)
        # had an issue where ,Node. was None
        elif types == (int, Node, int) or types == (int, type(None), int):
            self.__init___4(*args)
        elif types == (int, Node, Node, int):
            self.__init___5(*args)
        elif types == (int,):
            self.__init___(*args)
        elif types == (int, Node, Node, Node, int):
            self.__init___6(*args)
        else:
            print types
            raise NotImplementedError()
        
    """
    def __init__(self, nodeType, left = None, right = None):
        self.type = nodeType
        if isinstance(left, int):
            #left is actually line number
            self.lineno = left
            return
        self.last = right or left # takes the left-most non None
        if left is not None:
            left.next = right
        if right is not None:
            right.next = None
    """
    def __init___(self, nodeType):
        self.type = nodeType
        self.last = None


    #@__init__.register(object, int, Node)
    def __init___0(self, nodeType, child):
        self.type = nodeType
        self.first = self.last = child
        if child is not None: # <- to get with statements working - 
                              # TODO: check this is required
            child.next = None

    #@__init__.register(object, int, Node, Node)
    def __init___1(self, nodeType, left, right):
        self.type = nodeType
        self.first = left
        self.last = right
        left.next = right
        right.next = None

    #@__init__.register(object, int, Node, Node, Node)
    def __init___2(self, nodeType, left, mid, right):
        self.type = nodeType
        self.first = left
        self.last = right
        left.next = mid
        mid.next = right
        right.next = None

    #@__init__.register(object, int, int)
    def __init___3(self, nodeType, line):
        self.type = nodeType
        self.lineno = line

    #@__init__.register(object, int, Node, int)
    def __init___4(self, nodeType, child, line):
        self.__init__(nodeType, child)
        #super(Node, self).__init__(nodeType, child)
        self.lineno = line

    #@__init__.register(object, int, Node, Node, int)
    def __init___5(self, nodeType, left, right, line):
        self.__init__(nodeType, left, right)
        #super(Node, self).__init__(nodeType, left, right)
        self.lineno = line
    
    #@__init__.register(object, int, Node, Node, Node, int)
    def __init___6(self, nodeType,
                         left,
                         mid,
                         right,
                         line):
        self.__init__(nodeType, left, mid, right)
        #super(Node, self).__init__(nodeType, left, mid, right)
        self.lineno = line
   
    @classmethod
    def newNumber(cls, number):
        return NumberNode(number)

    @classmethod
    #@overloaded
    def newString(cls, arg1, arg2 = None):
        if arg2 is None:
            strval = arg1
            token_type = Token.STRING
        else:
            token_type = arg1
            strval = arg2
        return StringNode(token_type, strval)

    """
    @classmethod
    @newString.register(type, int, str)
    def newString_0(cls, type, strval):
        return StringNode(cls.type, strval)
    """

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = self.type

    def hasChildren(self):
        return self.first is not None

    def getFirstChild(self):
        return self.first

    def getLastChild(self):
        return self.last

    def getNext(self):
        return self.next

    def getChildBefore(self, child):
        if (child == self.first):
            return
        n = self.first
        while (n.next != child):
            n = n.next
            if n is None:
                raise RuntimeException("node is not a child")
        return n

    def getLastSibling(self):
        n = self
        while n.next is not None:
            n = n.next
        return n

    def addChildToFront(self, child):
        child.next = self.first
        self.first = child
        if self.last is None:
            self.last = child

    def addChildToBack(self, child):
        child.next = None
        if self.last is None:
            self.first = self.last = child
            return
        self.last.next = child
        self.last = child

    def addChildrenToFront(self, children):
        lastSib = children.getLastSibling()
        lastSib.next = self.first
        self.first = children
        if self.last is None:
            self.last = lastSib

    def addChildrenToBack(self, children):
        if self.last is not None:
            self.last.next = children
        self.last = children.getLastSibling()
        if self.first is None:
            self.first = children

    def addChildBefore(self, newChild, node):
        if newChild.next is not None:
            raise RuntimeException("newChild had siblings in addChildBefore")
        if (self.first == node):
            newChild.next = self.first
            self.first = newChild
            return
        prev = self.getChildBefore(node)
        self.addChildAfter(newChild, prev)

    def addChildAfter(self, newChild, node):
        if newChild.next is not None:
            raise RuntimeException("newChild had siblings in addChildAfter")
        newChild.next = node.next
        node.next = newChild
        if (self.last == node):
            self.last = newChild

    def removeChild(self, child):
        prev = self.getChildBefore(child)
        if prev is None:
            self.first = self.first.next
        else:
            prev.next = child.next
        if (child == self.last):
            self.last = prev
        child.next = None

    def replaceChild(self, child, newChild):
        newChild.next = child.next
        if (child == self.first):
            self.first = newChild
        else:
            prev = self.getChildBefore(child)
            prev.next = newChild
        if (child == self.last):
            self.last = newChild
        child.next = None

    def replaceChildAfter(self, prevChild, newChild):
        child = prevChild.next
        newChild.next = child.next
        prevChild.next = newChild
        if (child == self.last):
            self.last = newChild
        child.next = None

    @classmethod
    def propToString(cls, propType):
        if Token.printTrees:
            if propType == cls.FUNCTION_PROP:
                return "function"
            elif propType == cls.LOCAL_PROP:
                return "local"
            elif propType == cls.LOCAL_BLOCK_PROP:
                return "local_block"
            elif propType == cls.REGEXP_PROP:
                return "regexp"
            elif propType == cls.CASEARRAY_PROP:
                return "casearray"
            elif propType == cls.TARGETBLOCK_PROP:
                return "targetblock"
            elif propType == cls.VARIABLE_PROP:
                return "variable"
            elif propType == cls.ISNUMBER_PROP:
                return "isnumber"
            elif propType == cls.DIRECTCALL_PROP:
                return "directcall"
            elif propType == cls.SPECIALCALL_PROP:
                return "specialcall"
            elif propType == cls.SKIP_INDEXES_PROP:
                return "skip_indexes"
            elif propType == cls.OBJECT_IDS_PROP:
                return "object_ids_prop"
            elif propType == cls.INCRDECR_PROP:
                return "incrdecr_prop"
            elif propType == cls.CATCH_SCOPE_PROP:
                return "catch_scope_prop"
            elif propType == cls.LABEL_ID_PROP:
                return "label_id_prop"
            elif propType == cls.MEMBER_TYPE_PROP:
                return "member_type_prop"
            elif propType == cls.NAME_PROP:
                return "name_prop"
            elif propType == cls.CONTROL_BLOCK_PROP:
                return "control_block_prop"
            elif propType == cls.PARENTHESIZED_PROP:
                return "parenthesized_prop"
            else:
                Kit.codeBug()
        return

    def lookupProperty(self, propType):
        x = self.propListHead
        while x is not None and (propType != x.type):
            x = x.next
        return x

    def ensureProperty(self, propType):
        item = self.lookupProperty(propType)
        if item is None:
            item = PropListItem()
            item.type = propType
            item.next = self.propListHead
            self.propListHead = item
        return item

    def removeProp(self, propType):
        x = self.propListHead
        if x is not None:
            prev = None
            while (x.type != propType):
                prev = x
                x = x.next
                if x is None:
                    return
            if prev is None:
                self.propListHead = x.next
            else:
                prev.next = x.next

    def getProp(self, propType):
        item = self.lookupProperty(propType)
        if item is None:
            return
        return item.objectValue

    def getIntProp(self, propType, defaultValue):
        item = self.lookupProperty(propType)
        if item is None:
            return defaultValue
        return item.intValue

    def getExistingIntProp(self, propType):
        item = self.lookupProperty(propType)
        if item is None:
            Kit.codeBug()
        return item.intValue

    def putProp(self, propType, prop):
        if prop is None:
            self.removeProp(propType)
        else:
            item = self.ensureProperty(propType)
            item.objectValue = prop

    def putIntProp(self, propType, prop):
        item = self.ensureProperty(propType)
        item.intValue = prop

    def getLineno(self):
        return self.lineno

    def getDouble(self):
        return self.number

    def setDouble(self, number):
        self.number = number

    def getString(self):
        return self.strval

    def setString(self, s):
        if s is None:
            Kit.codeBug()
        self.strval = s

    @classmethod
    def newTarget(cls):
        return Node(Token.TARGET)

    END_UNREACHED = 0
    END_DROPS_OFF = 1
    END_RETURNS = 2
    END_RETURNS_VALUE = 4

    def hasConsistentReturnUsage(self):
        n = self.endCheck()
        return (n & self.END_RETURNS_VALUE == 0) or (n & self.END_DROPS_OFF | self.END_RETURNS == 0)

    def endCheckIf(self):
        th = Node()
        el = Node()
        rv = self.END_UNREACHED
        th = self.next
        el = self.target
        rv = th.endCheck()
        if el is not None:
            rv |= el.endCheck()
        else:
            rv |= self.END_DROPS_OFF
        return rv

    def endCheckSwitch(self):
        n = Node()
        rv = self.END_UNREACHED
        ## for-while
        while n is not None:
            if (n.type == Token.CASE):
                rv |= n.target.endCheck()
            else:
                break
            n = n.next
        rv &= ~self.END_DROPS_OFF
        n = self.getDefault()
        if n is not None:
            rv |= n.endCheck()
        else:
            rv |= self.END_DROPS_OFF
        rv |= self.getIntProp(self.CONTROL_BLOCK_PROP, self.END_UNREACHED)
        return rv

    def endCheckTry(self):
        n = Node()
        rv = self.END_UNREACHED
        n = self.getFinally()
        if n is not None:
            rv = n.next.first.endCheck()
        else:
            rv = self.END_DROPS_OFF
        if (rv & self.END_DROPS_OFF != 0):
            rv &= ~self.END_DROPS_OFF
            rv |= self.first.endCheck()
            n = self.target
            if n is not None:
                ## for-while
                while n is not None:
                    rv |= n.next.first.next.first.endCheck()
                    n = n.next.next
        return rv

    def endCheckLoop(self):
        n = Node()
        rv = self.END_UNREACHED
        ## for-while
        while (n.next != self.last):
            n = n.next
        if (n.type != Token.IFEQ):
            return self.END_DROPS_OFF
        rv = n.target.next.endCheck()
        if (n.first.type == Token.TRUE):
            rv &= ~self.END_DROPS_OFF
        rv |= self.getIntProp(self.CONTROL_BLOCK_PROP, self.END_UNREACHED)
        return rv

    def endCheckBlock(self):
        n = Node()
        rv = self.END_DROPS_OFF
        ## for-while
        while (rv & self.END_DROPS_OFF != 0) and n is not None:
            rv &= ~self.END_DROPS_OFF
            rv |= n.endCheck()
            n = n.next
        return rv

    def endCheckLabel(self):
        rv = self.END_UNREACHED
        rv = self.next.endCheck()
        rv |= self.getIntProp(self.CONTROL_BLOCK_PROP, self.END_UNREACHED)
        return rv

    def endCheckBreak(self):
        n = self.jumpNode
        n.putIntProp(self.CONTROL_BLOCK_PROP, self.END_DROPS_OFF)
        return self.END_UNREACHED

    def endCheck(self):
        if self.type == Token.BREAK:
            return self.endCheckBreak()
        elif self.type == Token.THROW:
            return self.END_UNREACHED
        elif self.type == Token.RETURN:
            if self.first is not None:
                return self.END_RETURNS_VALUE
            else:
                return self.END_RETURNS
        elif self.type == Token.TARGET:
            if self.next is not None:
                return self.next.endCheck()
            else:
                return self.END_DROPS_OFF
        elif self.type == Token.LOOP:
            return self.endCheckLoop()
        elif self.type == Token.BLOCK:
            if self.first is None:
                return self.END_DROPS_OFF
            if self.first.type == Token.LABEL:
                return self.first.endCheckLabel()
            elif self.first.type == Token.IFNE:
                return self.first.endCheckIf()
            elif self.first.type == Token.SWITCH:
                return self.first.endCheckSwitch()
            elif self.first.type == Token.TRY:
                return self.first.endCheckTry()
            else:
                return self.endCheckBlock()
        else:
            return self.END_DROPS_OFF

    def hasSideEffects(self):
        if self.type == Token.COMMA:
            if self.last is not None:
                return self.last.hasSideEffects()
            else:
                return True
        elif self.type == Token.HOOK:
            if self.first is None or self.first.next is None or self.first.next.next is None:
                Kit.codeBug()
            return self.first.next.hasSideEffects() and self.first.next.next.hasSideEffects()
        elif self.type == Token.SET_REF_OP:
            return True
        else:
            return False

    #@overloaded
    def toString(self):
        if Token.printTrees:
            sb = StringBuffer()
            self.toString(ObjToIntMap(), sb)
            return str(sb)
        return str(self.type)
    """
    @toString.register(object, ObjToIntMap, StringBuffer)
    def toString_0(self, printIds, sb):
        if Token.printTrees:
            sb.append(Token.name(self.type))
            if isinstance(self, (StringNode)):
                sb.append(' ')
                sb.append(self.getString())
            else:
                if isinstance(self, (ScriptOrFnNode)):
                    sof = self
                    if isinstance(self, (FunctionNode)):
                        fn = self
                        sb.append(' ')
                        sb.append(fn.getFunctionName())
                    sb.append(" [source name: ")
                    sb.append(sof.getSourceName())
                    sb.append("] [encoded source length: ")
                    sb.append(sof.getEncodedSourceEnd() - sof.getEncodedSourceStart())
                    sb.append("] [base line: ")
                    sb.append(sof.getBaseLineno())
                    sb.append("] [end line: ")
                    sb.append(sof.getEndLineno())
                    sb.append(']')
                else:
                    if isinstance(self, (Jump)):
                        jump = self
                        if (self.type == Token.BREAK) or (self.type == Token.CONTINUE):
                            sb.append(" [label: ")
                            self.appendPrintId(jump.getJumpStatement(), printIds, sb)
                            sb.append(']')
                        else:
                            if (self.type == Token.TRY):
                                catchNode = jump.target
                                finallyTarget = jump.getFinally()
                                if catchNode is not None:
                                    sb.append(" [catch: ")
                                    self.appendPrintId(catchNode, printIds, sb)
                                    sb.append(']')
                                if finallyTarget is not None:
                                    sb.append(" [finally: ")
                                    self.appendPrintId(finallyTarget, printIds, sb)
                                    sb.append(']')
                            else:
                                if (self.type == Token.LABEL) or (self.type == Token.LOOP) or (self.type == Token.SWITCH):
                                    sb.append(" [break: ")
                                    self.appendPrintId(jump.target, printIds, sb)
                                    sb.append(']')
                                    if (self.type == Token.LOOP):
                                        sb.append(" [continue: ")
                                        self.appendPrintId(jump.getContinue(), printIds, sb)
                                        sb.append(']')
                                else:
                                    sb.append(" [target: ")
                                    self.appendPrintId(jump.target, printIds, sb)
                                    sb.append(']')
                    else:
                        if (self.type == Token.NUMBER):
                            sb.append(' ')
                            sb.append(self.getDouble())
                        else:
                            if (self.type == Token.TARGET):
                                sb.append(' ')
                                self.appendPrintId(self, printIds, sb)
            if (self.lineno != -1):
                sb.append(' ')
                sb.append(self.lineno)
            ## for-while
            x = self.propListHead
            while x is not None:
                self.type = x.type
                sb.append(" [")
                sb.append(self.propToString(self.type))
                sb.append(": ")
                value = ""
                if self.type == self.TARGETBLOCK_PROP:
                    value = "target block property"
                    break
                elif self.type == self.LOCAL_BLOCK_PROP:
                    value = "last local block"
                    break
                elif self.type == self.ISNUMBER_PROP:
                    if x.intValue == self.BOTH:
                        value = "both"
                        break
                    elif x.intValue == self.RIGHT:
                        value = "right"
                        break
                    elif x.intValue == self.LEFT:
                        value = "left"
                        break
                    else:
                        raise Kit.codeBug()
                    break
                elif self.type == self.SPECIALCALL_PROP:
                    if x.intValue == self.SPECIALCALL_EVAL:
                        value = "eval"
                        break
                    elif x.intValue == self.SPECIALCALL_WITH:
                        value = "with"
                        break
                    else:
                        raise Kit.codeBug()
                    break
                else:
                    obj = x.objectValue
                    if obj is not None:
                        value = str(obj)
                    else:
                        value = str(x.intValue)
                    break
                sb.append(value)
                sb.append(']')
                x = x.next
    """
    def toStringTree(self, treeTop):
        if Token.printTrees:
            sb = StringBuffer()
            self.toStringTreeHelper(treeTop, self, None, 0, sb)
            return str(sb)
        return

    @classmethod
    def toStringTreeHelper(cls, treeTop,
                                n,
                                printIds,
                                level,
                                sb):
        if Token.printTrees:
            if printIds is None:
                printIds = ObjToIntMap()
                cls.generatePrintIds(treeTop, printIds)
            ## for-while
            i = 0
            while (i != level):
                sb.append("    ")
                i += 1
            n.cls.toString(printIds, sb)
            sb.append('\n')
            ## for-while
            cursor = n.cls.getFirstChild()
            while cursor is not None:
                if (cursor.cls.getType() == Token.FUNCTION):
                    fnIndex = cursor.cls.getExistingIntProp(Node.cls.FUNCTION_PROP)
                    fn = treeTop.getFunctionNode(fnIndex)
                    cls.toStringTreeHelper(fn, fn, None, level + 1, sb)
                else:
                    cls.toStringTreeHelper(treeTop, cursor, printIds, level + 1, sb)
                cursor = cursor.cls.getNext()

    #@classmethod
    def generatePrintIds(cls, n, map):
        if Token.printTrees:
            map.put(n, len(map))
            ## for-while
            cursor = n.cls.getFirstChild()
            while cursor is not None:
                cls.generatePrintIds(cursor, map)
                cursor = cursor.cls.getNext()

    @classmethod
    def appendPrintId(cls, n, printIds, sb):
        if Token.printTrees:
            if n is not None:
                id = printIds[n, -1]
                sb.append('#')
                if (id != -1):
                    sb.append(id + 1)
                else:
                    sb.append("<not_available>")

    type = 0
    next = None
    first = None
    last = None
    lineno = -1
    propListHead = None#PropListItem()

    def get_labelId(self):
        if (self.type != Token.TARGET):
            Kit.codeBug()
        return self.getIntProp(self.LABEL_ID_PROP, -1)

    def set_labelId(self, labelId):
        if (self.type != Token.TARGET):
            Kit.codeBug()
        self.putIntProp(self.LABEL_ID_PROP, self.labelId)

    labelId = property(get_labelId, set_labelId)




class PropListItem(object):
        """ generated source for PropListItem

        """
        next = None
        type = 0
        intValue = 0
        objectValue = None
        
class Jump(Node):
    """ generated source for Jump

    """

    #@overloaded
    def __init__(self, *args):
        Node.__init__(self, *args)
        pass

    """
    @__init__.register(object, int, int)
    def __init___0(self, type, lineno):
        pass

    @__init__.register(object, int, Node)
    def __init___1(self, type, child):
        pass

    @__init__.register(object, int, Node, int)
    def __init___2(self, type, child, lineno):
        pass
    """

    def getJumpStatement(self):
        if not (self.type == Token.BREAK) or (self.type == Token.CONTINUE):
            Kit.codeBug()
        return self.jumpNode

    def setJumpStatement(self, jumpStatement):
        if not ((self.type == Token.BREAK) or (self.type == Token.CONTINUE)):
            Kit.codeBug()
        if jumpStatement is None:
            Kit.codeBug()
        if self.jumpNode is not None:
            Kit.codeBug()
        self.jumpNode = jumpStatement

    def getDefault(self):
        if not (self.type == Token.SWITCH):
            Kit.codeBug()
        return self.target2

    def setDefault(self, defaultTarget):
        if not (self.type == Token.SWITCH):
            Kit.codeBug()
        if (defaultTarget.type != Token.TARGET):
            Kit.codeBug()
        if self.target2 is not None:
            Kit.codeBug()
        self.target2 = defaultTarget

    def getFinally(self):
        if not (self.type == Token.TRY):
            Kit.codeBug()
        return self.target2

    def setFinally(self, finallyTarget):
        if not (self.type == Token.TRY):
            Kit.codeBug()
        if (finallyTarget.type != Token.TARGET):
            Kit.codeBug()
        if self.target2 is not None:
            Kit.codeBug()
        self.target2 = finallyTarget

    def getLoop(self):
        if not (self.type == Token.LABEL):
            Kit.codeBug()
        return self.jumpNode

    def setLoop(self, loop):
        if not (self.type == Token.LABEL):
            Kit.codeBug()
        if loop is None:
            Kit.codeBug()
        if self.jumpNode is not None:
            Kit.codeBug()
        self.jumpNode = loop

    def getContinue(self):
        if (self.type != Token.LOOP):
            Kit.codeBug()
        return self.target2

    def setContinue(self, continueTarget):
        if (self.type != Token.LOOP):
            Kit.codeBug()
        if (continueTarget.type != Token.TARGET):
            Kit.codeBug()
        if self.target2 is not None:
            Kit.codeBug()
        self.target2 = continueTarget

    target = None#Node()
    target2 = None#Node()
    jumpNode = None#Jump()

class StringNode(Node):
    """ generated source for StringNode

    """

    def __init__(self, type, strval):
        self.strval = strval
        Node.__init__(self, type)

    str = ""
class NumberNode(Node):
    """ generated source for NumberNode

    """

    def __init__(self, number):
        self.number = number
        Node.__init__(self, Token.NUMBER)
        #Node.__init__(self, number)

    number = None #float()
    
    
