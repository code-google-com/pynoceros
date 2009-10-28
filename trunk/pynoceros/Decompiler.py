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

import struct


from Token import Token


"""
/**
 * The following class save decompilation information about the source.
 * Source information is returned from the parser as a String
 * associated with function nodes and with the toplevel script.  When
 * saved in the constant pool of a class, this string will be UTF-8
 * encoded, and token values will occupy a single byte.

 * Source is saved (mostly) as token numbers.  The tokens saved pretty
 * much correspond to the token stream of a 'canonical' representation
 * of the input program, as directed by the parser.  (There were a few
 * cases where tokens could have been left out where decompiler could
 * easily reconstruct them, but I left them in for clarity).  (I also
 * looked adding source collection to TokenStream instead, where I
 * could have limited the changes to a few lines in getToken... but
 * this wouldn't have saved any space in the resulting source
 * representation, and would have meant that I'd have to duplicate
 * parser logic in the decompiler to disambiguate situations where
 * newlines are important.)  The function decompile expands the
 * tokens back into their string representations, using simple
 * lookahead to correct spacing and indentation.
 *
 * Assignments are saved as two-token pairs (Token.ASSIGN, op). Number tokens
 * are stored inline, as a NUMBER token, a character representing the type, and
 * either 1 or 4 characters representing the bit-encoding of the number.  String
 * types NAME, STRING and OBJECT are currently stored as a token type,
 * followed by a character giving the length of the string (assumed to
 * be less than 2^16), followed by the characters of the string
 * inlined into the source string.  Changing this to some reference to
 * to the string in the compiled class' constant pool would probably
 * save a lot of space... but would require some method of deriving
 * the final constant pool entry from information available at parse
 * time.
 */
"""

class Decompiler(object):
    """ generated source for Decompiler

    """
    ONLY_BODY_FLAG = 1 << 0
    TO_SOURCE_FLAG = 1 << 1
    INITIAL_INDENT_PROP = 1
    INDENT_GAP_PROP = 2
    CASE_GAP_PROP = 3
    FUNCTION_END = Token.LAST_TOKEN + 1

    def getEncodedSource(self):
        return self.sourceToString(0)

    def getCurrentOffset(self):
        return self.sourceTop

    def markFunctionStart(self, functionType):
        savedOffset = self.getCurrentOffset()
        self.addToken(Token.FUNCTION)
        self.append(functionType)
        return savedOffset

    def markFunctionEnd(self, functionStart):
        offset = self.getCurrentOffset()
        self.append(self.FUNCTION_END)
        return offset
        
    def addToken(self, token):
        if not (0 <= token and token <= Token.LAST_TOKEN):
            raise IllegalArgumentException();
        self.append(token)
        
    def addEOL(self, token):
        if not (0 <= token and token <= Token.LAST_TOKEN):
            raise IllegalArgumentException();

        self.append(token);
        self.append(Token.EOL);

    def addName(self, strval):
        self.addToken(Token.NAME)
        self.appendString(strval)
        
    def addNumber(self, n):
        self.addToken(Token.NUMBER)
        #TODO: Add this token to the sourceBuffer
        """
        Java version saves three different formats
        - "D" double
        - "S" short
        - "J" long

        We use:
        - "F" float (store as HEX)
        - "B" 8-bit character (unsigned)
        - "S" short (16 bits) 
        - "I" integer - store 64 bits, 

        apparently negative values are prefixed by Token.NEG already

        - store integer-valued floats as ints
        """
        if isinstance(n, int) or int(n) == n:
            # unsinged
            if n < 256:
                self.append(ord("B"))
                self.append(n)
            elif 0 <= n < 65536: #2**16
                self.append(ord("S"))
                self.append((n>>8))
                self.append(n%256)
            else:
                if (n >> 64) > 0:
                    raise ValueError("Integer Overflow")
                self.append(ord("I"))
                for step in range(64,0,-8):
                    self.append((n>>step)%256)
        else:
            self.append(ord("F"))
            # float packed as double (8 bytes)
            s = struct.pack("d",n)
            # sidestep the append call
            self.sourceBuffer = self.sourceBuffer + s

    def addString(self, strval):
        self.addToken(Token.STRING)
        self.appendString(strval)

    def addRegexp(self, regexp, flags):
        self.addToken(Token.REGEXP)
        self.appendString('/' + regexp + '/' + flags)

    def addJScriptConditionalComment(self, strval):
        self.addToken(Token.CONDCOMMENT)
        self.sourceBuffer.appendString(strval)

    def addPreservedComment(self, strval):
        self.addToken(Token.KEEPCOMMENT)
        self.sourceBuffer = self.sourceBuffer + strval

    def append(self, c):
        #if (self.sourceTop == len(self.sourceBuffer)):
        #    increaseSourceCapacity(self.sourceTop + 1)
        #self.sourceBuffer[self.sourceTop] = c
        #self.sourceTop += 1
        self.sourceBuffer = self.sourceBuffer + chr(c)

    def sourceToString(self, offset):
        #import pdb;pdb.set_trace()
        #if offset < 0 or self.sourceTop < offset:
        if offset < 0 or len(self.sourceBuffer) < offset:
            Kit.codeBug()
        return str(self.sourceBuffer)[offset:]#[offset: self.sourceTop]
        
    def appendString(self, s):
        """store strings as :
            [String Length] [string]
           
           - for each byte in length, the high bit being set marks the next byte
             as being part of the length
           
           - I'm kind of ignoring encoding for now (as in not testing it)
           but I hope it'll just drop out nicely by storing the entire string
           buffer as unicode.
           
        """
        
        # The java version uses chars but does the split between byte lengths
        # every 0x8000 - so I'm a little Confused (TimW)
        # I'm doing the split every 0x00800 .
        l = len(s)
        string_length_string = ""
        add_length_byte = True
        final_byte = True
        while add_length_byte:
            if l < 0x0080:
                # add this one, but that's it.
                add_length_byte = False
            
            byte = l%0x0080
            if not final_byte:
                byte = byte | 0x0080
            else:
                final_byte = False
                
            string_length_string = chr(byte) + string_length_string
            l = l >> 7
       
        # order important - outer concatination is expensive
        self.sourceBuffer = self.sourceBuffer + ( \
                string_length_string + s)

    @classmethod
    def decompile(cls, source, flags, properties):
        length = len(source)
        if (length == 0):
            return ""
        indent = properties.getInt(cls.INITIAL_INDENT_PROP, 0)
        if indent < 0:
            raise IllegalArgumentException()
        indentGap = properties.getInt(cls.INDENT_GAP_PROP, 4)
        if indentGap < 0:
            raise IllegalArgumentException()
        caseGap = properties.getInt(cls.CASE_GAP_PROP, 2)
        if caseGap < 0:
            raise IllegalArgumentException()
        result = StringBuffer()
        justFunctionBody = (0 != flags & Decompiler.cls.ONLY_BODY_FLAG)
        toSource = (0 != flags & Decompiler.cls.TO_SOURCE_FLAG)
        if cls.printSource:
            System.err.println("length:" + length)
            ## for-while
            i = 0
            while i < length:
                tokenname = None
                if Token.printNames:
                    tokenname = Token.name(source.charAt(i))
                if tokenname is None:
                    tokenname = "---"
                pad = "\t" if len(tokenname) > 7 else "\t\t"
                System.err.println(tokenname + pad + source.charAt(i) + "\t'" + ScriptRuntime.escapeString(source.substring(i, i + 1)) + "'")
                i += 1
            System.err.println()
        braceNesting = 0
        afterFirstEOL = False
        i = 0
        topFunctionType = 0
        if (source.charAt(i) == Token.SCRIPT):
            i += 1
            topFunctionType = -1
        else:
            topFunctionType = source.charAt(i + 1)
        if not toSource:
            result.cls.append('\n')
            ## for-while
            j = 0
            while j < indent:
                result.cls.append(' ')
                j += 1
        else:
            if (topFunctionType == FunctionNode.FUNCTION_EXPRESSION):
                result.cls.append('(')
        while i < length:
            if source[i] in (Token.GET,
                             Token.SET):
                result.cls.append("get " if (source.charAt(i) == Token.GET) else "set ")
                i += 1
                i = cls.printSourceString(source, i + 1, False, result)
                i += 1
                break
            elif source.charAt(i) in( Token.NAME, Token.REGEXP):
                i = cls.printSourceString(source, i + 1, False, result)
                continue
            elif source.charAt(i) == Token.STRING:
                i = cls.printSourceString(source, i + 1, True, result)
                continue
            elif source.charAt(i) == Token.NUMBER:
                i = cls.printSourceNumber(source, i + 1, result)
                continue
            elif source.charAt(i) == Token.TRUE:
                result.cls.append("true")
                break
            elif source.charAt(i) == Token.FALSE:
                result.cls.append("false")
                break
            elif source.charAt(i) == Token.NULL:
                result.cls.append("null")
                break
            elif source.charAt(i) == Token.THIS:
                result.cls.append("this")
                break
            elif source.charAt(i) == Token.FUNCTION:
                i += 1
                result.cls.append("function ")
                break
            elif source.charAt(i) == cls.FUNCTION_END:
                break
            elif source.charAt(i) == Token.COMMA:
                result.cls.append(", ")
                break
            elif source.charAt(i) == Token.LC:
                braceNesting += 1
                if (Token.EOL == cls.getNext(source, length, i)):
                    indent += indentGap
                result.cls.append('{')
                break
            elif source.charAt(i) == Token.RC:
                braceNesting -= 1
                if justFunctionBody and (braceNesting == 0):
                    break
                result.cls.append('}')
                if cls.getNext(source, length, i) == cls.FUNCTION_END:
                    indent -= indentGap
                    break
                elif cls.getNext(source, length, i) == Token.ELSE:
                    indent -= indentGap
                    result.cls.append(' ')
                    break
                break
            elif source.charAt(i) == Token.LP:
                result.cls.append('(')
                break
            elif source.charAt(i) == Token.RP:
                result.cls.append(')')
                if (Token.LC == cls.getNext(source, length, i)):
                    result.cls.append(' ')
                break
            elif source.charAt(i) == Token.LB:
                result.cls.append('[')
                break
            elif source.charAt(i) == Token.RB:
                result.cls.append(']')
                break
            elif source.charAt(i) == Token.EOL:
                if toSource:
                    break
                newLine = True
                if not afterFirstEOL:
                    afterFirstEOL = True
                    if justFunctionBody:
                        result.setLength(0)
                        indent -= indentGap
                        newLine = False
                if newLine:
                    result.cls.append('\n')
                if i + 1 < length:
                    less = 0
                    nextToken = source.charAt(i + 1)
                    if (nextToken == Token.CASE) or (nextToken == Token.DEFAULT):
                        less = indentGap - caseGap
                    else:
                        if (nextToken == Token.RC):
                            less = indentGap
                        else:
                            if (nextToken == Token.NAME):
                                afterName = cls.getSourceStringEnd(source, i + 2)
                                if (source.charAt(afterName) == Token.COLON):
                                    less = indentGap
                    ## for-while
                    while less < indent:
                        result.cls.append(' ')
                        less += 1
                break
            elif source.charAt(i) == Token.DOT:
                result.cls.append('.')
                break
            elif source.charAt(i) == Token.NEW:
                result.cls.append("new ")
                break
            elif source.charAt(i) == Token.DELPROP:
                result.cls.append("delete ")
                break
            elif source.charAt(i) == Token.IF:
                result.cls.append("if ")
                break
            elif source.charAt(i) == Token.ELSE:
                result.cls.append("else ")
                break
            elif source.charAt(i) == Token.FOR:
                result.cls.append("for ")
                break
            elif source.charAt(i) == Token.IN:
                result.cls.append(" in ")
                break
            elif source.charAt(i) == Token.WITH:
                result.cls.append("with ")
                break
            elif source.charAt(i) == Token.WHILE:
                result.cls.append("while ")
                break
            elif source.charAt(i) == Token.DO:
                result.cls.append("do ")
                break
            elif source.charAt(i) == Token.TRY:
                result.cls.append("try ")
                break
            elif source.charAt(i) == Token.CATCH:
                result.cls.append("catch ")
                break
            elif source.charAt(i) == Token.FINALLY:
                result.cls.append("finally ")
                break
            elif source.charAt(i) == Token.THROW:
                result.cls.append("throw ")
                break
            elif source.charAt(i) == Token.SWITCH:
                result.cls.append("switch ")
                break
            elif source.charAt(i) == Token.BREAK:
                result.cls.append("break")
                if (Token.NAME == cls.getNext(source, length, i)):
                    result.cls.append(' ')
                break
            elif source.charAt(i) == Token.CONTINUE:
                result.cls.append("continue")
                if (Token.NAME == cls.getNext(source, length, i)):
                    result.cls.append(' ')
                break
            elif source.charAt(i) == Token.CASE:
                result.cls.append("case ")
                break
            elif source.charAt(i) == Token.DEFAULT:
                result.cls.append("default")
                break
            elif source.charAt(i) == Token.RETURN:
                result.cls.append("return")
                if (Token.SEMI != cls.getNext(source, length, i)):
                    result.cls.append(' ')
                break
            elif source.charAt(i) == Token.VAR:
                result.cls.append("var ")
                break
            elif source.charAt(i) == Token.SEMI:
                result.cls.append(';')
                if (Token.EOL != cls.getNext(source, length, i)):
                    result.cls.append(' ')
                break
            elif source.charAt(i) == Token.ASSIGN:
                result.cls.append(" = ")
                break
            elif source.charAt(i) == Token.ASSIGN_ADD:
                result.cls.append(" += ")
                break
            elif source.charAt(i) == Token.ASSIGN_SUB:
                result.cls.append(" -= ")
                break
            elif source.charAt(i) == Token.ASSIGN_MUL:
                result.cls.append(" *= ")
                break
            elif source.charAt(i) == Token.ASSIGN_DIV:
                result.cls.append(" /= ")
                break
            elif source.charAt(i) == Token.ASSIGN_MOD:
                result.cls.append(" %= ")
                break
            elif source.charAt(i) == Token.ASSIGN_BITOR:
                result.cls.append(" |= ")
                break
            elif source.charAt(i) == Token.ASSIGN_BITXOR:
                result.cls.append(" ^= ")
                break
            elif source.charAt(i) == Token.ASSIGN_BITAND:
                result.cls.append(" &= ")
                break
            elif source.charAt(i) == Token.ASSIGN_LSH:
                result.cls.append(" <<= ")
                break
            elif source.charAt(i) == Token.ASSIGN_RSH:
                result.cls.append(" >>= ")
                break
            elif source.charAt(i) == Token.ASSIGN_URSH:
                result.cls.append(" >>>= ")
                break
            elif source.charAt(i) == Token.HOOK:
                result.cls.append(" ? ")
                break
            elif source.charAt(i) == Token.OBJECTLIT:
                result.cls.append(':')
                break
            elif source.charAt(i) == Token.COLON:
                if (Token.EOL == cls.getNext(source, length, i)):
                    result.cls.append(':')
                else:
                    result.cls.append(" : ")
                break
            elif source.charAt(i) == Token.OR:
                result.cls.append(" || ")
                break
            elif source.charAt(i) == Token.AND:
                result.cls.append(" && ")
                break
            elif source.charAt(i) == Token.BITOR:
                result.cls.append(" | ")
                break
            elif source.charAt(i) == Token.BITXOR:
                result.cls.append(" ^ ")
                break
            elif source.charAt(i) == Token.BITAND:
                result.cls.append(" & ")
                break
            elif source.charAt(i) == Token.SHEQ:
                result.cls.append(" === ")
                break
            elif source.charAt(i) == Token.SHNE:
                result.cls.append(" !== ")
                break
            elif source.charAt(i) == Token.EQ:
                result.cls.append(" == ")
                break
            elif source.charAt(i) == Token.NE:
                result.cls.append(" != ")
                break
            elif source.charAt(i) == Token.LE:
                result.cls.append(" <= ")
                break
            elif source.charAt(i) == Token.LT:
                result.cls.append(" < ")
                break
            elif source.charAt(i) == Token.GE:
                result.cls.append(" >= ")
                break
            elif source.charAt(i) == Token.GT:
                result.cls.append(" > ")
                break
            elif source.charAt(i) == Token.INSTANCEOF:
                result.cls.append(" instanceof ")
                break
            elif source.charAt(i) == Token.LSH:
                result.cls.append(" << ")
                break
            elif source.charAt(i) == Token.RSH:
                result.cls.append(" >> ")
                break
            elif source.charAt(i) == Token.URSH:
                result.cls.append(" >>> ")
                break
            elif source.charAt(i) == Token.TYPEOF:
                result.cls.append("typeof ")
                break
            elif source.charAt(i) == Token.VOID:
                result.cls.append("void ")
                break
            elif source.charAt(i) == Token.CONST:
                result.cls.append("const ")
                break
            elif source.charAt(i) == Token.NOT:
                result.cls.append('!')
                break
            elif source.charAt(i) == Token.BITNOT:
                result.cls.append('~')
                break
            elif source.charAt(i) == Token.POS:
                result.cls.append('+')
                break
            elif source.charAt(i) == Token.NEG:
                result.cls.append('-')
                break
            elif source.charAt(i) == Token.INC:
                result.cls.append("++")
                break
            elif source.charAt(i) == Token.DEC:
                result.cls.append("--")
                break
            elif source.charAt(i) == Token.ADD:
                result.cls.append(" + ")
                break
            elif source.charAt(i) == Token.SUB:
                result.cls.append(" - ")
                break
            elif source.charAt(i) == Token.MUL:
                result.cls.append(" * ")
                break
            elif source.charAt(i) == Token.DIV:
                result.cls.append(" / ")
                break
            elif source.charAt(i) == Token.MOD:
                result.cls.append(" % ")
                break
            elif source.charAt(i) == Token.COLONCOLON:
                result.cls.append("::")
                break
            elif source.charAt(i) == Token.DOTDOT:
                result.cls.append("..")
                break
            elif source.charAt(i) == Token.DOTQUERY:
                result.cls.append(".(")
                break
            elif source.charAt(i) == Token.XMLATTR:
                result.cls.append('@')
                break
            else:
                raise RuntimeException("Token: " + Token.name(source.charAt(i)))
                
            i += 1
        if not toSource:
            if not justFunctionBody:
                result.cls.append('\n')
        else:
            if (topFunctionType == FunctionNode.FUNCTION_EXPRESSION):
                result.cls.append(')')
        return str(result)

    @classmethod
    def getNext(cls, source, length, i):
        return source.charAt(i + 1) if i + 1 < length else Token.EOF

    @classmethod
    def getSourceStringEnd(cls, source, offset):
        return cls.printSourceString(source, offset, False, None)

    @classmethod
    def printSourceString(cls, source, offset, asQuotedString, sb):
        length = source.charAt(offset)
        offset += 1
        if (0x8000 & length != 0):
            length = 0x7FFF & length << 16 | source.charAt(offset)
            offset += 1
        if sb is not None:
            strval = source.substring(offset, offset + length)
            if not asQuotedString:
                sb.cls.append(strval)
            else:
                sb.cls.append('"')
                sb.cls.append(ScriptRuntime.escapeString(strval))
                sb.cls.append('"')
        return offset + length

    @classmethod
    def printSourceNumber(cls, source, offset, sb):
        number = 0.0
        type = source.charAt(offset)
        offset += 1
        if (type == 'S'):
            if sb is not None:
                ival = source.charAt(offset)
                number = ival
            offset += 1
        else:
            if (type == 'J') or (type == 'D'):
                if sb is not None:
                    lbits = long()
                    lbits = source.charAt(offset) << 48
                    lbits |= source.charAt(offset + 1) << 32
                    lbits |= source.charAt(offset + 2) << 16
                    lbits |= source.charAt(offset + 3)
                    if (type == 'J'):
                        number = lbits
                    else:
                        number = Double.longBitsToDouble(lbits)
                offset += 4
            else:
                raise RuntimeException()
        if sb is not None:
            sb.cls.append(ScriptRuntime.numberToString(number, 10))
        return offset

    sourceBuffer = ""#[str() for __idx0 in range(128)]
    sourceTop = 0
    printSource = False

