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

from ObjToIntMap import ObjToIntMap
from Token import Token
from ScriptRuntime import ScriptRuntime

Token.printNames = True
def printval(f):
    def wrap(*args, **kwargs):
        r = f(*args, **kwargs)
        return r
    return wrap

EOF_CHAR = -1;

class TokenStream(object):
    """ generated source for TokenStream

    """
    EOF_CHAR = -1

    def __init__(self, parser, sourceReader, sourceString, lineno):
        self.parser = parser
        self.lineno = lineno
        if self.sourceReader is not None:
            if self.sourceString is not None:
                Kit.codeBug()
            self.sourceReader = self.sourceReader
            self.sourceBuffer = [strval() for __idx0 in range(512)]
            self.sourceEnd = 0
        else:
            if self.sourceString is None:
                Kit.codeBug()
            self.sourceString = sourceString
            self.sourceEnd = len(self.sourceString)
        # origionally 0
        self.sourceCursor = -1

    def tokenToString(self, token):
        if Token.printTrees:
            name = Token.name(token)
            if token in (Token.REGEXP,
                         Token.STRING,
                         Token.NAME):
                return name + " `" + self.string + "'"
            elif token == Token.NUMBER:
                return "NUMBER " + self.number
            return name
        return ""

    @classmethod
    def isKeyword(cls, s):
        return (Token.EOF != stringToKeyword(s))
        
    def stringToKeyword(self, name):
        length = len(name)
        token_id = 0
        
        if length == 2:
            if name == "if":
                return Token.IF
            elif name == "in":
                return Token.IN
            elif name == "do":
                return Token.DO
                
        elif length == 3:
            if name == "var":
                return Token.VAR
            elif name == "for":
                return Token.FOR
            elif name == "int":
                return Token.RESERVED
            elif name == "new":
                return Token.NEW
            elif name == "try":
                return Token.TRY
        
        # Strings of length 4+ should really be searched for in a single dict.
        elif length == 4:
            token_id = {"byte":Token.RESERVED,
             "case":Token.CASE,
             "char":Token.RESERVED,
             "else":Token.ELSE,
             "enum":Token.RESERVED,
             "goto":Token.RESERVED,
             "long":Token.RESERVED,
             "null":Token.NULL,
             "true":Token.TRUE,
             "this":Token.THIS,
             "void":Token.VOID,
             "with":Token.WITH}.get(name,0)
             
        elif length == 5:
            token_id = {"class":Token.RESERVED,
                       "break":Token.BREAK,
                       "while":Token.WHILE,
                       "false":Token.FALSE,
                       "const":Token.CONST,
                       "final":Token.RESERVED,
                       "float":Token.RESERVED,
                       "short":Token.RESERVED,
                       "super":Token.RESERVED,
                       "throw":Token.THROW,
                       "catch":Token.CATCH}.get(name,0)
                       
        elif length == 6:
            token_id = {"native":Token.RESERVED,
                        "delete":Token.DELPROP,
                        "return":Token.RETURN,
                        "throws":Token.RESERVED,
                        "import":Token.IMPORT,
                        "double":Token.RESERVED,
                        "static":Token.RESERVED,
                        "public":Token.RESERVED,
                        "switch":Token.SWITCH,
                        "export":Token.EXPORT,
                        "typeof":Token.TYPEOF}.get(name,0)
        elif length == 7:
            token_id = {"package": Token.RESERVED,
                        "default": Token.DEFAULT,
                        "finally": Token.FINALLY,
                        "boolean": Token.RESERVED,
                        "private": Token.RESERVED,
                        "extends": Token.RESERVED}.get(name,0)
        elif length == 8:
            token_id = {"abstract":Token.RESERVED,
                        "continue":Token.CONTINUE,
                        "debugger":Token.RESERVED,
                        "function":Token.FUNCTION,
                        "volatile":Token.RESERVED}.get(name,0)
        elif length == 9 or length == 10:
            token_id = {"interface":Token.RESERVED,
                        "protected":Token.RESERVED,
                        "transient":Token.RESERVED,
                        "implements":Token.RESERVED,
                        "instanceof":Token.INSTANCEOF}.get(name,0)
        elif length == 12:
            if name == "synchronized":
                return Token.RESERVED
        if token_id == 0:
            return Token.EOF
        return token_id
        
        """
    private static int stringToKeyword(String name)
    {
// #string_id_map#
// The following assumes that Token.EOF == 0
        final int
            Id_break         = Token.BREAK,
            Id_case          = Token.CASE,
            Id_continue      = Token.CONTINUE,
            Id_default       = Token.DEFAULT,
            Id_delete        = Token.DELPROP,
            Id_do            = Token.DO,
            Id_else          = Token.ELSE,
            Id_export        = Token.EXPORT,
            Id_false         = Token.FALSE,
            Id_for           = Token.FOR,
            Id_function      = Token.FUNCTION,
            Id_if            = Token.IF,
            Id_in            = Token.IN,
            Id_new           = Token.NEW,
            Id_null          = Token.NULL,
            Id_return        = Token.RETURN,
            Id_switch        = Token.SWITCH,
            Id_this          = Token.THIS,
            Id_true          = Token.TRUE,
            Id_typeof        = Token.TYPEOF,
            Id_var           = Token.VAR,
            Id_void          = Token.VOID,
            Id_while         = Token.WHILE,
            Id_with          = Token.WITH,

            // the following are #ifdef RESERVE_JAVA_KEYWORDS in jsscan.c
            Id_abstract      = Token.RESERVED,
            Id_boolean       = Token.RESERVED,
            Id_byte          = Token.RESERVED,
            Id_catch         = Token.CATCH,
            Id_char          = Token.RESERVED,
            Id_class         = Token.RESERVED,
            Id_const         = Token.CONST,
            Id_debugger      = Token.RESERVED,
            Id_double        = Token.RESERVED,
            Id_enum          = Token.RESERVED,
            Id_extends       = Token.RESERVED,
            Id_final         = Token.RESERVED,
            Id_finally       = Token.FINALLY,
            Id_float         = Token.RESERVED,
            Id_goto          = Token.RESERVED,
            Id_implements    = Token.RESERVED,
            Id_import        = Token.IMPORT,
            Id_instanceof    = Token.INSTANCEOF,
            Id_int           = Token.RESERVED,
            Id_interface     = Token.RESERVED,
            Id_long          = Token.RESERVED,
            Id_native        = Token.RESERVED,
            Id_package       = Token.RESERVED,
            Id_private       = Token.RESERVED,
            Id_protected     = Token.RESERVED,
            Id_public        = Token.RESERVED,
            Id_short         = Token.RESERVED,
            Id_static        = Token.RESERVED,
            Id_super         = Token.RESERVED,
            Id_synchronized  = Token.RESERVED,
            Id_throw         = Token.THROW,
            Id_throws        = Token.RESERVED,
            Id_transient     = Token.RESERVED,
            Id_try           = Token.TRY,
            Id_volatile      = Token.RESERVED;

        int id;
        String s = name;
// #generated# Last update: 2001-06-01 17:45:01 CEST
        L0: { id = 0; String X = null; int c;
            L: switch (s.length()) {
            case 7: switch (s.charAt(1)) {
                case 'a': X="package";id=Id_package; break L;
                case 'e': X="default";id=Id_default; break L;
                case 'i': X="finally";id=Id_finally; break L;
                case 'o': X="boolean";id=Id_boolean; break L;
                case 'r': X="private";id=Id_private; break L;
                case 'x': X="extends";id=Id_extends; break L;
                } break L;
            }
            if (X!=null && X!=s && !X.equals(s)) id = 0;
        }
// #/generated#
// #/string_id_map#
        if (id == 0) { return Token.EOF; }
        return id & 0xff;
    }"""

    def getLineno(self):
        return self.lineno

    def getString(self):
        return self.string

    def getNumber(self):
        return self.number

    def eof(self):
        return self.hitEOF
    @printval
    def getToken(self):
        c = 0
        while True:
            while True:
                c = self.getChar()
                if (c == self.EOF_CHAR):
                    return Token.EOF
                else:
                    if (c == '\n'):
                        self.dirtyLine = False
                        return Token.EOL
                    else:
                        if not self.isJSSpace(c):
                            if (c != '-'):
                                self.dirtyLine = True
                            break
            
            if (c == '@'):
                return Token.XMLATTR
            identifierStart = bool()
            isUnicodeEscapeStart = False
            if (c == '\\'):
                c = self.getChar()
                if (c == 'u'):
                    identifierStart = True
                    isUnicodeEscapeStart = True
                    self.stringBufferTop = 0
                else:
                    identifierStart = False
                    self.ungetChar(c)
                    c = '\\'
            else:
                # TODO: check this is the same...
                identifierStart = (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$")
                #identifierStart = Character.isJavaIdentifierStart(c)
                
                if identifierStart:
                    self.stringBufferTop = 0
                    self.addToString(c)
            if identifierStart:
                containsEscape = isUnicodeEscapeStart
                while True:
                    if isUnicodeEscapeStart:
                        escapeVal = 0
                        ## for-while
                        i = 0
                        while (i != 4):
                            c = self.getChar()
                            escapeVal = Kit.xDigitToInt(c, escapeVal)
                            if escapeVal < 0:
                                break
                            i += 1
                        if escapeVal < 0:
                            self.parser.addError("msg.invalid.escape")
                            return Token.ERROR
                        self.addToString(escapeVal)
                        isUnicodeEscapeStart = False
                    else:
                        c = self.getChar()
                        if (c == '\\'):
                            c = self.getChar()
                            if (c == 'u'):
                                isUnicodeEscapeStart = True
                                containsEscape = True
                            else:
                                self.parser.addError("msg.illegal.character")
                                return Token.ERROR
                        else:
                            if (c == self.EOF_CHAR) or \
                                not (c in "abcdefghijklmnopqrstuvwxyz"\
                                          "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
                                           "$1234567890"):
                                #Character.isJavaIdentifierPart(c): <- what it was
                                break
                            self.addToString(c)
                self.ungetChar(c)
                strval = self.getStringFromBuffer()
                if not containsEscape:
                    result = self.stringToKeyword(strval)
                    if (result != Token.EOF):
                        if (result != Token.RESERVED):
                            return result
                        else:
                            if not parser.compilerEnv.isReservedKeywordAsIdentifier():
                                return result
                            else:
                                parser.addWarning("msg.reserved.keyword", strval)
                self.string = intern(strval) #allStrings.intern(strval)
                return Token.NAME
            ##
            # Is it a Number?
            ##
            if c.isdigit() or c == "." and self.peekChar().isdigit():
                num_chars = []
                base = 10
                if c == "0":
                    c = self.getChar()
                    if c == "x" or c == "X":
                        #HEX
                        base = 16
                        c = self.getChar()
                    elif c.isdigit():
                        base = 8
                    else:
                        num_chars.append("0")
                        
                if base == 16:
                    while c in "0123456789abcdefABCDEF":
                        num_chars.append(c)
                        c = self.getChar()
                else:
                    while ord("0") <= ord(c) <= ord("9"):
                        #/*
                        # * We permit 08 and 09 as decimal numbers, which
                        # * makes our behavior a superset of the ECMA
                        # * numeric grammar.  We might not always be so
                        # * permissive, so we warn about it.
                        # */
                        if (base == 8 and c in ("8","9") ):
                            self.parser.addWarning("msg.bad.octal.literal", c);
                            base = 10;
                        num_chars.append(c)
                        c = self.getChar();
                        
                isInteger = True
                if (base == 10 and c in (".","E","e")):
                    isInteger = False
                    if c == ".":
                        while True:
                            num_chars.append(c)
                            c = self.getChar()
                            if not c.isdigit():
                                break
                    if c == "e" or c == "E":
                        num_chars.append(c)
                        c = self.getChar()
                        if c == "+" or c == "-":
                            num_chars.append(c)
                            c = self.getChar()
                        if not c.isdigit():
                            self.parser.addError("msg.missing.exponent")
                            return Token.ERROR
                        while True:
                            num_chars.append(c)
                            c = self.getChar()
                            if not c.isdigit():
                                break 

                    #raise NotImplementedError()
                self.ungetChar(c)
                numString = "".join(num_chars)
                
                dval = 0.0
                # TODO: lots
                if (base == 10 and not isInteger):
                    self.number = float(numString)
                    # TODO: Check this is complete (xEy?)
                    #raise NotImplementedError()
                elif base == 10:
                    self.number = int(numString)
                elif base == 16:
                    # TODO: is this the only way?
                    self.number = eval("0x"+numString)
                else:
                    raise NotImplementedError()
                return Token.NUMBER
                
            ##
            # Is it a string?
            ##
            if (c == '"' or c == '\''):
                #// We attempt to accumulate a string the fast way, by
                #// building it directly out of the reader.  But if there
                #// are any escaped characters in the string, we revert to
                #// building it out of a StringBuffer.
                quoteChar = c
                self.stringBufferTop = 0;

                c = self.getChar();
                while (c != quoteChar):
                    if (c == '\n' or c == self.EOF_CHAR):
                        self.ungetChar(c);
                        self.parser.addError("msg.unterminated.string.lit");
                        return Token.ERROR;

                    if (c == '\\'):
                        #// We've hit an escaped character
                        c = self.getChar();
                        if c in "\\bfnrtvdux":
                            # backslash, backspace, form feed, line feed,
                            # carriage return, horizontal tab, octal seq,
                            # unicode sequence, hex sequence
                            
                            #// Only keep the '\' character for those
                            #// characters that need to be escaped...
                            #// Don't escape quoting characters...
                            self.addToString('\\');
                            self.addToString(c);
                        elif c == "\n":
                            pass
                        else:
                            if (c.isdigit()):
                                # Octal representation of a character
                                # preserve the escaping
                                self.addToString("\\");
                            self.addToString(c);

                    else:

                        self.addToString(c);

                    c = self.getChar();

                str = self.getStringFromBuffer();
                self.string = intern(str);
                #this.string = (String)allStrings.intern(str);
                return Token.STRING;
                
            # LOOKUP DICT
            quick_char_lookup = \
                {";":Token.SEMI,
                 "[":Token.LB,
                 "]":Token.RB,
                 "{":Token.LC,
                 "}":Token.RC,
                 "(":Token.LP,
                 ")":Token.RP,
                 ",":Token.COMMA,
                 "?":Token.HOOK}
                 
            token = quick_char_lookup.get(c,None)
            if token is not None:
                return token
            
            if c == ":":
                if self.matchChar(':'):
                    return Token.COLONCOLON;
                else:
                    return Token.COLON;
            elif c == '.':
                if self.matchChar('.'):
                    return Token.DOTDOT;
                elif self.matchChar('('):
                    return Token.DOTQUERY;
                else:
                    return Token.DOT;
            elif c == '|':
                if self.matchChar('|'):
                    return Token.OR;
                elif self.matchChar('='):
                    return Token.ASSIGN_BITOR;
                else:
                    return Token.BITOR;
            elif c == '^':
                if self.matchChar('='):
                    return Token.ASSIGN_BITXOR;
                else:
                    return Token.BITXOR;
            elif c == '&':
                if self.matchChar('&'):
                    return Token.AND;
                elif self.matchChar('='):
                    return Token.ASSIGN_BITAND;
                else:
                    return Token.BITAND;
            elif c == '=':
                if self.matchChar('='):
                    if self.matchChar('='):
                        return Token.SHEQ;
                    else:
                        return Token.EQ;
                else:
                    return Token.ASSIGN;

            elif c == '!':
                if (self.matchChar('=')):
                    if (self.matchChar('=')):
                        return Token.SHNE;
                    else:
                        return Token.NE;
                else:
                    return Token.NOT;
                    
            elif c ==  '<':
                #/* NB:treat HTML begin-comment as comment-till-eol */
                if (self.matchChar('!')):
                    if (self.matchChar('-')):
                        if (self.matchChar('-')):
                            self.skipLine();
                            continue
                            # was continue retry;
                        self.ungetChar('-');
                    self.ungetChar('!');
                if (self.matchChar('<')):
                    if (self.matchChar('=')):
                        return Token.ASSIGN_LSH;
                    else:
                        return Token.LSH;
                else:
                    if (self.matchChar('=')):
                        return Token.LE;
                    else:
                        return Token.LT;

            elif c == '>':
                if (self.matchChar('>')):
                    if (self.matchChar('>')):
                        if (self.matchChar('=')):
                            return Token.ASSIGN_URSH;
                        else:
                            return Token.URSH;
                    else:
                        if (self.matchChar('=')):
                            return Token.ASSIGN_RSH;
                        else:
                            return Token.RSH;
                else:
                    if (self.matchChar('=')):
                        return Token.GE;
                    else:
                        return Token.GT;

            elif c == '*':
                if (self.matchChar('=')):
                    return Token.ASSIGN_MUL;
                else:
                    return Token.MUL;
                    
                    
            elif c ==  '/':
                #// is it a // comment?
                if (self.matchChar('/')):
                    self.skipLine();
                    continue
                    #continue retry;
                if (self.matchChar('*')):
                    lookForSlash = False;
                    sb = []
                    while True:
                        c = self.getChar();
                        if (c == self.EOF_CHAR):
                            self.parser.addError("msg.unterminated.comment");
                            return Token.ERROR;
                        sb.append(c);
                        if (c == '*'):
                            lookForSlash = True;
                        elif (c == '/'):
                            if (lookForSlash):
                                #sb.pop()
                                #sb.pop()#delete(sb.length()-2, sb.length());
                                s1 = "".join(sb)
                                s2 = s1.strip()#s1.trim();
                                if (s1[0]=="!"):
                                    #// Remove the leading '!'
                                    self.string = s1[1:]
                                    return Token.KEEPCOMMENT;
                                elif (s2.startswith("@cc_on") or \
                                           s2.startswith("@if")    or \
                                           s2.startswith("@elif")  or \
                                           s2.startswith("@else")  or \
                                           s2.startswith("@end")):
                                    self.string = s1;
                                    return Token.CONDCOMMENT;
                                else:
                                    break
                                    #continue retry;
                        else:
                            lookForSlash = False;
                    # Catch breaks from the loop to start looking 
                    # for tokens from the top
                    continue


                if (self.matchChar('=')):
                    return Token.ASSIGN_DIV;
                else:
                    return Token.DIV;

            elif c == '%':
                if (self.matchChar('=')):
                    return Token.ASSIGN_MOD;
                else:
                    return Token.MOD;
            
            elif c == '~':
                return Token.BITNOT;

            elif c == '+':
                if (self.matchChar('=')):
                    return Token.ASSIGN_ADD;
                elif (self.matchChar('+')):
                    return Token.INC;
                else:
                    return Token.ADD;

            elif c == '-':
                if (self.matchChar('=')):
                    c = Token.ASSIGN_SUB;
                elif (self.matchChar('-')):
                    if (not self.dirtyLine):
                        #// treat HTML end-comment after possible whitespace
                        #// after line start as comment-utill-eol
                        if (self.matchChar('>')):
                            self.skipLine();
                            continue; # TODO - is this correct? continue retry 
                                      # (where was retry)
                    c = Token.DEC;
                else:
                    c = Token.SUB;
                self.dirtyLine = True;
                return c;

                

            # N.B. - some should go before the lookup dict part
            print "Token Type not yet done - poke around a bit if wanted"
            #import pdb;pdb.set_trace()
            raise NotImplementedError()
            
            """
            // is it a number?
            if (isDigit(c) || (c == '.' && isDigit(peekChar()))) {

                stringBufferTop = 0;
                int base = 10;

                if (c == '0') {
                    c = getChar();
                    if (c == 'x' || c == 'X') {
                        base = 16;
                        c = getChar();
                    } else if (isDigit(c)) {
                        base = 8;
                    } else {
                        addToString('0');
                    }
                }

                if (base == 16) {
                    while (0 <= Kit.xDigitToInt(c, 0)) {
                        addToString(c);
                        c = getChar();
                    }
                } else {
                    while ('0' <= c && c <= '9') {
                        /*
                         * We permit 08 and 09 as decimal numbers, which
                         * makes our behavior a superset of the ECMA
                         * numeric grammar.  We might not always be so
                         * permissive, so we warn about it.
                         */
                        if (base == 8 && c >= '8') {
                            parser.addWarning("msg.bad.octal.literal",
                                              c == '8' ? "8" : "9");
                            base = 10;
                        }
                        addToString(c);
                        c = getChar();
                    }
                }

                boolean isInteger = true;

                if (base == 10 && (c == '.' || c == 'e' || c == 'E')) {
                    isInteger = false;
                    if (c == '.') {
                        do {
                            addToString(c);
                            c = getChar();
                        } while (isDigit(c));
                    }
                    if (c == 'e' || c == 'E') {
                        addToString(c);
                        c = getChar();
                        if (c == '+' || c == '-') {
                            addToString(c);
                            c = getChar();
                        }
                        if (!isDigit(c)) {
                            parser.addError("msg.missing.exponent");
                            return Token.ERROR;
                        }
                        do {
                            addToString(c);
                            c = getChar();
                        } while (isDigit(c));
                    }
                }
                ungetChar(c);
                String numString = getStringFromBuffer();

                double dval;
                if (base == 10 && !isInteger) {
                    try {
                        // Use Java conversion to number from string...
                        dval = Double.valueOf(numString).doubleValue();
                    }
                    catch (NumberFormatException ex) {
                        parser.addError("msg.caught.nfe");
                        return Token.ERROR;
                    }
                } else {
                    dval = ScriptRuntime.stringToNumber(numString, 0, base);
                }

                this.number = dval;
                return Token.NUMBER;
            }

            // is it a string?
            if (c == '"' || c == '\'') {
                // We attempt to accumulate a string the fast way, by
                // building it directly out of the reader.  But if there
                // are any escaped characters in the string, we revert to
                // building it out of a StringBuffer.

                int quoteChar = c;
                stringBufferTop = 0;

                c = getChar();
                while (c != quoteChar) {
                    if (c == '\n' || c == EOF_CHAR) {
                        ungetChar(c);
                        parser.addError("msg.unterminated.string.lit");
                        return Token.ERROR;
                    }

                    if (c == '\\') {
                        // We've hit an escaped character

                        c = getChar();

                        switch (c) {

                            case '\\': // backslash
                            case 'b':  // backspace
                            case 'f':  // form feed
                            case 'n':  // line feed
                            case 'r':  // carriage return
                            case 't':  // horizontal tab
                            case 'v':  // vertical tab
                            case 'd':  // octal sequence
                            case 'u':  // unicode sequence
                            case 'x':  // hexadecimal sequence
                                // Only keep the '\' character for those
                                // characters that need to be escaped...
                                // Don't escape quoting characters...
                                addToString('\\');
                                addToString(c);
                                break;

                            case '\n':
                                // Remove line terminator after escape
                                break;

                            default:
                                if (isDigit(c)) {
                                    // Octal representation of a character.
                                    // Preserve the escaping (see Y! bug #1637286)
                                    addToString('\\');
                                }
                                addToString(c);
                                break;
                        }

                    } else {

                        addToString(c);
                    }

                    c = getChar();
                }

                String str = getStringFromBuffer();
                this.string = (String)allStrings.intern(str);
                return Token.STRING;
            }

            switch (c) {
            
            /*
            **************************************************            
            TIM - the lookup dict should go here...
            **************************************************
            */
            case ':':
                if (matchChar(':')) {
                    return Token.COLONCOLON;
                } else {
                    return Token.COLON;
                }
            case '.':
                if (matchChar('.')) {
                    return Token.DOTDOT;
                } else if (matchChar('(')) {
                    return Token.DOTQUERY;
                } else {
                    return Token.DOT;
                }

            case '|':
                if (matchChar('|')) {
                    return Token.OR;
                } else if (matchChar('=')) {
                    return Token.ASSIGN_BITOR;
                } else {
                    return Token.BITOR;
                }

            case '^':
                if (matchChar('=')) {
                    return Token.ASSIGN_BITXOR;
                } else {
                    return Token.BITXOR;
                }

            case '&':
                if (matchChar('&')) {
                    return Token.AND;
                } else if (matchChar('=')) {
                    return Token.ASSIGN_BITAND;
                } else {
                    return Token.BITAND;
                }

            case '=':
                if (matchChar('=')) {
                    if (matchChar('='))
                        return Token.SHEQ;
                    else
                        return Token.EQ;
                } else {
                    return Token.ASSIGN;
                }

            case '!':
                if (matchChar('=')) {
                    if (matchChar('='))
                        return Token.SHNE;
                    else
                        return Token.NE;
                } else {
                    return Token.NOT;
                }

            case '<':
                /* NB:treat HTML begin-comment as comment-till-eol */
                if (matchChar('!')) {
                    if (matchChar('-')) {
                        if (matchChar('-')) {
                            skipLine();
                            continue retry;
                        }
                        ungetChar('-');
                    }
                    ungetChar('!');
                }
                if (matchChar('<')) {
                    if (matchChar('=')) {
                        return Token.ASSIGN_LSH;
                    } else {
                        return Token.LSH;
                    }
                } else {
                    if (matchChar('=')) {
                        return Token.LE;
                    } else {
                        return Token.LT;
                    }
                }

            case '>':
                if (matchChar('>')) {
                    if (matchChar('>')) {
                        if (matchChar('=')) {
                            return Token.ASSIGN_URSH;
                        } else {
                            return Token.URSH;
                        }
                    } else {
                        if (matchChar('=')) {
                            return Token.ASSIGN_RSH;
                        } else {
                            return Token.RSH;
                        }
                    }
                } else {
                    if (matchChar('=')) {
                        return Token.GE;
                    } else {
                        return Token.GT;
                    }
                }

            case '*':
                if (matchChar('=')) {
                    return Token.ASSIGN_MUL;
                } else {
                    return Token.MUL;
                }

            case '/':
                // is it a // comment?
                if (matchChar('/')) {
                    skipLine();
                    continue retry;
                }
                if (matchChar('*')) {
                    boolean lookForSlash = false;
                    StringBuffer sb = new StringBuffer();
                    for (;;) {
                        c = getChar();
                        if (c == EOF_CHAR) {
                            parser.addError("msg.unterminated.comment");
                            return Token.ERROR;
                        }
                        sb.append((char) c);
                        if (c == '*') {
                            lookForSlash = true;
                        } else if (c == '/') {
                            if (lookForSlash) {
                                sb.delete(sb.length()-2, sb.length());
                                String s1 = sb.toString();
                                String s2 = s1.trim();
                                if (s1.startsWith("!")) {
                                    // Remove the leading '!'
                                    this.string = s1.substring(1);
                                    return Token.KEEPCOMMENT;
                                } else if (s2.startsWith("@cc_on") ||
                                           s2.startsWith("@if")    ||
                                           s2.startsWith("@elif")  ||
                                           s2.startsWith("@else")  ||
                                           s2.startsWith("@end")) {
                                    this.string = s1;
                                    return Token.CONDCOMMENT;
                                } else {
                                    continue retry;
                                }
                            }
                        } else {
                            lookForSlash = false;
                        }
                    }
                }

                if (matchChar('=')) {
                    return Token.ASSIGN_DIV;
                } else {
                    return Token.DIV;
                }

            case '%':
                if (matchChar('=')) {
                    return Token.ASSIGN_MOD;
                } else {
                    return Token.MOD;
                }

            case '~':
                return Token.BITNOT;

            case '+':
                if (matchChar('=')) {
                    return Token.ASSIGN_ADD;
                } else if (matchChar('+')) {
                    return Token.INC;
                } else {
                    return Token.ADD;
                }

            case '-':
                if (matchChar('=')) {
                    c = Token.ASSIGN_SUB;
                } else if (matchChar('-')) {
                    if (!dirtyLine) {
                        // treat HTML end-comment after possible whitespace
                        // after line start as comment-utill-eol
                        if (matchChar('>')) {
                            skipLine();
                            continue retry;
                        }
                    }
                    c = Token.DEC;
                } else {
                    c = Token.SUB;
                }
                dirtyLine = true;
                return c;

            default:
                parser.addError("msg.illegal.character");
                return Token.ERROR;
            }"""


    def isJSFormatChar(self, c):
        return c > 127 and (Character.getType(c) == Character.FORMAT)
    
    """
    /* As defined in ECMA.  jsscan.c uses C isspace() (which allows
     * \v, I think.)  note that code in getChar() implicitly accepts
     * '\r' == \u000D as well.
     */"""
    def isJSSpace(self, c):
        o = None
        if isinstance(c, int):
            #raise TypeError("should be using string here...:0(")
            o = c
            c = chr(o)
        else:
            o = ord(c)
        if (o <= 127):
            return o == 0x20 or o == 0x9 or o == 0xC or o == 0xB;
        else:
            return o == 0xA0 or \
                Character.getType(c) == Character.SPACE_SEPARATOR;

    def readRegExp(self, startToken):
        self.stringBufferTop = 0
        if (startToken == Token.ASSIGN_DIV):
            self.addToString('=')
        else:
            if (startToken != Token.DIV):
                Kit.codeBug()
        c = 0
        inClass = False
        c = self.getChar()
        while (c != '/') or inClass:
            if (c == '\n') or (c == self.EOF_CHAR):
                self.ungetChar(c)
                raise self.parser.reportError("msg.unterminated.re.lit")
            if (c == '\\'):
                self.addToString(c)
                c = self.getChar()
            else:
                if (c == '['):
                    inClass = True
                else:
                    if (c == ']'):
                        inClass = False
            self.addToString(c)
            c = self.getChar()
        reEnd = self.stringBufferTop
        while True:
            if self.matchChar('g'):
                self.addToString('g')
            else:
                if self.matchChar('i'):
                    self.addToString('i')
                else:
                    if self.matchChar('m'):
                        self.addToString('m')
                    else:
                        break
        if self.peekChar().isalpha():
            raise self.parser.reportError("msg.invalid.re.flag")
        self.string = "".join(self.stringBuffer[0:reEnd])
        self.regExpFlags = "".join(self.stringBuffer[reEnd:self.stringBufferTop])

    def isXMLAttribute(self):
        return self.xmlIsAttribute

    def getFirstXMLToken(self):
        self.xmlOpenTagsCount = 0
        self.xmlIsAttribute = False
        self.xmlIsTagContent = False
        self.ungetChar('<')
        return self.getNextXMLToken()

    def getNextXMLToken(self):
        self.stringBufferTop = 0
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            if self.xmlIsTagContent:
                if c == '>':
                    self.addToString(c)
                    self.xmlIsTagContent = False
                    self.xmlIsAttribute = False
                    break
                elif c == '/':
                    self.addToString(c)
                    if (self.peekChar() == '>'):
                        c = self.getChar()
                        self.addToString(c)
                        self.xmlIsTagContent = False
                        self.xmlOpenTagsCount -= 1
                    break
                elif c == '{':
                    self.ungetChar(c)
                    self.string = self.getStringFromBuffer()
                    return Token.XML
                elif c == '"':
                    self.addToString(c)
                    if not self.readQuotedString(c):
                        return Token.ERROR
                    break
                elif c == '=':
                    self.addToString(c)
                    self.xmlIsAttribute = True
                    break
                elif c in (' ', '\t','\r', '\n'):
                    self.addToString(c)
                    break
                else:
                    self.addToString(c)
                    self.xmlIsAttribute = False
                    break
                if not self.xmlIsTagContent and (self.xmlOpenTagsCount == 0):
                    self.string = self.getStringFromBuffer()
                    return Token.XMLEND
            else:
                if c == '<':
                    self.addToString(c)
                    c = self.peekChar()
                    if c == '!':
                        c = self.getChar()
                        self.addToString(c)
                        c = self.peekChar()
                        if c == '-':
                            c = self.getChar()
                            self.addToString(c)
                            c = self.getChar()
                            if (c == '-'):
                                self.addToString(c)
                                if not self.readXmlComment():
                                    return Token.ERROR
                            else:
                                self.stringBufferTop = 0
                                self.string = None
                                self.parser.addError("msg.XML.bad.form")
                                return Token.ERROR
                            break
                        elif c == '[':
                            c = self.getChar()
                            self.addToString(c)
                            if (getChar() == 'C') and (getChar() == 'D') and (getChar() == 'A') and (getChar() == 'T') and (getChar() == 'A') and (getChar() == '['):
                                self.addToString('C')
                                self.addToString('D')
                                self.addToString('A')
                                self.addToString('T')
                                self.addToString('A')
                                self.addToString('[')
                                if not self.readCDATA():
                                    return Token.ERROR
                            else:
                                self.stringBufferTop = 0
                                self.string = None
                                self.parser.addError("msg.XML.bad.form")
                                return Token.ERROR
                            break
                        else:
                            if not self.readEntity():
                                return Token.ERROR
                            break
                        break
                    elif c == '?':
                        c = self.getChar()
                        self.addToString(c)
                        if not self.readPI():
                            return Token.ERROR
                        break
                    elif c == '/':
                        c = self.getChar()
                        self.addToString(c)
                        if (self.xmlOpenTagsCount == 0):
                            self.stringBufferTop = 0
                            self.string = None
                            self.parser.addError("msg.XML.bad.form")
                            return Token.ERROR
                        self.xmlIsTagContent = True
                        self.xmlOpenTagsCount -= 1
                        break
                    else:
                        self.xmlIsTagContent = True
                        self.xmlOpenTagsCount += 1
                        break
                    break
                elif c == '{':
                    self.ungetChar(c)
                    self.string = self.getStringFromBuffer()
                    return Token.XML
                else:
                    self.addToString(c)
                    break
            c = self.getChar()
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return Token.ERROR

    def readQuotedString(self, quote):
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            self.addToString(c)
            if (c == quote):
                return True
            c = self.getChar()
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return False

    def readXmlComment(self):
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            self.addToString(c)
            if (c == '-') and (self.peekChar() == '-'):
                c = self.getChar()
                self.addToString(c)
                if (self.peekChar() == '>'):
                    c = self.getChar()
                    self.addToString(c)
                    return True
                else:
                    continue
            c = self.getChar()
            True
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return False

    def readCDATA(self):
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            self.addToString(c)
            if (c == ']') and (self.peekChar() == ']'):
                c = self.getChar()
                self.addToString(c)
                if (self.peekChar() == '>'):
                    c = self.getChar()
                    self.addToString(c)
                    return True
                else:
                    continue
            c = self.getChar()
            True
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return False

    def readEntity(self):
        declTags = 1
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            self.addToString(c)
            if c == '<':
                declTags += 1
                break
            elif c == '>':
                declTags -= 1
                if (declTags == 0):
                    return True
                break
            c = self.getChar()
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return False

    def readPI(self):
        ## for-while
        c = self.getChar()
        while (c != self.EOF_CHAR):
            self.addToString(c)
            if (c == '?') and (self.peekChar() == '>'):
                c = self.getChar()
                self.addToString(c)
                return True
            c = self.getChar()
        self.stringBufferTop = 0
        self.string = None
        self.parser.addError("msg.XML.bad.form")
        return False

    def getStringFromBuffer(self):
        #import pdb;pdb.set_trace()
        #return "".join(self.stringBuffer[:self.stringBufferTop-1])
        return "".join(self.stringBuffer[:self.stringBufferTop]).strip()

    def addToString(self, c):
        N = self.stringBufferTop
        """
        if (N == len(self.stringBuffer)):
            tmp = [strval() for __idx0 in range(self.stringBuffer.length * 2)]
            System.arraycopy(self.stringBuffer, 0, tmp, 0, N)
            self.stringBuffer = tmp
        
        self.stringBuffer[N] = c
        self.stringBufferTop = N + 1
        """
        if N == len(self.stringBuffer):
            self.stringBuffer.append(c)
        else:
            self.stringBuffer[N] = c
        self.stringBufferTop += 1

    def ungetChar(self, c):
        if (self.ungetCursor != 0) and (self.ungetBuffer[self.ungetCursor - 1] == '\n'):
            Kit.codeBug()
        self.ungetBuffer[self.ungetCursor] = c  # Think this is right - was [self.ungetCursor += 1]
        self.ungetCursor += 1 # TODO: check this <---- this broke when I set it to something else...
        
    def matchChar(self, test):
        c = self.getChar()
        if (c == test):
            return True
        else:
            self.ungetChar(c)
            return False

    def peekChar(self):
        c = self.getChar()
        self.ungetChar(c)
        return c
        
    def getChar(self):
        c = ""
        if self.ungetCursor != 0 :
            self.ungetCursor -= 1
            return self.ungetBuffer[self.ungetCursor]
        while (True):
            if self.sourceString is not None:
                self.sourceCursor += 1
                if self.sourceCursor >= self.sourceEnd:
                    self.hitEOF = True
                    return EOF_CHAR
                #self.sourceCursor += 1
                c = self.sourceString[self.sourceCursor]
            else:
                if self.sourceCursor == self.sourceEnd:
                    if not self.fillSourceBuffer():
                        self.hitEOF = True
                        return EOF_CHAR
                self.sourceCursor += 1
                c = self.sourceString[self.sourceCursor]
            
            if self.lineEndChar >= 0:
                if (self.lineEndChar == "\r" and c == "\n"):
                    self.lineEndChar = "\n"
                    continue
                self.lineEndChar = -1
                self.lineStart = self.sourceCursor - 1
                self.lineno += 1
                
            # Java version has integers for c the whole time
            o = ord(c)
                
            if (o <= 127):
                if (c in ('\n','\r')):
                    lineEndChar = c;
                    c = '\n';
            else:
                if (self.isJSFormatChar(c)):
                    continue;
                if (ScriptRuntime.isJSLineTerminator(c)):
                    lineEndChar = c;
                    c = '\n';
            return c;

    def skipLine(self):
        c = self.getChar()
        while (c != self.EOF_CHAR) and (c != '\n'):
            c = self.getChar()
        self.ungetChar(c)

    def getOffset(self):
        n = self.sourceCursor - self.lineStart
        if self.lineEndChar >= 0:
            n -= 1
        return n

    def getLine(self):
        if self.sourceString is not None:
            lineEnd = self.sourceCursor
            if self.lineEndChar >= 0:
                lineEnd -= 1
            else:
                ## for-while
                while (lineEnd != self.sourceEnd):
                    c = self.sourceString[lineEnd]
                    if ScriptRuntime.isJSLineTerminator(c):
                        break
                    lineEnd += 1
            return self.sourceString[self.lineStart:lineEnd]
        else:
            lineLength = self.sourceCursor - self.lineStart
            if self.lineEndChar >= 0:
                lineLength -= 1
            else:
                while True:
                    i = self.lineStart + lineLength
                    if (i == self.sourceEnd):
                        try:
                            if not self.fillSourceBuffer():
                                break
                        except (IOException, ), ioe:
                            break
                        i = self.lineStart + lineLength
                    c = self.sourceBuffer[i]
                    if ScriptRuntime.isJSLineTerminator(c):
                        break
                    linelength += 1
            return String(self.sourceBuffer, self.lineStart, lineLength)

    def fillSourceBuffer(self):
        if self.sourceString is not None:
            Kit.codeBug()
        if (self.sourceEnd == self.sourceBuffer.length):
            if (self.lineStart != 0):
                System.arraycopy(self.sourceBuffer, self.lineStart, self.sourceBuffer, 0, self.sourceEnd - self.lineStart)
                self.sourceEnd -= self.lineStart
                self.sourceCursor -= self.lineStart
                self.lineStart = 0
            else:
                tmp = [strval() for __idx0 in range(self.sourceBuffer.length * 2)]
                System.arraycopy(self.sourceBuffer, 0, tmp, 0, self.sourceEnd)
                self.sourceBuffer = tmp
        n = self.sourceReader.read(self.sourceBuffer, self.sourceEnd, self.sourceBuffer.length - self.sourceEnd)
        if n < 0:
            return False
        self.sourceEnd += n
        return True

    dirtyLine = bool()
    regExpFlags = ""
    string = ""
    number = float()
    stringBuffer = []#[str() for __idx0 in range(128)]
    stringBufferTop = 0
    allStrings = ObjToIntMap(50)
    ungetBuffer = [int() for __idx0 in range(3)]
    ungetCursor = 0
    hitEOF = False
    lineStart = 0
    lineno = 0
    lineEndChar = -1
    sourceString = ""
    sourceReader = None#Reader()
    sourceBuffer = []
    sourceEnd = 0
    sourceCursor = 0
    xmlIsAttribute = bool()
    xmlIsTagContent = bool()
    xmlOpenTagsCount = 0
    #parser = Parser()

