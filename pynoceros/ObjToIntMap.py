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

# It seems it's always immutable objects used
# - so just rely on dict implementation
class ObjToIntMap (dict):
    def __init__(self, size):
        pass
    
    def isEmpty(self):
        return len(self)== 0
        
    def size(self):
        return len(self)
    
    def has(self, key):
        return key in self.keys()
        
    def getExisting(self, keyobject):
        raise NotImplementedError()
        
    def put(self, key, val):
        self[key] = val
"""
class ObjToIntMap (object):
    def __init__(self, size):
        # throw away size - rely on dict...
        self.__mydict = {}
        
    def isEmpty(self):
        return (len(self.__mydict) == 0)
        
    def size(self):
        return len(self.__mydict)
        
    def has(self, keyobject):
        return ( self._objecthash(keyobject) in self.__mydict.keys() )
        
    def _objecthash(self, keyobject):
        # separated in case the object is mutable
        return id(keyobject)
        #return hash(keyobject)
        
    def get(self, keyobject, default):
        #TODO:
        return self.__mydict.get(self._objecthash(keyobject) , default)
        raise NotImplementedError()
        
    def getExisting(self, keyobject):
        #TODO:
        raise NotImplementedError()
        
    def put(self, keyobject, value):
        #TODO:
        self.__mydict[self._objecthash(keyobject)] = value
        #raise NotImplementedError()
        
    
    #/**
    # * If table already contains a key that equals to keyArg, return that key
    # * while setting its value to zero, otherwise add keyArg with 0 value to
    # * the table and return it.
    # */
    def intern(self, keyobject):
        #TODO:
        raise NotImplementedError()

    def remove(self, keyobject):
        #TODO:
        raise NotImplementedError()
        
    def clear(self):
        #TODO:
        raise NotImplementedError()
    """
