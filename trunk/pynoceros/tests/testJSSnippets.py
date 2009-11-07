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
from pynoceros.Parser import Parser
from pynoceros.Token import Token

from pynoceros.CompilerEnvirons import CompilerEnvirons
from pynoceros.ErrorReporter import ErrorReporter

class TestJSSnippets(TestCase):
    def setUp(self):
        ce = CompilerEnvirons()
        er = ErrorReporter()
        self.parser = Parser(ce, er)
        
    def _parsesOk(self, instr):
        try:
            self.parser.parse(instr+"\n", None, 1)
        except Exception, e:
            print e
            return False
        return True
        
    def test_function_def(self):
        assert self._parsesOk("function a () {};")
        
    def test_anon_function_def(self):
        assert self._parsesOk("a = function () {};")
        
    def test_call_function(self):
        assert self._parsesOk("alert(1);")
        
    def test_call_function_with_string(self):
        assert self._parsesOk("alert(\"hello\");")
        
    def test_object_repr(self):
        assert self._parsesOk("var a = {a:1,b:2}")
        
    def test_array_repr(self):
        assert self._parsesOk("var b = [0,1,2,3,4,5]")
        
    def test_while(self):
        assert self._parsesOk("while (true) {};")

    def test_or_defn(self):
        assert self._parsesOk("var myvar = myvar || {};")
        
    def test_for(self):
        assert self._parsesOk("for (i=0;i<=5;i++){i = 6;}")

    def test_for_var(self):
        # different execution path
        assert self._parsesOk("for (var i = 0; i < 5; i++){i=6;}")
        
    def test_for_requires_semi(self):
        assert not self._parsesOk("for (var i = 0; i < 5 i++){i=6;}")
               
    def test_for_in(self):
        assert self._parsesOk("var a = {}; for (i in a){var b = a[i] };")

    def test_do(self):
        assert self._parsesOk("i = 0; do{ i++; } while (i < 5)")
        
    def test_for_break(self):
        assert self._parsesOk("for (i=0;i<=5;i++){break;}")
        
    def test_for_continue(self):
        assert self._parsesOk("for (i=0;i<=5;i++){continue;}")
        
    def test_switch(self):
        assert self._parsesOk("""
            n = 5;
            switch(n)
            {
            case 1:
                a = 1;
            default:
                a = 1;
            }""")
        
    def test_var(self):
        assert self._parsesOk("var a = 1;")
        
    def test_comment(self):
        assert self._parsesOk("// comment")
        
    def test_blockcomment(self):
        assert self._parsesOk("/* block comment */")
        
    def test_try(self):
        assert self._parsesOk("try{a = 1} catch(e){}")
        
    def test_finally(self):
        assert self._parsesOk("try {} catch( myError ) {} finally {}")
        
    def test_label(self):
        """I had no idea you could have labels in javascript until I read this
           source ... TimW"""
        assert self._parsesOk("""myLabel: {var a;}""")
        
    def test_break_label(self):
        assert self._parsesOk("""outloop:while(true){break outloop;}""")
       
    def test_throw_string(self):
        assert self._parsesOk("""throw "Testing Throw";""")

    def test_assign_add(self):
        assert self._parsesOk("var i = 0; i += 1;")
    
    def test_plus_pluss(self):
        assert self._parsesOk("var i = 0; i ++;")

    def test_assign_sub(self):
        assert self._parsesOk("var i = 10; i -= 1;")

    def test_new(self):
        assert self._parsesOk("function Klass(){}; var i = new Klass();")

    def test_function_with_params(self):
        assert self._parsesOk("function testme(a,b){return b+a;}")

    def test_if(self):
        assert self._parsesOk("if (true) {var i = 0;}")

    def test_if_else(self):
        assert self._parsesOk("if (false) {var i = 0;} else{ var i = 1;}")

    def test_with(self):
        assert self._parsesOk("var a = {}; with(a){a[1]=1;}")
        
    def test_hex(self):
        assert self._parsesOk("var a = 0xa0f;")
        
    def test_long_hex(self):
        assert self._parsesOk("var a = 0x0fffffff;")
        
    def throw_object(self):
        assert self._parsesOk("var y = []; y.length = {valueOf:function() { throw new Error(); }};")
        
    def test_float(self):
        assert self._parsesOk("var a = 0.332;")
        
    def test_escaped_string(self):
        assert self._parsesOk('var a = "\\ntest";')
        
    def test_med_int(self):
        assert self._parsesOk("var a = 300;")
        
    def test_med_int(self):
        assert self._parsesOk("var a = 100000;")
        
    def test_neg_int(self):
        assert self._parsesOk("var a = -300;")
        
    def test_null(self):
        assert self._parsesOk("var a = null;")
        
    def test_rhs_expression_assignment(self):
        assert self._parsesOk("""(function() {\
           var x, y;\
           x = y = 8;\
           return x;\
         })()""")
         
    def test_regex_test(self):
        assert self._parsesOk("/[6-9]/.test('2');")
        
    def test_while_assumed_scope(self):
        assert self._parsesOk("result = 42; while(true)break")
        
    def test_unicode(self):
        assert self._parsesOk("abc\u0067efg")
        
        
    def test_triple_eq(self):
        assert self._parsesOk("1 === 1;")
        
    def test_query_cond(self):
        assert self._parsesOk("x = x ? x : 0;")
       
    def test_typeof(self):
        # This caused the initial import to fail parsing jQuery
        assert self._parsesOk('if(typeof a === "string"){}')

    def test_labels(self):
        # Another bug that was raised during parsing jQeury
        assert self._parsesOk('example: function(){}')
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestJSSnippets))
    return suite
