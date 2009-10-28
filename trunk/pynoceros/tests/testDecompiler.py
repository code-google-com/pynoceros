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

from unittest import TestCase
from pynoceros.Decompiler import Decompiler
from pynoceros.Token import Token


class TestDecompilerAppendString(TestCase):
    def setUp(self):
        self.d = Decompiler()
        
    def test_appendString(self):
        self.d.appendString("a")
        assert self.d.sourceBuffer == (chr(1) + "a")
        
    def test_appendString2(self):
        self.d.appendString("a"*2)
        assert self.d.sourceBuffer == (chr(2) + "aa")
        
    def test_appendString3(self):
        self.d.appendString("a"*129)
        #assert len(self.d.sourceBuffer) == 131
        assert self.d.sourceBuffer == chr(0x0001 | 0x0080) + chr(0x0001) + "a" * 129
        
    def test_appendString4(self):
        self.d.appendString("abcdefg")
        assert len(self.d.sourceBuffer) == 8
        assert self.d.sourceBuffer == chr(7) + "abcdefg"
        
    
class TestDecompiler(TestCase):
    def setUp(self):
        self.d = Decompiler()
    
    def test_addToken(self):
        self.d.addToken(10)
        assert self.d.sourceBuffer == chr(10)
        
    def test_addEOL(self):
        self.d.addEOL(Token.ADD)
        assert self.d.sourceBuffer == (chr(Token.ADD) + chr(Token.EOL))
    
    def test_addName(self):
        myname = "myname"
        self.d.addName(myname)
        d2 = Decompiler()
        d2.appendString(myname)
        assert self.d.sourceBuffer[0] == chr(Token.NAME)
        assert self.d.sourceBuffer[1:] == d2.sourceBuffer
        
    def test_addString(self):
        self.d.addString("string")
        assert self.d.sourceBuffer[0] == chr(Token.STRING)
        
    def test_addRegexp(self):
        self.d.addRegexp(".+?",flags="re")
        assert self.d.sourceBuffer[0] == chr(Token.REGEXP)    
        
        

