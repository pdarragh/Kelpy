def add(arguments):
    result = arguments[0]
    if len(arguments) > 1:
        for argument in arguments[1:]:
            result += argument
    return result

def multiply(arguments):
    result = arguments[0]
    if len(arguments) > 1:
        for argument in arguments[1:]:
            result *= argument
    return result

def subtract(arguments):
    result = arguments[0]
    if len(arguments) > 1:
        for argument in arguments[1:]:
            result -= argument
    return result

def divide(arguments):
    result = arguments[0]
    if len(arguments) > 1:
        for argument in arguments[1:]:
            result /= argument
    return result

def modulo(arguments):
    result = arguments[0]
    if len(arguments) > 1:
        for argument in arguments[1:]:
            result %= argument
    return result

FUNCTION_MAP = {
    '+': ('Add',        add),
    '*': ('Multiply',   multiply),
    '-': ('Subtract',   subtract),
    '/': ('Divide',     divide),
    '%': ('Modulo',     modulo),
}
