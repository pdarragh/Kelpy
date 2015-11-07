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
# KObject
#   - in case there's ever more than just KExpression, here's the top-top-level
####

class KObject(object):
    def __init__(self, *args):
        self.raw = str(args)
        self.type = "KObject"
    def __repr__(self):
        return "<kobj: {raw}>".format(raw=self.raw)
    def __str__(self):
        return self.raw

################################################################################
# KExpression
#   - top-level class from which the others inherit
####

class KExpression(KObject):
    def __init__(self, raw):
        self.raw = raw
        self.type = "kexp"
    def __repr__(self):
        return "<expr: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "{raw}".format(raw=self.raw)

################################################################################
# KFunctionExpression
#   - function expressions
####

class KFunctionExpression(KExpression):
    def __init__(self, raw, function, *args):
        self.raw        = raw
        self.function   = function
        self.args       = args
        self.type       = "KF{}".format(FUNCTION_MAP[self.function][0])
    def __repr__(self):
        return "<{type}: {raw}>".format(type=self.type, raw=self.raw)
    def __str__(self):
        return "{type}({arguments})".format(
            type        = self.type,
            arguments   = ', '.join([str(argument) for argument in self.args]))

################################################################################
# KIf
#   - if expression
####

class KIf(KExpression):
    def __init__(self, raw, test, result_true, result_false):
        self.raw    = raw
        self.test   = test
        self.true   = result_true
        self.false  = result_false
        self.type   = "KIf"
    def __repr__(self):
        return "<{type}: {raw}>".format(type=self.type, raw=self.raw)
    def __str__(self):
        return "{type}({test} ? {true} : {false})".format(
            type    = self.type,
            test    = self.test,
            true    = self.true,
            false   = self.false
        )

################################################################################
# KPrimitive
#   - wrappers for primitives
####

class KPrimitive(KExpression):
    def __init__(self, raw):
        raise RawPrimitiveException(raw)

class KSymbol(KPrimitive):
    def __init__(self, raw):
        if not raw[0] == "'":
            raise InvalidSymbolException(raw)
        self.raw = raw
        self.type = "symbol"
    def __repr__(self):
        return "<sym: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "{raw}".format(raw=self.raw)

class KBoolean(KPrimitive):
    def __init__(self, raw):
        if str(raw).lower() in ('true', '#t'):
            self.value = True
        elif str(raw).lower() in ('false', '#f'):
            self.value = False
        elif isinstance(raw, KBoolean):
            self.value = raw.value
        elif isinstance(raw, KNumber):
            self.value = raw.value != 0
            self.raw = raw.raw
        else:
            raise InvalidBooleanException(raw)
        self.raw = raw
        self.type = "boolean"
    def __repr__(self):
        return "<bool: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "{value}".format(value=self.value)
    def __nonzero__(self):
        return self.value

class KNumber(KPrimitive):
    def __init__(self, raw):
        self.raw = str(raw)
        self.type = "number"
        integer     = re.compile(r"^-?\d+$")
        floating_nd = re.compile(r"^-?\d+.\d*$")
        floating_wd = re.compile(r"^-?\d*.\d+$")
        if not (re.match(integer, self.raw) or
                re.match(floating_nd, self.raw) or
                re.match(floating_wd, self.raw)):
            raise InvalidNumberException(self.raw)
        if re.match(integer, self.raw):
            self.value = int(self.raw)
        else:
            self.value = float(self.raw)
    def __repr__(self):
        return "<num: {raw}>".format(raw=self.raw)
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
        return self.value != other.value
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

class KList(KPrimitive):
    def __init__(self, *kexps):
        if len(kexps) == 0:
            self.raw = '()'
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
        self.raw = "({})".format(', '.join([kexp.raw for kexp in kexps]))
    def __repr__(self):
        return "<list: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "{raw}".format(raw)
    def __nonzero__(self):
        return len(self.kexps) != 0
    def __add__(self, other):
        return KList(self.kexps + other.kexps)
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

def first(klist):
    if not isinstance(klist, KList):
        raise InvalidFirstException(klist)
    return klist.first

def rest(klist):
    if not isinstance(klist, KList):
        raise InvalidRestException(klist)
    return klist.rest

def cons(*klists):
    result = KList()
    if len(klists) == 0:
        return result
    for klist in klists:
        if not isinstance(klist, KList):
            if isinstance(klist, KExpression):
                result += KList(klist)
            else:
                raise InvalidConsException(klist)
        result += klist
    return result
