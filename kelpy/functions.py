from function_definitions import *

FUNCTION_MAP = {
    '+': ('Add', arithmetic.add),
    '*': ('Multiply', arithmetic.multiply)
}

def handle_function(kfunction):
    try:
        return FUNCTION_MAP[kfunction.function][1](kfunction.args)
    except KeyError:
        raise InvalidFunctionException(kfunction.function)
