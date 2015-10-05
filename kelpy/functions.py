from function_definitions import *

SUPPORTED_FUNCTIONS = [
    '+', '-',
    '*', '/',
]

def handle_function(function, arguments):
    raw = function.raw
    if raw == '+':
        return arithmetic.add(arguments)
    elif raw == '-':
        return arithmetic.subtract(arguments)
    elif raw == '*':
        return arithmetic.multiply(arguments)
    elif raw == '/':
        return arithmetic.divide(arguments)
    else:
        raise BadFunctionException(raw)
