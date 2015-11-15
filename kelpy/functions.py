from function_definitions import *

FUNCTION_MAP = {}
FUNCTION_MAP.update(arithmetic.FUNCTION_MAP)
FUNCTION_MAP.update(comparison.FUNCTION_MAP)

def handle_function(function, args):
    try:
        return FUNCTION_MAP[function][1](args)
    except KeyError: # pragma: no cover
        raise InvalidFunctionException(function)
