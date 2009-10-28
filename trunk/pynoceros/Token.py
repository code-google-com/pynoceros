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


class Token(object):
    """ generated source for Token

    """
    printTrees = False
    printICode = False
    printNames = printTrees or printICode
    ERROR = -1
    EOF = 0
    EOL = 1
    FIRST_BYTECODE_TOKEN = 2
    ENTERWITH = 2
    LEAVEWITH = 3
    RETURN = 4
    GOTO = 5
    IFEQ = 6
    IFNE = 7
    SETNAME = 8
    BITOR = 9
    BITXOR = 10
    BITAND = 11
    EQ = 12
    NE = 13
    LT = 14
    LE = 15
    GT = 16
    GE = 17
    LSH = 18
    RSH = 19
    URSH = 20
    ADD = 21
    SUB = 22
    MUL = 23
    DIV = 24
    MOD = 25
    NOT = 26
    BITNOT = 27
    POS = 28
    NEG = 29
    NEW = 30
    DELPROP = 31
    TYPEOF = 32
    GETPROP = 33
    SETPROP = 34
    GETELEM = 35
    SETELEM = 36
    CALL = 37
    NAME = 38
    NUMBER = 39
    STRING = 40
    NULL = 41
    THIS = 42
    FALSE = 43
    TRUE = 44
    SHEQ = 45
    SHNE = 46
    REGEXP = 47
    BINDNAME = 48
    THROW = 49
    RETHROW = 50
    IN = 51
    INSTANCEOF = 52
    LOCAL_LOAD = 53
    GETVAR = 54
    SETVAR = 55
    CATCH_SCOPE = 56
    ENUM_INIT_KEYS = 57
    ENUM_INIT_VALUES = 58
    ENUM_NEXT = 59
    ENUM_ID = 60
    THISFN = 61
    RETURN_RESULT = 62
    ARRAYLIT = 63
    OBJECTLIT = 64
    GET_REF = 65
    SET_REF = 66
    DEL_REF = 67
    REF_CALL = 68
    REF_SPECIAL = 69
    DEFAULTNAMESPACE = 70
    ESCXMLATTR = 71
    ESCXMLTEXT = 72
    REF_MEMBER = 73
    REF_NS_MEMBER = 74
    REF_NAME = 75
    REF_NS_NAME = 76
    LAST_BYTECODE_TOKEN = REF_NS_NAME
    TRY = 77
    SEMI = 78
    LB = 79
    RB = 80
    LC = 81
    RC = 82
    LP = 83
    RP = 84
    COMMA = 85
    ASSIGN = 86
    ASSIGN_BITOR = 87
    ASSIGN_BITXOR = 88
    ASSIGN_BITAND = 89
    ASSIGN_LSH = 90
    ASSIGN_RSH = 91
    ASSIGN_URSH = 92
    ASSIGN_ADD = 93
    ASSIGN_SUB = 94
    ASSIGN_MUL = 95
    ASSIGN_DIV = 96
    ASSIGN_MOD = 97
    FIRST_ASSIGN = ASSIGN
    LAST_ASSIGN = ASSIGN_MOD
    HOOK = 98
    COLON = 99
    OR = 100
    AND = 101
    INC = 102
    DEC = 103
    DOT = 104
    FUNCTION = 105
    EXPORT = 106
    IMPORT = 107
    IF = 108
    ELSE = 109
    SWITCH = 110
    CASE = 111
    DEFAULT = 112
    WHILE = 113
    DO = 114
    FOR = 115
    BREAK = 116
    CONTINUE = 117
    VAR = 118
    WITH = 119
    CATCH = 120
    FINALLY = 121
    VOID = 122
    RESERVED = 123
    EMPTY = 124
    BLOCK = 125
    LABEL = 126
    TARGET = 127
    LOOP = 128
    EXPR_VOID = 129
    EXPR_RESULT = 130
    JSR = 131
    SCRIPT = 132
    TYPEOFNAME = 133
    USE_STACK = 134
    SETPROP_OP = 135
    SETELEM_OP = 136
    LOCAL_BLOCK = 137
    SET_REF_OP = 138
    DOTDOT = 139
    COLONCOLON = 140
    XML = 141
    DOTQUERY = 142
    XMLATTR = 143
    XMLEND = 144
    TO_OBJECT = 145
    TO_DOUBLE = 146
    GET = 147
    SET = 148
    CONST = 149
    SETCONST = 150
    SETCONSTVAR = 151
    CONDCOMMENT = 152
    KEEPCOMMENT = 153
    LAST_TOKEN = 154

    @classmethod
    def name(cls, token):
        if not cls.printNames:
            return str(token)
        if token == cls.ERROR:
            return "ERROR"
        elif token == cls.EOF:
            return "EOF"
        elif token == cls.EOL:
            return "EOL"
        elif token == cls.ENTERWITH:
            return "ENTERWITH"
        elif token == cls.LEAVEWITH:
            return "LEAVEWITH"
        elif token == cls.RETURN:
            return "RETURN"
        elif token == cls.GOTO:
            return "GOTO"
        elif token == cls.IFEQ:
            return "IFEQ"
        elif token == cls.IFNE:
            return "IFNE"
        elif token == cls.SETNAME:
            return "SETNAME"
        elif token == cls.BITOR:
            return "BITOR"
        elif token == cls.BITXOR:
            return "BITXOR"
        elif token == cls.BITAND:
            return "BITAND"
        elif token == cls.EQ:
            return "EQ"
        elif token == cls.NE:
            return "NE"
        elif token == cls.LT:
            return "LT"
        elif token == cls.LE:
            return "LE"
        elif token == cls.GT:
            return "GT"
        elif token == cls.GE:
            return "GE"
        elif token == cls.LSH:
            return "LSH"
        elif token == cls.RSH:
            return "RSH"
        elif token == cls.URSH:
            return "URSH"
        elif token == cls.ADD:
            return "ADD"
        elif token == cls.SUB:
            return "SUB"
        elif token == cls.MUL:
            return "MUL"
        elif token == cls.DIV:
            return "DIV"
        elif token == cls.MOD:
            return "MOD"
        elif token == cls.NOT:
            return "NOT"
        elif token == cls.BITNOT:
            return "BITNOT"
        elif token == cls.POS:
            return "POS"
        elif token == cls.NEG:
            return "NEG"
        elif token == cls.NEW:
            return "NEW"
        elif token == cls.DELPROP:
            return "DELPROP"
        elif token == cls.TYPEOF:
            return "TYPEOF"
        elif token == cls.GETPROP:
            return "GETPROP"
        elif token == cls.SETPROP:
            return "SETPROP"
        elif token == cls.GETELEM:
            return "GETELEM"
        elif token == cls.SETELEM:
            return "SETELEM"
        elif token == cls.CALL:
            return "CALL"
        elif token == cls.NAME:
            return "NAME"
        elif token == cls.NUMBER:
            return "NUMBER"
        elif token == cls.STRING:
            return "STRING"
        elif token == cls.NULL:
            return "NULL"
        elif token == cls.THIS:
            return "THIS"
        elif token == cls.FALSE:
            return "FALSE"
        elif token == cls.TRUE:
            return "TRUE"
        elif token == cls.SHEQ:
            return "SHEQ"
        elif token == cls.SHNE:
            return "SHNE"
        elif token == cls.REGEXP:
            return "OBJECT"
        elif token == cls.BINDNAME:
            return "BINDNAME"
        elif token == cls.THROW:
            return "THROW"
        elif token == cls.RETHROW:
            return "RETHROW"
        elif token == cls.IN:
            return "IN"
        elif token == cls.INSTANCEOF:
            return "INSTANCEOF"
        elif token == cls.LOCAL_LOAD:
            return "LOCAL_LOAD"
        elif token == cls.GETVAR:
            return "GETVAR"
        elif token == cls.SETVAR:
            return "SETVAR"
        elif token == cls.CATCH_SCOPE:
            return "CATCH_SCOPE"
        elif token == cls.ENUM_INIT_KEYS:
            return "ENUM_INIT_KEYS"
        elif token == cls.ENUM_INIT_VALUES:
            return "ENUM_INIT_VALUES"
        elif token == cls.ENUM_NEXT:
            return "ENUM_NEXT"
        elif token == cls.ENUM_ID:
            return "ENUM_ID"
        elif token == cls.THISFN:
            return "THISFN"
        elif token == cls.RETURN_RESULT:
            return "RETURN_RESULT"
        elif token == cls.ARRAYLIT:
            return "ARRAYLIT"
        elif token == cls.OBJECTLIT:
            return "OBJECTLIT"
        elif token == cls.GET_REF:
            return "GET_REF"
        elif token == cls.SET_REF:
            return "SET_REF"
        elif token == cls.DEL_REF:
            return "DEL_REF"
        elif token == cls.REF_CALL:
            return "REF_CALL"
        elif token == cls.REF_SPECIAL:
            return "REF_SPECIAL"
        elif token == cls.DEFAULTNAMESPACE:
            return "DEFAULTNAMESPACE"
        elif token == cls.ESCXMLTEXT:
            return "ESCXMLTEXT"
        elif token == cls.ESCXMLATTR:
            return "ESCXMLATTR"
        elif token == cls.REF_MEMBER:
            return "REF_MEMBER"
        elif token == cls.REF_NS_MEMBER:
            return "REF_NS_MEMBER"
        elif token == cls.REF_NAME:
            return "REF_NAME"
        elif token == cls.REF_NS_NAME:
            return "REF_NS_NAME"
        elif token == cls.TRY:
            return "TRY"
        elif token == cls.SEMI:
            return "SEMI"
        elif token == cls.LB:
            return "LB"
        elif token == cls.RB:
            return "RB"
        elif token == cls.LC:
            return "LC"
        elif token == cls.RC:
            return "RC"
        elif token == cls.LP:
            return "LP"
        elif token == cls.RP:
            return "RP"
        elif token == cls.COMMA:
            return "COMMA"
        elif token == cls.ASSIGN:
            return "ASSIGN"
        elif token == cls.ASSIGN_BITOR:
            return "ASSIGN_BITOR"
        elif token == cls.ASSIGN_BITXOR:
            return "ASSIGN_BITXOR"
        elif token == cls.ASSIGN_BITAND:
            return "ASSIGN_BITAND"
        elif token == cls.ASSIGN_LSH:
            return "ASSIGN_LSH"
        elif token == cls.ASSIGN_RSH:
            return "ASSIGN_RSH"
        elif token == cls.ASSIGN_URSH:
            return "ASSIGN_URSH"
        elif token == cls.ASSIGN_ADD:
            return "ASSIGN_ADD"
        elif token == cls.ASSIGN_SUB:
            return "ASSIGN_SUB"
        elif token == cls.ASSIGN_MUL:
            return "ASSIGN_MUL"
        elif token == cls.ASSIGN_DIV:
            return "ASSIGN_DIV"
        elif token == cls.ASSIGN_MOD:
            return "ASSIGN_MOD"
        elif token == cls.HOOK:
            return "HOOK"
        elif token == cls.COLON:
            return "COLON"
        elif token == cls.OR:
            return "OR"
        elif token == cls.AND:
            return "AND"
        elif token == cls.INC:
            return "INC"
        elif token == cls.DEC:
            return "DEC"
        elif token == cls.DOT:
            return "DOT"
        elif token == cls.FUNCTION:
            return "FUNCTION"
        elif token == cls.EXPORT:
            return "EXPORT"
        elif token == cls.IMPORT:
            return "IMPORT"
        elif token == cls.IF:
            return "IF"
        elif token == cls.ELSE:
            return "ELSE"
        elif token == cls.SWITCH:
            return "SWITCH"
        elif token == cls.CASE:
            return "CASE"
        elif token == cls.DEFAULT:
            return "DEFAULT"
        elif token == cls.WHILE:
            return "WHILE"
        elif token == cls.DO:
            return "DO"
        elif token == cls.FOR:
            return "FOR"
        elif token == cls.BREAK:
            return "BREAK"
        elif token == cls.CONTINUE:
            return "CONTINUE"
        elif token == cls.VAR:
            return "VAR"
        elif token == cls.WITH:
            return "WITH"
        elif token == cls.CATCH:
            return "CATCH"
        elif token == cls.FINALLY:
            return "FINALLY"
        elif token == cls.RESERVED:
            return "RESERVED"
        elif token == cls.EMPTY:
            return "EMPTY"
        elif token == cls.BLOCK:
            return "BLOCK"
        elif token == cls.LABEL:
            return "LABEL"
        elif token == cls.TARGET:
            return "TARGET"
        elif token == cls.LOOP:
            return "LOOP"
        elif token == cls.EXPR_VOID:
            return "EXPR_VOID"
        elif token == cls.EXPR_RESULT:
            return "EXPR_RESULT"
        elif token == cls.JSR:
            return "JSR"
        elif token == cls.SCRIPT:
            return "SCRIPT"
        elif token == cls.TYPEOFNAME:
            return "TYPEOFNAME"
        elif token == cls.USE_STACK:
            return "USE_STACK"
        elif token == cls.SETPROP_OP:
            return "SETPROP_OP"
        elif token == cls.SETELEM_OP:
            return "SETELEM_OP"
        elif token == cls.LOCAL_BLOCK:
            return "LOCAL_BLOCK"
        elif token == cls.SET_REF_OP:
            return "SET_REF_OP"
        elif token == cls.DOTDOT:
            return "DOTDOT"
        elif token == cls.COLONCOLON:
            return "COLONCOLON"
        elif token == cls.XML:
            return "XML"
        elif token == cls.DOTQUERY:
            return "DOTQUERY"
        elif token == cls.XMLATTR:
            return "XMLATTR"
        elif token == cls.XMLEND:
            return "XMLEND"
        elif token == cls.TO_OBJECT:
            return "TO_OBJECT"
        elif token == cls.TO_DOUBLE:
            return "TO_DOUBLE"
        elif token == cls.GET:
            return "GET"
        elif token == cls.SET:
            return "SET"
        elif token == cls.CONST:
            return "CONST"
        elif token == cls.SETCONST:
            return "SETCONST"
        raise IllegalStateException(str(token))


