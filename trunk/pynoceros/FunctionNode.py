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
from ScriptOrFnNode import ScriptOrFnNode

class FunctionNode(ScriptOrFnNode):
    """ generated source for FunctionNode

    """

    def __init__(self, name):
        ScriptOrFnNode.__init__(self, Token.FUNCTION)
        self.functionName = name

    def getFunctionName(self):
        return self.functionName

    def requiresActivation(self):
        return self.itsNeedsActivation

    def getIgnoreDynamicScope(self):
        return self.itsIgnoreDynamicScope

    FUNCTION_STATEMENT = 1
    FUNCTION_EXPRESSION = 2
    FUNCTION_EXPRESSION_STATEMENT = 3

    def getFunctionType(self):
        return self.itsFunctionType

    functionName = ""
    itsNeedsActivation = bool()
    itsFunctionType = 0
    itsIgnoreDynamicScope = bool()

