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

from Node import Node
from ObjToIntMap import ObjToIntMap

class ScriptOrFnNode(Node):
    """ generated source for ScriptOrFnNode

    """

    def __init__(self, nodeType):
        Node.__init__(self, nodeType)
        self.itsVariableNames = ObjToIntMap(11)
        self.itsVariables = []
        self.itsConst = []
        self.functions = []
        self.regexps = []

    def getSourceName(self):
        return self.sourceName

    def setSourceName(self, sourceName):
        self.sourceName = self.sourceName

    def getEncodedSourceStart(self):
        return self.encodedSourceStart

    def getEncodedSourceEnd(self):
        return self.encodedSourceEnd

    def setEncodedSourceBounds(self, start, end):
        self.encodedSourceStart = start
        self.encodedSourceEnd = end

    def getBaseLineno(self):
        return self.baseLineno

    def setBaseLineno(self, lineno):
        if lineno < 0 or self.baseLineno >= 0:
            Kit.codeBug()
        self.baseLineno = lineno

    def getEndLineno(self):
        return self.endLineno

    def setEndLineno(self, lineno):
        if lineno < 0 or self.endLineno >= 0:
            Kit.codeBug()
        self.endLineno = lineno

    def getFunctionCount(self):
        if self.functions is None:
            return 0
        return len(self.functions)

    def getFunctionNode(self, i):
        return self.functions[i]

    def addFunction(self, fnNode):
        if fnNode is None:
            Kit.codeBug()
        if self.functions is None:
            self.functions = []
        self.functions.append(fnNode)
        return len(self.functions) - 1

    def getRegexpCount(self):
        if self.regexps is None:
            return 0
        return len(self.regexps) / 2

    def getRegexpString(self, index):
        return self.regexps[index * 2]

    def getRegexpFlags(self, index):
        return self.regexps[index * 2 + 1]

    def addRegexp(self, string, flags):
        if string is None:
            Kit.codeBug()
        if self.regexps is None:
            self.regexps = []
        self.regexps.append(string)
        self.regexps.append(flags)
        return len(self.regexps) / 2 - 1

    def hasParamOrVar(self, name):
        return self.itsVariableNames.has(name)

    def getParamOrVarIndex(self, name):
        return self.itsVariableNames.get(name, -1)

    def getParamOrVarName(self, index):
        return self.itsVariables[index]

    def getParamCount(self):
        return self.varStart

    def getParamAndVarCount(self):
        return len(self.itsVariables)

    def getParamAndVarNames(self):
        N = len(self.itsVariables)
        if (N == 0):
            return ScriptRuntime.emptyStrings
        array = [String() for __idx0 in range(N)]
        self.itsVariables.toArray(array)
        return array

    def getParamAndVarConst(self):
        N = len(self.itsVariables)
        array = [bool() for __idx0 in range(N)]
        ## for-while
        i = 0
        while i < N:
            if self.itsConst[i] is not None:
                array[i] = True
            i += 1
        return array

    def addParam(self, name):
        #Check addparam is not called after addLocal
        if (self.varStart != len(self.itsVariables)):
            Kit.codeBug()
        # Allow non-unique parameter names: use the last occurrence (parser
        # will warn about dups)
        self.varStart += 1
        index = self.varStart
        self.itsVariables.append(name)
        self.itsConst.append(None)
        self.itsVariableNames.put(name, index)

    NO_DUPLICATE = 1
    DUPLICATE_VAR = 0
    DUPLICATE_PARAMETER = -1
    DUPLICATE_CONST = -2

    def addVar(self, name):
        #vIndex = self.itsVariableNames[name, -1]
        vIndex = self.itsVariableNames.get(name, -1)
        if (vIndex != -1):
            if vIndex >= self.varStart:
                v = self.itsConst[vIndex]
                if v is not None:
                    return self.DUPLICATE_CONST
                else:
                    return self.DUPLICATE_VAR
            else:
                return self.DUPLICATE_PARAMETER
        index = len(self.itsVariables)
        self.itsVariables.append(name)
        self.itsConst.append(None)
        self.itsVariableNames.put(name, index)
        return self.NO_DUPLICATE

    def addConst(self, name):
        #vIndex = self.itsVariableNames[name, -1]
        vIndex = self.itsVariableNames.get(name, -1)
        if (vIndex != -1):
            return False
        index = len(self.itsVariables)
        self.itsVariables.append(name)
        self.itsConst.append(name)
        self.itsVariableNames.put(name, index)
        return True

    def removeParamOrVar(self, name):
        #i = self.itsVariableNames[name, -1]
        i = self.itsVariableNames.get(name,-1)
        if (i != -1):
            self.itsVariables.remove(i)
            self.itsVariableNames.remove(name)
            iter = self.itsVariableNames.newIterator()
            ## for-while
            while not iter.done():
                v = iter.getValue()
                if v > i:
                    iter.setValue(v - 1)
                iter.next()

    def getCompilerData(self):
        return self.compilerData

    def setCompilerData(self, data):
        if data is None:
            raise IllegalArgumentException()
        if self.compilerData is not None:
            raise IllegalStateException()
        self.compilerData = data

    encodedSourceStart = 0
    encodedSourceEnd = 0
    sourceName = ""
    baseLineno = -1
    endLineno = -1
    functions = None #[]#ObjArray()
    regexps = None #[]#ObjArray()
    itsVariables = None#ObjArray()
    itsConst = None#ObjArray()
    itsVariableNames = None
    varStart = 0
    compilerData = []#Object()

