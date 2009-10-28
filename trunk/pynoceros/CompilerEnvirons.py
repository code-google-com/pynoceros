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

from ErrorReporter import ErrorReporter
from Hashtable import Hashtable
from Context import Context

class CompilerEnvirons(object):
    """ generated source for CompilerEnvirons

    """

    def __init__(self):
        """# self.errorReporter = DefaultErrorReporter.instance"""
        self.languageVersion = Context.VERSION_DEFAULT
        self.generateDebugInfo = True
        self.useDynamicScope = False
        self.reservedKeywordAsIdentifier = False
        self.allowMemberExprAsFunctionName = False
        self.xmlAvailable = True
        self.optimizationLevel = 0
        self.generatingSource = True
        self.strictMode = False
        self.warningAsError = False

    def initFromContext(self, cx):
        self.setErrorReporter(cx.getErrorReporter())
        self.languageVersion = cx.getLanguageVersion()
        self.useDynamicScope = cx.compileFunctionsWithDynamicScopeFlag
        self.generateDebugInfo = not cx.isGeneratingDebugChanged() or cx.isGeneratingDebug()
        self.reservedKeywordAsIdentifier = cx.hasFeature(Context.FEATURE_RESERVED_KEYWORD_AS_IDENTIFIER)
        self.allowMemberExprAsFunctionName = cx.hasFeature(Context.FEATURE_MEMBER_EXPR_AS_FUNCTION_NAME)
        self.strictMode = cx.hasFeature(Context.FEATURE_STRICT_MODE)
        self.warningAsError = cx.hasFeature(Context.FEATURE_WARNING_AS_ERROR)
        self.xmlAvailable = cx.hasFeature(Context.FEATURE_E4X)
        self.optimizationLevel = cx.getOptimizationLevel()
        self.generatingSource = cx.isGeneratingSource()
        self.activationNames = cx.activationNames

    def getErrorReporter(self):
        return self.errorReporter

    def setErrorReporter(self, errorReporter):
        if self.errorReporter is None:
            raise IllegalArgumentException()
        self.errorReporter = self.errorReporter

    def getLanguageVersion(self):
        return self.languageVersion

    def setLanguageVersion(self, languageVersion):
        Context.checkLanguageVersion(self.languageVersion)
        self.languageVersion = self.languageVersion

    def isGenerateDebugInfo(self):
        return self.generateDebugInfo

    def setGenerateDebugInfo(self, flag):
        self.generateDebugInfo = flag

    def isUseDynamicScope(self):
        return self.useDynamicScope

    def isReservedKeywordAsIdentifier(self):
        return self.reservedKeywordAsIdentifier

    def setReservedKeywordAsIdentifier(self, flag):
        self.reservedKeywordAsIdentifier = flag

    def isAllowMemberExprAsFunctionName(self):
        return self.allowMemberExprAsFunctionName

    def setAllowMemberExprAsFunctionName(self, flag):
        self.allowMemberExprAsFunctionName = flag

    def isXmlAvailable(self):
        return self.xmlAvailable

    def setXmlAvailable(self, flag):
        self.xmlAvailable = flag

    def getOptimizationLevel(self):
        return self.optimizationLevel

    def setOptimizationLevel(self, level):
        Context.checkOptimizationLevel(level)
        self.optimizationLevel = level

    def isGeneratingSource(self):
        return self.generatingSource

    def isStrictMode(self):
        return self.strictMode

    def reportWarningAsError(self):
        return self.warningAsError

    def setGeneratingSource(self, generatingSource):
        self.generatingSource = self.generatingSource

    errorReporter = ErrorReporter()
    languageVersion = 0
    generateDebugInfo = bool()
    useDynamicScope = bool()
    reservedKeywordAsIdentifier = bool()
    allowMemberExprAsFunctionName = bool()
    xmlAvailable = bool()
    optimizationLevel = 0
    generatingSource = bool()
    strictMode = bool()
    warningAsError = bool()
    activationNames = Hashtable()

