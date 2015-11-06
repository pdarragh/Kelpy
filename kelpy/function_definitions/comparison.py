import kelpy.types
from kelpy.exceptions import TooFewArgumentsException
from itertools import combinations

def equality(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('==', arguments)
    for argument in arguments[1:]:
        if arguments[0] != argument:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

def inequality(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('!=', arguments)
    for pair in [p for p in combinations(arguments, 2)]:
        if pair[0] == pair[1]:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

def less_than(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('<', arguments)
    for i in xrange(len(arguments) - 1):
        if arguments[i] >= arguments[i + 1]:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

def greater_than(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('>', arguments)
    for i in xrange(len(arguments) - 1):
        if arguments[i] <= arguments[i + 1]:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

def less_than_or_equal(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('<=', arguments)
    for i in xrange(len(arguments) - 1):
        if arguments[i] > arguments[i + 1]:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

def greater_than_or_equal(arguments):
    if len(arguments) < 2:
        raise TooFewArgumentsException('>=', arguments)
    for i in xrange(len(arguments) - 1):
        if arguments[i] < arguments[i + 1]:
            return kelpy.types.KBoolean(False)
    return kelpy.types.KBoolean(True)

FUNCTION_MAP = {
    '==': ('Equality',          equality),
    '!=': ('Inequality',        inequality),
    '<':  ('LessThan',          less_than),
    '>':  ('GreaterThan',       greater_than),
    '<=': ('LessThanEqual',     less_than_or_equal),
    '>=': ('GreaterThanEqual',  greater_than_or_equal),
}
