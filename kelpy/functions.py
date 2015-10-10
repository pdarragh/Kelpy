from function_definitions import *

FUNCTION_MAP = {
    '+': ('Add', arithmetic.add),
    '*': ('Multiply', arithmetic.multiply),
    '-': ('Subtract', arithmetic.subtract),
    '/': ('Divide', arithmetic.divide),
    '%': ('Modulo', arithmetic.modulo)
}

def handle_function(kfunction):
    try:
        return FUNCTION_MAP[kfunction.function][1](kfunction.args)
    except KeyError:
        raise InvalidFunctionException(kfunction.function)
