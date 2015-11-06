from function_definitions import *

FUNCTION_MAP = {}
FUNCTION_MAP.update(arithmetic.FUNCTION_MAP)
FUNCTION_MAP.update(comparison.FUNCTION_MAP)

def handle_function(kfunction):
    try:
        return FUNCTION_MAP[kfunction.function][1](kfunction.args)
    except KeyError:
        raise InvalidFunctionException(kfunction.function)
