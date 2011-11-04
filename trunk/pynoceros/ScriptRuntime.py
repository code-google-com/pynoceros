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

"""
Hand coded custom bits
"""

class ScriptRuntime(object):
    @classmethod
    def getMessage0(self, message_id):
        # This should look up a full, translated message etc.
        # Don't bother for now.
        return str(message_id)
    
    @classmethod
    def getMessage1(self, message_id, arg1):
        #TODO:...
        return self.getMessage0(message_id)

    @classmethod
    def isJSLineTerminator(self, c):
        if c == '\n' or c == '\r' or ord(c) == 0x2028 or ord(c) == 0x2029:
            return True
        return False

    @classmethod
    def getIndexObject(self, s):
        if isinstance(s, int):
            i = int(s)
            if i > 0:
                return i
        return s

    @classmethod
    def isSpecialProperty(self, s):
        return ( (s == "__proto__") or (s == "__parent__") )

    emptyArgs = []
        
