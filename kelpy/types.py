################################################################################
#
# This module defines the types used throughout Kelpy, such as the expressions
# produced by the parser and passed into the interpreter.
#
################################################################################

import re
from exceptions import *
from functions import FUNCTION_MAP

################################################################################
# KExpression
#   - top-level class from which the others inherit
####

class KExpression(object):
    def __init__(self):
        raise RawExpressionException()

################################################################################
# KFunctionExpression
#   - function expressions
####

# class KFunctionExpression(KExpression):
#     def __init__(self, function, *args):
#         self.function   = function
#         self.args       = args
#         self.type       = "KF{}".format(FUNCTION_MAP[self.function][0])
#     def __str__(self):
#         return "{type}({arguments})".format(
#             type        = self.type,
#             arguments   = ', '.join([str(argument) for argument in self.args]))
class KFunctionExpression(KExpression):
    def __init__(self, typename, symbol, args):
        self.type   = typename
        self.symbol = symbol
        self.args   = args
    def __str__(self):
        return "{type}({arguments})".format(
            type        = self.type,
            arguments   = (
                '{} '.format(' ' + self.symbol if self.symbol else ',')
            ).join([str(argument) for argument in self.args])
        )

########
# Arithmetic
####

class KAdd(KFunctionExpression):
    def __init__(self, *args):
        super(KAdd, self).__init__('KAdd', '+', args)

class KMultiply(KFunctionExpression):
    def __init__(self, *args):
        super(KMultiply, self).__init__('KMultiply', '*', args)

class KSubtract(KFunctionExpression):
    def __init__(self, *args):
        super(KSubtract, self).__init__('KSubtract', '-', args)

class KDivide(KFunctionExpression):
    def __init__(self, *args):
        super(KDivide, self).__init__('KDivide', '/', args)

class KModulo(KFunctionExpression):
    def __init__(self, *args):
        super(KModulo, self).__init__('KModulo', '%', args)

########
# Comparison
####

class KEquality(KFunctionExpression):
    def __init__(self, *args):
        super(KEquality, self).__init__('KEquality', '==', args)

class KInequality(KFunctionExpression):
    def __init__(self, *args):
        super(KInequality, self).__init__('KInequality', '!=', args)

class KLessThan(KFunctionExpression):
    def __init__(self, *args):
        super(KLessThan, self).__init__('KLessThan', '<', args)

class KGreaterThan(KFunctionExpression):
    def __init__(self, *args):
        super(KGreaterThan, self).__init__('KGreaterThan', '>', args)

class KLessThanEqual(KFunctionExpression):
    def __init__(self, *args):
        super(KLessThanEqual, self).__init__('KLessThanEqual', '<=', args)

class KGreaterThanEqual(KFunctionExpression):
    def __init__(self, *args):
        super(KGreaterThanEqual, self).__init__('KGreaterThanEqual', '>=', args)

################################################################################
# KPrimitive
#   - wrappers for primitives
####

class KPrimitive(KExpression):
    def __init__(self):
        raise RawPrimitiveException(raw)

class KSymbol(KPrimitive):
    def __init__(self, symbol):
        if not symbol[0] == "'":
            raise InvalidSymbolException(symbol)
        self.name = symbol
        self.type  = "symbol"
    def __str__(self):
        return "{}".format(self.name)
    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

class KBoolean(KPrimitive):
    def __init__(self, boolean):
        if str(boolean).lower() in ('true', '#t'):
            self.value = True
        elif str(boolean).lower() in ('false', '#f'):
            self.value = False
        elif isinstance(boolean, KExpression):
            self.value = bool(boolean)
        else:
            raise InvalidBooleanException(boolean)
        self.type = "boolean"
    def __str__(self):
        return "{}".format(self.value)
    def __nonzero__(self):
        return self.value
    def __eq__(self, other):
        return self.value == other.value

class KNumber(KPrimitive):
    def __init__(self, number):
        self.type = "number"
        integer     = re.compile(r"^-?\d+$")
        fraction    = re.compile(r"^-?\d+/\d+$")
        floating_nd = re.compile(r"^-?\d+.\d*$")
        floating_wd = re.compile(r"^-?\d*.\d+$")
        if not (re.match(integer, str(number)) or
                re.match(fraction, str(number)) or
                re.match(floating_nd, str(number)) or
                re.match(floating_wd, str(number))):
            raise InvalidNumberException(number)
        if re.match(integer, str(number)):
            self.value   = int(number)
            self.integer = True
        elif re.match(fraction, str(number)):
            numerator    = number[:number.find('/')]
            denominator  = number[number.find('/') + 1:]
            self.value   = float(numerator) / float(denominator)
            if self.value == int(self.value):
                self.value   = int(self.value)
                self.integer = True
            else:
                self.integer = False
        else:
            self.value   = float(number)
            self.integer = False
    def __str__(self):
        return str(self.value)
    def __add__(self, other):
        return KNumber(str(self.value + other.value))
    def __sub__(self, other):
        return KNumber(str(self.value - other.value))
    def __mul__(self, other):
        return KNumber(str(self.value * other.value))
    def __floordiv__(self, other):
        return KNumber(str(self.value // other.value))
    def __div__(self, other):
        return KNumber(str(self.value / other.value))
    def __mod__(self, other):
        return KNumber(str(self.value % other.value))
    def __lt__(self, other):
        return self.value < other.value
    def __le__(self, other):
        return self.value <= other.value
    def __eq__(self, other):
        return self.value == other.value
    def __ne__(self, other):
        return not self.__eq__(other)
    def __ge__(self, other):
        return self.value >= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __nonzero__(self):
        return self.value != 0

################################################################################
# KList
#   - slightly more advanced primitive with its own methods
#   - handles lists of expressions and such
####

def first(klist):
    if not isinstance(klist, KList):
        raise InvalidFirstException(klist)
    return klist.first

def rest(klist):
    if not isinstance(klist, KList):
        raise InvalidRestException(klist)
    return klist.rest

def reverse(klist):
    if not isinstance(klist, KList):
        raise InvalidReverseException(klist)
    return klist.reverse

def prepend(item, klist):
    if not isinstance(item, KExpression):
        raise InvalidPrependException(item)
    if not isinstance(klist, KList):
        raise InvalidPrependException(klist)
    return KList(item) + klist

def append(item, klist):
    if not isinstance(item, KExpression):
        raise InvalidAppendException(item)
    if not isinstance(klist, KList):
        raise InvalidAppendException(klist)
    return klist + KList(item)

class KList(KPrimitive):
    def __init__(self, *kexps):
        if len(kexps) == 0:
            kexps = []
        elif len(kexps) == 1:
            if isinstance(kexps[0], list):
                kexps = kexps[0]
            else:
                kexps = [kexps[0]]
        else:
            kexps = [kexp for kexp in kexps]
        for kexp in kexps:
            if not isinstance(kexp, KExpression):
                raise InvalidListException("({})".format(', '.join(kexps)))
        self.kexps = kexps
        self.type  = "list"
    def __str__(self):
        return "({})".format(', '.join([str(kexp) for kexp in self.kexps]))
    def __nonzero__(self):
        return len(self.kexps) != 0
    def __add__(self, other):
        return KList(self.kexps + other.kexps)
    def __eq__(self, other):
        if not isinstance(other, KList):
            return False
        if self.empty and other.empty:
            return True
        if ((self.empty and not other.empty) or
            (not self.empty and other.empty)):
            return False
        if self.first != other.first:
            return False
        return self.rest == other.rest
    def __ne__(self, other):
        return not self.__eq__(other)
    def __iter__(self):
        return iter(self.kexps)
    @property
    def first(self):
        try:
            return self.kexps[0]
        except IndexError:
            raise BadListIndexException('0')
    @property
    def rest(self):
        try:
            return KList(self.kexps[1:])
        except IndexError:
            raise BadListIndexException
    @property
    def empty(self):
        return len(self.kexps) == 0
    @property
    def reverse(self):
        return KList(*list(reversed(self.kexps)))

################################################################################
# KEnvironment
#   - environmental abilities are handled with this
####

class KBinding(KExpression):
    def __init__(self, symbol, kexp):
        if not isinstance(symbol, KSymbol):
            raise BadBindingNameException(symbol)
        if not isinstance(kexp, KExpression):
            raise BadBindingValueException(kexp)
        self.symbol = symbol
        self.kexp = kexp
        self.type = "binding"
        self.raw = "{} -> {}".format(symbol, kexp)
    def __str__(self):
        return "({} -> {})".format(self.symbol, self.kexp)

class KEnvironment(KExpression):
    def __init__(self, *bindings):
        self.bindings = KList()
        for binding in bindings:
            if not isinstance(binding, KBinding):
                raise BadEnvironmentBindingException(binding)
            self.bindings += KList(binding)
        self.type = "environment"
    def __str__(self):
        return "{}".format(', '.join([str(binding) for binding in self.bindings]))
    def __add__(self, other):
        if isinstance(other, KBinding):
            return KEnvironment(*(self.bindings + KList(other)))
        else:
            return KEnvironment(*(self.bindings + other.bindings))
    def __iter__(self):
        return iter(self.bindings)

empty_env = KEnvironment()

def lookup(symbol, env):
    if not isinstance(env, KEnvironment):
        raise BadLookupException(symbol)
    for binding in env:
        if binding.symbol == symbol:
            return binding.kexp

################################################################################
# KIf
#   - if expression
####

class KIf(KExpression):
    def __init__(self, test, result_true, result_false):
        self.test   = test
        self.true   = result_true
        self.false  = result_false
        self.type   = "KIf"
    def __str__(self):
        return "{type}({test} ? {true} : {false})".format(
            type    = self.type,
            test    = self.test,
            true    = self.true,
            false   = self.false
        )

################################################################################
# KLet
#   - let things be other things
####

class KLet(KExpression):
    def __init__(self, name, value, body):
        self.name   = name
        self.value  = value
        self.body   = body
        self.type   = "KLet"
    def __str__(self):
        return "with ({name} -> {value}) : {body}".format(
            name    = self.name,
            value   = self.value,
            body    = self.body
        )
