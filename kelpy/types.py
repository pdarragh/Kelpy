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
# KExpression
#   - function expressions
####

class KFunctionExpression(KExpression):
    def __init__(self, raw, function, args):
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

class KFAdd(KFunctionExpression):
    def __init__(self, raw, *args):
        super(KFAdd, self).__init__(raw, '+', args)

class KFMultiply(KFunctionExpression):
    def __init__(self, raw, *args):
        super(KFMultiply, self).__init__(raw, '*', args)

################################################################################
# KExpression
#   - wrappers for primitives
####

class KSymbol(KExpression):
    def __init__(self, raw):
        if not raw[0] == "'":
            raise InvalidSymbolException(raw)
        self.raw = raw
        self.type = "symbol"
    def __repr__(self):
        return "<sym: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "{raw}".format(raw=self.raw)

class KNumber(KExpression):
    def __init__(self, raw):
        self.raw = raw
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