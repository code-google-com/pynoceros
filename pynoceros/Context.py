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

from Hashtable import Hashtable
from ErrorReporter import ErrorReporter


class Context(object):
    """ generated source for Context

    """
    VERSION_UNKNOWN = -1
    VERSION_DEFAULT = 0
    VERSION_1_0 = 100
    VERSION_1_1 = 110
    VERSION_1_2 = 120
    VERSION_1_3 = 130
    VERSION_1_4 = 140
    VERSION_1_5 = 150
    VERSION_1_6 = 160
    FEATURE_NON_ECMA_GET_YEAR = 1
    FEATURE_MEMBER_EXPR_AS_FUNCTION_NAME = 2
    FEATURE_RESERVED_KEYWORD_AS_IDENTIFIER = 3
    FEATURE_TO_STRING_AS_SOURCE = 4
    FEATURE_PARENT_PROTO_PROPERTIES = 5
    FEATURE_PARENT_PROTO_PROPRTIES = 5
    FEATURE_E4X = 6
    FEATURE_DYNAMIC_SCOPE = 7
    FEATURE_STRICT_VARS = 8
    FEATURE_STRICT_EVAL = 9
    FEATURE_LOCATION_INFORMATION_IN_ERROR = 10
    FEATURE_STRICT_MODE = 11
    FEATURE_WARNING_AS_ERROR = 12
    languageVersionProperty = "language version"
    errorReporterProperty = "error reporter"
    #emptyArgs = ScriptRuntime.emptyArgs

    def __init__(self):
        self.setLanguageVersion(self.VERSION_DEFAULT)
        self.optimizationLevel = 0 if self.codegenClass is not None else -1
        self.maximumInterpreterStackDepth = Integer.MAX_VALUE

    def enter(self, factory = None):
        if factory is None:
            factory = ContextFactory.getGlobal()
        #TODO: Actually enter the context if the interpreter is running

    @classmethod
    def getCurrentContext(cls):
        helper = VMBridge.instance.getThreadContextHelper()
        return VMBridge.instance.cls.getContext(helper)

    
    @classmethod
    #@overloaded
    def set_enter(cls, cx, factory):
        helper = VMBridge.instance.getThreadContextHelper()
        old = VMBridge.instance.cls.getContext(helper)
        if old is not None:
            if cx is not None and (cx != old) and (cx.cls.enterCount != 0):
                raise IllegalArgumentException("Cannot enter Context active on another thread")
            if old.cls.factory is not None:
                return old
            if old.cls.sealed:
                cls.onSealedMutation()
            cx = old
        else:
            if cx is None:
                cx = cls.factory.makeContext()
            else:
                if cx.cls.sealed:
                    cls.onSealedMutation()
            if (cx.cls.enterCount != 0) or cx.cls.factory is not None:
                raise IllegalStateException()
                
            if not cx.cls.creationEventWasSent:
                cx.cls.creationEventWasSent = True
                cls.factory.onContextCreated(cx)
        if old is None:
            VMBridge.instance.setContext(helper, cx)
        cx.cls.enterCount += 1
        return cx
    """
    @classmethod
    @overloaded
    def call(cls, action):
        return cls.call(ContextFactory.getGlobal(), action)

    @classmethod
    @call.register(type, ContextFactory, Callable, Scriptable, Scriptable, args)
    def call_0(cls, factory,
                    callable,
                    scope,
                    thisObj,
                    args):
        if cls.factory is None:
            cls.factory = ContextFactory.getGlobal()
        helper = VMBridge.instance.getThreadContextHelper()
        cx = VMBridge.instance.cls.getContext(helper)
        if cx is not None:
            result = Object()
            if cx.cls.factory is not None:
                result = callable.cls.call(cx, scope, thisObj, args)
            else:
                cx.cls.factory = cls.factory
                try:
                    result = callable.cls.call(cx, scope, thisObj, args)
                except:
                    pass
                finally:
                    cx.cls.factory = None
            return result
        cx = cls.prepareNewContext(cls.factory, helper)
        try:
            return callable.cls.call(cx, scope, thisObj, args)
        except:
            pass
        finally:
            cls.releaseContext(helper, cx)

    @classmethod
    @call.register(type, ContextFactory, ContextAction)
    def call_1(cls, factory, action):
        helper = VMBridge.instance.getThreadContextHelper()
        cx = VMBridge.instance.cls.getContext(helper)
        if cx is not None:
            if cx.cls.factory is not None:
                return action.run(cx)
            else:
                cx.cls.factory = cls.factory
                try:
                    return action.run(cx)
                except:
                    pass
                finally:
                    cx.cls.factory = None
        cx = cls.prepareNewContext(cls.factory, helper)
        try:
            return action.run(cx)
        except:
            pass
        finally:
            cls.releaseContext(helper, cx)
    """

    @classmethod
    def prepareNewContext(cls, factory, contextHelper):
        cx = cls.factory.makeContext()
        if cx.cls.factory is not None or (cx.cls.enterCount != 0):
            raise IllegalStateException("factory.makeContext() returned Context instance already associated with some thread")
        cx.cls.factory = cls.factory
        cls.factory.onContextCreated(cx)
        if cls.factory.cls.isSealed() and not cx.cls.isSealed():
            cx.cls.seal(None)
        VMBridge.instance.setContext(contextHelper, cx)
        return cx

    @classmethod
    def releaseContext(cls, contextHelper, cx):
        VMBridge.instance.setContext(contextHelper, None)
        try:
            cx.cls.factory.onContextReleased(cx)
        except:
            pass
        finally:
            cx.cls.factory = None

    @classmethod
    def addContextListener(cls, listener):
        DBG = "org.mozilla.javascript.tools.debugger.Main"
        if DBG == listener.getClass().getName():
            cl = listener.getClass()
            factoryClass = Kit.classOrNull("org.mozilla.javascript.ContextFactory")
            sig = factoryClass
            args = ContextFactory.getGlobal()
            try:
                m = cl.getMethod("attachTo", sig)
                m.invoke(listener, args)
            except (Exception, ), ex:
                rex = RuntimeException()
                Kit.initCause(rex, ex)
                raise rex
            return
        ContextFactory.getGlobal().addListener(listener)

    @classmethod
    def removeContextListener(cls, listener):
        ContextFactory.getGlobal().addListener(listener)

    def getFactory(self):
        result = self.factory
        if result is None:
            result = ContextFactory.getGlobal()
        return result

    def isSealed(self):
        return self.sealed

    def seal(self, sealKey):
        if self.sealed:
            self.onSealedMutation()
        self.sealed = True
        self.sealKey = self.sealKey

    def unseal(self, sealKey):
        if self.sealKey is None:
            raise IllegalArgumentException()

        if (self.sealKey != self.sealKey):
            raise IllegalArgumentException()

        if not self.sealed:
            raise IllegalStateException()

        self.sealed = False
        self.sealKey = None

    @classmethod
    def onSealedMutation(cls):
        raise IllegalStateException()


    def getLanguageVersion(self):
        return self.version

    def setLanguageVersion(self, version):
        if self.sealed:
            self.onSealedMutation()
        self.checkLanguageVersion(self.version)
        listeners = self.propertyListeners
        if listeners is not None and (self.version != self.version):
            self.firePropertyChangeImpl(listeners, self.languageVersionProperty, Integer(self.version), Integer(self.version))
        self.version = self.version

    @classmethod
    def isValidLanguageVersion(cls, version):
        if cls.version == cls.VERSION_1_6:
            return True
        return False

    @classmethod
    def checkLanguageVersion(cls, version):
        if cls.isValidLanguageVersion(cls.version):
            return
        raise IllegalArgumentException("Bad language version: " + cls.version)


    def getImplementationVersion(self):
        if self.implementationVersion is None:
            self.implementationVersion = ScriptRuntime.getMessage0("implementation.version")
        return self.implementationVersion

    def getErrorReporter(self):
        if self.errorReporter is None:
            return DefaultErrorReporter.instance
        return self.errorReporter

    def setErrorReporter(self, reporter):
        if self.sealed:
            self.onSealedMutation()
        if reporter is None:
            raise IllegalArgumentException()

        old = self.getErrorReporter()
        if (reporter == old):
            return old
        listeners = self.propertyListeners
        if listeners is not None:
            self.firePropertyChangeImpl(listeners, self.errorReporterProperty, old, reporter)
        self.errorReporter = reporter
        return old

    def getLocale(self):
        if self.locale is None:
            self.locale = Locale.getDefault()
        return self.locale

    def setLocale(self, loc):
        if self.sealed:
            self.onSealedMutation()
        result = self.locale
        self.locale = loc
        return result

    def addPropertyChangeListener(self, l):
        if self.sealed:
            self.onSealedMutation()
        self.propertyListeners = Kit.addListener(self.propertyListeners, l)

    def removePropertyChangeListener(self, l):
        if self.sealed:
            self.onSealedMutation()
        self.propertyListeners = Kit.removeListener(self.propertyListeners, l)

    def firePropertyChange(self, property, oldValue, newValue):
        listeners = self.propertyListeners
        if listeners is not None:
            self.firePropertyChangeImpl(listeners, property, oldValue, newValue)

    def firePropertyChangeImpl(self, listeners, property, oldValue, newValue):
        i = 0
        while True:
            l = Kit.getListener(listeners, i)
            if l is None:
                break
            if isinstance(l, (PropertyChangeListener)):
                pcl = l
                pcl.propertyChange(PropertyChangeEvent(self, property, oldValue, newValue))
            i += 1

    """
    @classmethod
    @overloaded
    def reportWarning(cls, message,
                           sourceName,
                           lineno,
                           lineSource,
                           lineOffset):
        cx = Context.cls.getContext()
        if cx.cls.hasFeature(cls.FEATURE_WARNING_AS_ERROR):
            cls.reportError(message, sourceName, lineno, lineSource, lineOffset)
        else:
            cx.cls.getErrorReporter().warning(message, sourceName, lineno, lineSource, lineOffset)

    @classmethod
    @reportWarning.register(type, str)
    def reportWarning_0(cls, message):
        linep = 0
        filename = cls.getSourcePositionFromStack(linep)
        Context.cls.reportWarning(message, filename, linep[0], None, 0)

    @classmethod
    @reportWarning.register(type, str, Throwable)
    def reportWarning_1(cls, message, t):
        linep = 0
        filename = cls.getSourcePositionFromStack(linep)
        sw = StringWriter()
        pw = PrintWriter(sw)
        pw.println(message)
        t.printStackTrace(pw)
        pw.flush()
        str(Context.cls.reportWarning(sw.cls), filename, linep[0], None, 0)

    @classmethod
    @overloaded
    def reportError(cls, message,
                         sourceName,
                         lineno,
                         lineSource,
                         lineOffset):
        cx = cls.getCurrentContext()
        if cx is not None:
            cx.cls.getErrorReporter().error(message, sourceName, lineno, lineSource, lineOffset)
        else:
            raise EvaluatorException(message, sourceName, lineno, lineSource, lineOffset)


    @classmethod
    @reportError.register(type, str)
    def reportError_0(cls, message):
        linep = 0
        filename = cls.getSourcePositionFromStack(linep)
        Context.cls.reportError(message, filename, linep[0], None, 0)

    @classmethod
    @overloaded
    def reportRuntimeError(cls, message,
                                sourceName,
                                lineno,
                                lineSource,
                                lineOffset):
        cx = cls.getCurrentContext()
        if cx is not None:
            return cx.cls.getErrorReporter().runtimeError(message, sourceName, lineno, lineSource, lineOffset)
        else:
            raise EvaluatorException(message, sourceName, lineno, lineSource, lineOffset)
    """

    @classmethod
    def reportRuntimeError0(cls, messageId):
        msg = ScriptRuntime.getMessage0(messageId)
        return cls.reportRuntimeError(msg)

    @classmethod
    def reportRuntimeError1(cls, messageId, arg1):
        msg = ScriptRuntime.getMessage1(messageId, arg1)
        return cls.reportRuntimeError(msg)

    @classmethod
    def reportRuntimeError2(cls, messageId, arg1, arg2):
        msg = ScriptRuntime.getMessage2(messageId, arg1, arg2)
        return cls.reportRuntimeError(msg)

    @classmethod
    def reportRuntimeError3(cls, messageId, arg1, arg2, arg3):
        msg = ScriptRuntime.getMessage3(messageId, arg1, arg2, arg3)
        return cls.reportRuntimeError(msg)

    @classmethod
    def reportRuntimeError4(cls, messageId,
                                 arg1,
                                 arg2,
                                 arg3,
                                 arg4):
        msg = ScriptRuntime.getMessage4(messageId, arg1, arg2, arg3, arg4)
        return cls.reportRuntimeError(msg)

    """
    @classmethod
    @reportRuntimeError.register(type, str)
    def reportRuntimeError_0(cls, message):
        linep = 0
        filename = cls.getSourcePositionFromStack(linep)
        return Context.cls.reportRuntimeError(message, filename, linep[0], None, 0)

    @overloaded"""
    def set_initStandardObjects(self, scope, sealed):
        return ScriptRuntime.initStandardObjects(self, scope, self.sealed)
    
    
    @classmethod
    def getUndefinedValue(cls):
        return Undefined.instance

    def evaluateString(self, scope,
                             source,
                             sourceName,
                             lineno,
                             securityDomain):
        script = self.compileString(source, sourceName, lineno, securityDomain)
        if script is not None:
            return script.execute(self, scope)
        else:
            return

    def evaluateReader(self, scope,
                             readin,
                             sourceName,
                             lineno,
                             securityDomain):
        script = self.compileReader(scope, readin, sourceName, lineno, securityDomain)
        if script is not None:
            return script.execute(self, scope)
        else:
            return

    """
    /**
     * Check whether a string is ready to be compiled.
     * <p>
     * stringIsCompilableUnit is intended to support interactive compilation of
     * javascript.  If compiling the string would result in an error
     * that might be fixed by appending more source, this method
     * returns false.  In every other case, it returns true.
     * <p>
     * Interactive shells may accumulate source lines, using this
     * method after each new line is appended to check whether the
     * statement being entered is complete.
     *
     * @param source the source buffer to check
     * @return whether the source is ready for compilation
     * @since 1.4 Release 2
     */"""
    def stringIsCompilableUnit(self, source):
        errorseen = False
        compilerEnv = CompilerEnvirons()
        compilerEnv.initFromContext(self)
        compilerEnv.setGeneratingSource(False)
        p = Parser(compilerEnv, DefaultErrorReporter.instance)
        try:
            p.parse(source, None, 1)
        except (EvaluatorException, ), ee:
            errorseen = True
        if errorseen and p.eof():
            return False
        else:
            return True

    """
    @overloaded
    def compileReader(self, scope,
                            readin,
                            sourceName,
                            lineno,
                            securityDomain):
        return self.compileReader(readin, sourceName, lineno, securityDomain)

    @compileReader.register(object, Reader, str, int, Object)
    def compileReader_0(self, readin, sourceName, lineno, securityDomain):
        if lineno < 0:
            lineno = 0
        return self.compileImpl(None, readin, None, sourceName, lineno, securityDomain, False, None, None)
    """

    """
    /**
     * Compiles the source in the given string.
     * <p>
     * Returns a script that may later be executed.
     *
     */
    """
    def compileString(self, *args):
        # overloaded in Java
        if len(args) == 4:
            return self.compileString_0(*args)
        else:
            return self.compileString_1(*args)
        
    """
    /**
     * @param source the source string
     * @param sourceName a string describing the source, such as a filename
     * @param lineno the starting line number for reporting errors
     * @param securityDomain an arbitrary object that specifies security
     *        information about the origin or owner of the script. For
     *        implementations that don't care about security, this value
     *        may be null.
     * @return a script that may later be executed
     */
    """
    def compileString_0(self, source, sourceName, lineno, securityDomain):
        if lineno < 0:
            lineno = 0
        return self.compileString_1(source, None, None, sourceName, lineno, securityDomain)

    """
    
    """
    def compileString_1(self, source,
                              compiler,
                              compilationErrorReporter,
                              sourceName,
                              lineno,
                              securityDomain):
        try:
            return self.compileImpl(None, None, source, sourceName, lineno, securityDomain, False, compiler, compilationErrorReporter)
        except (IOException, ), ex:
            raise RuntimeException()

    def compileFunction(self, *args):
        #Overloaded in Java
        if len(args) == 5:
            return self.compileFunction_0(*args)
        else:
            return self.compileFunction_1(*args)

    def compileFunction_0(self, scope,
                              source,
                              sourceName,
                              lineno,
                              securityDomain):
        return self.compileFunction(scope, source, None, None, sourceName, lineno, securityDomain)

    def compileFunction_1(self, scope,
                                source,
                                compiler,
                                compilationErrorReporter,
                                sourceName,
                                lineno,
                                securityDomain):
        try:
            return self.compileImpl(scope, None, source, sourceName, lineno, securityDomain, True, compiler, compilationErrorReporter)
        except (IOException, ), ioe:
            raise RuntimeException()

    def decompileScript(self, script, indent):
        scriptImpl = script
        return scriptImpl.decompile(indent, 0)

    def decompileFunction(self, fun, indent):
        if isinstance(fun, (BaseFunction)):
            return fun.decompile(indent, 0)
        else:
            return "function " + fun.getClassName() + "() {\n\t[native code]\n}\n"

    def decompileFunctionBody(self, fun, indent):
        if isinstance(fun, (BaseFunction)):
            bf = fun
            return bf.decompile(indent, Decompiler.ONLY_BODY_FLAG)
        return "[native code]\n"

    """
    @overloaded
    def newObject(self, scope):
        return self.newObject(scope, "Object", ScriptRuntime.emptyArgs)

    @newObject.register(object, Scriptable, str)
    def newObject_0(self, scope, constructorName):
        return self.newObject(scope, constructorName, ScriptRuntime.emptyArgs)

    @newObject.register(object, Scriptable, str, list)
    def newObject_1(self, scope, constructorName, args):
        scope = ScriptableObject.getTopLevelScope(scope)
        ctor = ScriptRuntime.getExistingCtor(self, scope, constructorName)
        if args is None:
            args = ScriptRuntime.emptyArgs
        return ctor.construct(self, scope, args)

    @overloaded
    def newArray(self, scope, length):
        result = NativeArray(length)
        ScriptRuntime.setObjectProtoAndParent(result, scope)
        return result

    @newArray.register(object, Scriptable, list)
    def newArray_0(self, scope, elements):
        if (elements.getClass().getComponentType() != ScriptRuntime.ObjectClass):
            raise IllegalArgumentException()

        result = NativeArray(elements)
        ScriptRuntime.setObjectProtoAndParent(result, scope)
        return result
    """

    def getElements(self, object):
        return ScriptRuntime.getArrayElements(object)

    @classmethod
    def toBoolean(cls, value):
        return ScriptRuntime.cls.toBoolean(value)

    @classmethod
    def toNumber(cls, value):
        return ScriptRuntime.cls.toNumber(value)

    @classmethod
    def toString(cls, value):
        return ScriptRuntime.cls.toString(value)

    """
    @classmethod
    @overloaded
    def toObject(cls, value, scope):
        return ScriptRuntime.cls.toObject(scope, value)

    @classmethod
    @toObject.register(type, Object, Scriptable, Class)
    def toObject_0(cls, value, scope, staticType):
        return ScriptRuntime.cls.toObject(scope, value)
    """

    @classmethod
    def javaToJS(cls, value, scope):
        if isinstance(value, (strval)) or isinstance(value, (Number)) or isinstance(value, (Boolean)) or isinstance(value, (Scriptable)):
            return value
        else:
            if isinstance(value, (Character)):
                return str(value.charValue())
            else:
                cx = Context.cls.getContext()
                return cx.cls.getWrapFactory().wrap(cx, scope, value, None)

    @classmethod
    def jsToJava(cls, value, desiredType):
        return NativeJavaObject.coerceTypeImpl(desiredType, value)

    @classmethod
    def toType(cls, value, desiredType):
        try:
            return cls.jsToJava(value, desiredType)
        except (EvaluatorException, ), ex:
            ex2 = IllegalArgumentException(ex.getMessage())
            Kit.initCause(ex2, ex)
            raise ex2

    def isGeneratingDebug(self):
        return self.generatingDebug

    def setGeneratingDebug(self, generatingDebug):
        if self.sealed:
            self.onSealedMutation()
        self.generatingDebugChanged = True
        if self.generatingDebug and self.getOptimizationLevel() > 0:
            self.setOptimizationLevel(0)
        self.generatingDebug = self.generatingDebug

    def isGeneratingSource(self):
        return self.generatingSource

    def setGeneratingSource(self, generatingSource):
        if self.sealed:
            self.onSealedMutation()
        self.generatingSource = self.generatingSource

    def getOptimizationLevel(self):
        return self.optimizationLevel

    def setOptimizationLevel(self, optimizationLevel):
        if self.sealed:
            self.onSealedMutation()
        if (self.optimizationLevel == -2):
            self.optimizationLevel = -1
        self.checkOptimizationLevel(self.optimizationLevel)
        if self.codegenClass is None:
            self.optimizationLevel = -1
        self.optimizationLevel = self.optimizationLevel

    @classmethod
    def checkOptimizationLevel(cls, optimizationLevel):
        if isValidOptimizationLevel(cls.optimizationLevel):
            return
        raise IllegalArgumentException("Optimization level outside [-1..9]: " + cls.optimizationLevel)


    def getMaximumInterpreterStackDepth(self):
        return self.maximumInterpreterStackDepth

    def setMaximumInterpreterStackDepth(self, max):
        if self.sealed:
            self.onSealedMutation()
        if (self.optimizationLevel != -1):
            raise IllegalStateException("Cannot set maximumInterpreterStackDepth when optimizationLevel != -1")

        if max < 1:
            raise IllegalArgumentException("Cannot set maximumInterpreterStackDepth to less than 1")

        self.maximumInterpreterStackDepth = max

    def setSecurityController(self, controller):
        if self.sealed:
            self.onSealedMutation()
        if controller is None:
            raise IllegalArgumentException()

        if self.securityController is not None:
            raise SecurityException("Can not overwrite existing SecurityController object")

        if SecurityController.hasGlobal():
            raise SecurityException("Can not overwrite existing global SecurityController object")

        self.securityController = controller

    def setClassShutter(self, shutter):
        if self.sealed:
            self.onSealedMutation()
        if shutter is None:
            raise IllegalArgumentException()

        if self.classShutter is not None:
            raise SecurityException("Cannot overwrite existing " + "ClassShutter object")

        self.classShutter = shutter

    def getClassShutter(self):
        return self.classShutter

    def getThreadLocal(self, key):
        if self.hashtable is None:
            return
        return self.hashtable[key]

    def putThreadLocal(self, key, value):
        if self.sealed:
            self.onSealedMutation()
        if self.hashtable is None:
            self.hashtable = Hashtable()
        self.hashtable.put(key, value)

    def removeThreadLocal(self, key):
        if self.sealed:
            self.onSealedMutation()
        if self.hashtable is None:
            return
        self.hashtable.remove(key)

    def hasCompileFunctionsWithDynamicScope(self):
        return self.compileFunctionsWithDynamicScopeFlag

    def setCompileFunctionsWithDynamicScope(self, flag):
        if self.sealed:
            self.onSealedMutation()
        self.compileFunctionsWithDynamicScopeFlag = flag

    @classmethod
    def setCachingEnabled(cls, cachingEnabled):
        pass

    def setWrapFactory(self, wrapFactory):
        if self.sealed:
            self.onSealedMutation()
        if self.wrapFactory is None:
            raise IllegalArgumentException()
        self.wrapFactory = self.wrapFactory

    def getWrapFactory(self):
        if self.wrapFactory is None:
            self.wrapFactory = WrapFactory()
        return self.wrapFactory

    def getDebugger(self):
        return self.debugger

    def getDebuggerContextData(self):
        return self.debuggerData

    def setDebugger(self, debugger, contextData):
        if self.sealed:
            self.onSealedMutation()
        self.debugger = self.debugger
        self.debuggerData = contextData

    @classmethod
    def getDebuggableView(cls, script):
        if isinstance(script, (NativeFunction)):
            return script.cls.getDebuggableView()
        return

    def hasFeature(self, featureIndex):
        f = self.getFactory()
        return f.hasFeature(self, featureIndex)

    def getE4xImplementationFactory(self):
        return self.getFactory().getE4xImplementationFactory()

    def getInstructionObserverThreshold(self):
        return self.instructionThreshold

    def setInstructionObserverThreshold(self, threshold):
        if self.sealed:
            self.onSealedMutation()
        if threshold < 0:
            raise IllegalArgumentException()

        self.instructionThreshold = threshold

    def observeInstructionCount(self, instructionCount):
        f = self.getFactory()
        f.observeInstructionCount(self, self.instructionCount)

    def createClassLoader(self, parent):
        f = self.getFactory()
        return f.createClassLoader(parent)

    def getApplicationClassLoader(self):
        if self.applicationClassLoader is None:
            f = self.getFactory()
            loader = f.getApplicationClassLoader()
            if loader is None:
                threadLoader = VMBridge.instance.getCurrentThreadClassLoader()
                if threadLoader is not None and Kit.testIfCanLoadRhinoClasses(threadLoader):
                    return threadLoader
                fClass = f.getClass()
                if (fClass != ScriptRuntime.ContextFactoryClass):
                    loader = fClass.getClassLoader()
                else:
                    loader = getClass().getClassLoader()
            self.applicationClassLoader = loader
        return self.applicationClassLoader

    def setApplicationClassLoader(self, loader):
        if self.sealed:
            self.onSealedMutation()
        if loader is None:
            self.applicationClassLoader = None
            return
        if not Kit.testIfCanLoadRhinoClasses(loader):
            raise IllegalArgumentException("Loader can not resolve Rhino classes")

        self.applicationClassLoader = loader

    @classmethod
    def getContext(cls):
        cx = cls.getCurrentContext()
        if cx is None:
            raise RuntimeException("No Context associated with current Thread")

        return cx

    def compileImpl(self, scope,
                          sourceReader,
                          sourceString,
                          sourceName,
                          lineno,
                          securityDomain,
                          returnFunction,
                          compiler,
                          compilationErrorReporter):
        if securityDomain is not None and self.securityController is None:
            raise IllegalArgumentException("securityDomain should be None if setSecurityController() was never called")
            
        if not (sourceReader is None or sourceString is None):
            Kit.codeBug()
        if not (scope is None or returnFunction):
            Kit.codeBug()
        compilerEnv = CompilerEnvirons()
        compilerEnv.initFromContext(self)
        if compilationErrorReporter is None:
            compilationErrorReporter = compilerEnv.getErrorReporter()
        if self.debugger is not None:
            if sourceReader is not None:
                sourceString = Kit.readReader(sourceReader)
                sourceReader = None
        p = Parser(compilerEnv, compilationErrorReporter)
        if returnFunction:
            p.calledByCompileFunction = True
        tree = None#ScriptOrFnNode()
        if sourceString is not None:
            tree = p.parse(sourceString, sourceName, lineno)
        else:
            tree = p.parse(sourceReader, sourceName, lineno)
        if returnFunction:
            if not (tree.getFunctionCount() == 1) and tree.getFirstChild() is not None and (tree.getFirstChild().getType() == Token.FUNCTION):
                raise IllegalArgumentException("compileFunction only accepts source with single JS function: " + sourceString)

        if compiler is None:
            compiler = self.createCompiler()
        encodedSource = p.getEncodedSource()
        bytecode = compiler.compile(compilerEnv, tree, encodedSource, returnFunction)
        if self.debugger is not None:
            if sourceString is None:
                Kit.codeBug()
            if isinstance(bytecode, (DebuggableScript)):
                dscript = bytecode
                self.notifyDebugger_r(self, dscript, sourceString)
            else:
                raise RuntimeException("NOT SUPPORTED")
        result = Object()
        if returnFunction:
            result = compiler.createFunctionObject(self, scope, bytecode, securityDomain)
        else:
            result = compiler.createScriptObject(bytecode, securityDomain)
        return result

    @classmethod
    def notifyDebugger_r(cls, cx, dscript, debugSource):
        cx.cls.debugger.handleCompilationDone(cx, dscript, debugSource)
        ## for-while
        i = 0
        while (i != dscript.getFunctionCount()):
            cls.notifyDebugger_r(cx, dscript.getFunction(i), debugSource)
            i += 1

    #codegenClass = Kit.classOrNull("org.mozilla.javascript.optimizer.Codegen")

    def createCompiler(self):
        result = None
        if self.optimizationLevel >= 0 and self.codegenClass is not None:
            result = Kit.newInstanceOrNull(self.codegenClass)
        if result is None:
            result = Interpreter()
        return result

    @classmethod
    def getSourcePositionFromStack(cls, linep):
        cx = cls.getCurrentContext()
        if cx is None:
            return
        if cx.cls.lastInterpreterFrame is not None:
            return Interpreter.cls.getSourcePositionFromStack(cx, linep)
        writer = CharArrayWriter()
        re = RuntimeException()
        re.printStackTrace(PrintWriter(writer))
        s = str(writer.cls)
        open = -1
        close = -1
        colon = -1
        ## for-while
        i = 0
        while i < len(s):
            c = s.charAt(i)
            if (c == ':'):
                colon = i
            else:
                if (c == '('):
                    open = i
                else:
                    if (c == ')'):
                        close = i
                    else:
                        if (c == '\n') and (open != -1) and (close != -1) and (colon != -1) and open < colon and colon < close:
                            fileStr = s.substring(open + 1, colon)
                            if not fileStr.endsWith(".java"):
                                lineStr = s.substring(colon + 1, close)
                                try:
                                    linep[0] = Integer.parseInt(lineStr)
                                    if linep[0] < 0:
                                        linep[0] = 0
                                    return fileStr
                                except (NumberFormatException, ), e:
                                    pass
                            open = close = colon = -1
            i += 1
        return

    def getRegExpProxy(self):
        if self.regExpProxy is None:
            cl = Kit.classOrNull("org.mozilla.javascript.regexp.RegExpImpl")
            if cl is not None:
                self.regExpProxy = Kit.newInstanceOrNull(cl)
        return self.regExpProxy

    def isVersionECMA1(self):
        return (self.version == self.VERSION_DEFAULT) or self.version >= self.VERSION_1_3

    def getSecurityController(self):
        theglobal = SecurityController.myglobal()
        if theglobal is not None:
            return theglobal
        return self.securityController

    def isGeneratingDebugChanged(self):
        return self.generatingDebugChanged

    def addActivationName(self, name):
        if self.sealed:
            self.onSealedMutation()
        if self.activationNames is None:
            self.activationNames = Hashtable(5)
        self.activationNames.put(name, name)

    def isActivationNeeded(self, name):
        return self.activationNames is not None and self.activationNames.containsKey(name)

    def removeActivationName(self, name):
        if self.sealed:
            self.onSealedMutation()
        if self.activationNames is not None:
            self.activationNames.remove(name)

    
    implementationVersion = ""
    #factory = ContextFactory()
    sealed = bool()
    #sealKey = Object()
    #topCallScope = Scriptable()
    #currentActivationCall = NativeCall()
    #cachedXMLLib = XMLLib()
    #iterating = ObjToIntMap()
    #interpreterSecurityDomain = Object()
    version = 0
    #securityController = SecurityController()
    #classShutter = ClassShutter()
    #errorReporter = ErrorReporter()
    #regExpProxy = RegExpProxy()
    #locale = Locale()
    #generatingDebug = bool()
    #generatingDebugChanged = bool()
    generatingSource = True
    #compileFunctionsWithDynamicScopeFlag = bool()
    #useDynamicScope = bool()
    optimizationLevel = 0
    maximumInterpreterStackDepth = 0
    #wrapFactory = WrapFactory()
    #debugger = Debugger()
    #debuggerData = Object()
    enterCount = 0
    #propertyListeners = Object()
    hashtable = Hashtable()
    #applicationClassLoader = ClassLoader()
    #creationEventWasSent = bool()
    activationNames = Hashtable()
    #lastInterpreterFrame = Object()
    #previousInterpreterInvocations = ObjArray()
    instructionCount = 0
    instructionThreshold = 0
    scratchIndex = 0
    scratchUint32 = long()
    #scratchScriptable = Scriptable()

    def get_initStandardObjects(self):
        return self.initStandardObjects(None, False)

    """
    @set_initStandardObjects.register(object, ScriptableObject)
    def set_initStandardObjects_0(self, scope):
        return self.initStandardObjects(scope, False)
    """

    initStandardObjects = property(get_initStandardObjects, set_initStandardObjects)

    @classmethod
    def get_exit(cls):
        cls.exit(ContextFactory.getGlobal())

    @classmethod
    def set_exit(cls, factory):
        helper = VMBridge.instance.getThreadContextHelper()
        cx = VMBridge.instance.cls.getContext(helper)
        if cx is None:
            raise IllegalStateException("Calling Context.exit without previous Context.enter")

        if cx.cls.factory is not None:
            return
        if cx.cls.enterCount < 1:
            Kit.codeBug()
        if cx.cls.sealed:
            cls.onSealedMutation()
        cx.cls.enterCount -= 1
        if (cx.cls.enterCount == 0):
            VMBridge.instance.setContext(helper, None)
            cls.factory.onContextReleased(cx)

    exit = property(get_exit, set_exit)



