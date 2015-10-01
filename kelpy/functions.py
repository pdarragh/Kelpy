from function_definitions import *

SUPPORTED_FUNCTIONS = [
    '+', '-',
    '*', '/',
]

def handle_function(function, arguments):
    raw = function.raw
    if raw == '+':
        arithmetic.add(arguments)
    elif raw == '-':
        arithmetic.subtract(arguments)
    elif raw == '*':
        arithmetic.multiply(arguments)
    elif raw == '/':
        arithmetic.divide(arguments)
    else:
        raise BadFunctionException(raw)
